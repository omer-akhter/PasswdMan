'''
Created on Oct 5, 2013

@author: omera
'''
import cPickle
from collections import defaultdict
import datetime
from functools import reduce
import logging
import os
import random
import sys

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class PasswdMan( object ):

    @classmethod
    def instance( cls, config_inst ):
        try:
            return cls._instance
        except:
            pass

        cls._instance = cls( config_inst )
        return cls._instance

    def __init__( self, config_inst ):
        self._config_inst = config_inst
        self._data = {}

    def is_new_store( self ):
        return not ( os.path.isfile( self._config_inst.path_store ) )

    def read( self, callback, key ):
        logging.debug(
            'Loading store file: %s ',
            self._config_inst.path_store )
        self._store_file_e = EncryptedFile( self._config_inst.path_store, key )
        if not self.is_new_store():
            self._data = cPickle.loads( self._store_file_e.read() )

    def load( self ):
        return [x.to_dict() for x in self._data.itervalues()]

    def generate( self, id_ ):
        dict_min_len = self._config_inst.default_min.copy()
        dict_max_len = self._config_inst.default_max.copy()

        len_min_t = dict_min_len.pop( '__' )
        len_max_t = dict_max_len.pop( '__' )
        len_t = random.randint( len_min_t, len_max_t )

        dict_csets = { c: self._config_inst.charset_resolve( c )
                       for c in self._config_inst.charset_choices}
        for k in dict_csets.keys():
            if dict_csets[k] > self._config_inst.charset:
                del dict_csets[k]

        passwd_chars = defaultdict( list )
        for k, v in dict_min_len.iteritems():
            try:
                cset = dict_csets[k]
            except:
                continue
            passwd_chars[k] = random.sample( cset, v )

        for k in set( dict_csets.keys() ) - set( dict_max_len.keys() ):
            dict_max_len[k] = len_t

        len_t_fn = lambda: sum( map( len, passwd_chars.itervalues() ) )
        while len_t_fn() < len_t:
            for k, v in dict_max_len.iteritems():
                try:
                    cset = dict_csets[k]
                except:
                    continue
                if v == 0:
                    continue

                len_curr = len_t_fn()
                len_req = len_t - len_curr
                len_max = min( v, len_req )
                if len_max > 0:
                    len_max = random.randint( 1, len_max )
                    passwd_chars[k] += random.sample( cset, len_max )
                elif len_req == 0:
                    break

        passwd = reduce( lambda x, y: x + y, passwd_chars.itervalues() )
        random.shuffle( passwd )
        passwd = ''.join( passwd )
        return passwd

    def save( self, id_, title, passwd, do_persist=True ):
        passwd_item = None
        if id_:
            passwd_item = self._data.get( id_ )

        if not passwd_item:
            id_set = set( self._data.keys() )

            id_ = random.randint( 1, sys.maxsize )
            while id_ in id_set:
                id_ = random.randint( 1, sys.maxsize )

            passwd_item = self._data[id_] = PasswdItem( id_,
                                                        title, passwd,
                                                        expire=self._config_inst.default_expire,
                                                        charset=self._config_inst.charset,
                                                        min_=self._config_inst.default_min,
                                                        max_=self._config_inst.default_max )
        else:
            passwd_item.set_values( title=title, passwd=passwd )

        if do_persist:
            self._store_file_e.write( cPickle.dumps( self._data ) )

        return passwd_item


class PasswdItem():
    __attrs__ = (
        ( 'id', 'id_' ),
        ( 'title', 'title' ),
        ( 'passwd', 'passwd' ),
        ( 'expire', 'expire' ),
        ( 'charset', 'charset' ),
        ( 'min', 'min_' ),
        ( 'max', 'max_' ),
        ( 'passwd_ts', None )
    )

    def __init__( self, id_, title, passwd,
                  expire=None, charset=None, min_=None, max_=None ):
        self.id = id_
        self.set_values( title, passwd, expire, charset, min_, max_ )
        self._created = self.passwd_ts = self._modified
        self._store_version = 0.1

    def set_values( self, title=None, passwd=None,
                    expire=None, charset=None, min_=None, max_=None ):
        args = locals().items()
        updated = False
        attrs = dict( map( lambda x_y: ( x_y[1], x_y[0] ), self.__attrs__ ) )
        for k, v in args:
            if v is None:
                continue
            try:
                k = attrs[k]
            except:
                continue

            setattr( self, k, v )
            updated = True

        if updated:
            self._modified = datetime.datetime.now()

    def to_dict( self ):
        return { x: getattr( self, x ) for x, _ in self.__attrs__ }


class EncryptedFile( object ):

    def __init__( self, file_path, key ):
        if not key:  # or len( key ) < 8:
            raise Exception( 'Key needs to be at least 8 characters long' )
        self._file_path = file_path
        self._key = SHA256.new( key ).digest()

    def write( self, data ):
        iv = Random.new().read( AES.block_size )
        logging.debug( 'iv size: %d', len( iv ) )
        cipher = AES.new( self._key, AES.MODE_OPENPGP, iv )

        logging.debug( 'data size: %d', len( data ) )
        data_ = cipher.encrypt( data )

        logging.debug( 'data_ size: %d', len( data_ ) )
        with open( self._file_path, 'wb' ) as f:
            f.write( data_ )

    def read( self ):
        with open( self._file_path, 'rb' ) as f:
            data_ = f.read()

        logging.debug( 'data_ size: %d', len( data_ ) )
        iv_len = AES.block_size + 2
        iv = data_[:iv_len]
        logging.debug( 'iv size: %d', len( iv ) )

        data_ = data_[iv_len:]
        logging.debug( 'data_ size: %d', len( data_ ) )

        cipher = AES.new( self._key, AES.MODE_OPENPGP, iv )

        data = cipher.decrypt( data_ )
        logging.debug( 'data size: %d', len( data ) )

        return data
