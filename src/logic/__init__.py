'''
Created on Oct 5, 2013

@author: omera
'''
import os

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


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

    def set_key( self, key ):
        # if not key or len( key ) < 8:
        #    raise Exception( 'Key needs to be at least 8 characters long' )
        self._key = key

    def new_store( self ):
        return not ( os.path.isfile( self._config_inst.path_store ) )

    def load_all( self, callback, *attr_list ):
        pass


class EncryptedFile( object ):

    def __init__( self, file_path, key ):
        if not key or len( key ) < 8:
            raise Exception( 'Key needs to be at least 8 characters long' )
        self._file_path = file_path
        self._key = PBKDF2( key, os.urandom( 32 ), dkLen=32, count=5000 )

    def write( self, data ):
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self._key, AES.MODE_OPENPGP, iv )

        data_ = cipher.encrypt( data )
        with open( self._file_path, 'wb' ) as f:
            f.write( data_ )

    def read( self ):
        with open( self._file_path, 'rb' ) as f:
            data_ = f.read()

        iv_len = AES.block_size + 2
        iv = data_[:iv_len]
        data_ = data_[iv_len:]
        cipher = AES.new( self._key, AES.MODE_OPENPGP, iv )

        data = cipher.decrypt( data_ )

        return data
