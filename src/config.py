from functools import reduce
import logging
import string

import yaml

import extra


USER_CONF_KEYS = frozenset( (
    'ui',
    'logging',
    'path_store',
    'default_expire',
    'default_charset',
    'default_min',
    'default_max',
) )

CHARSET_CHOICES = {}


class Config( extra.MarkupDictObject ):

    @classmethod
    def load_yaml( cls, path_yaml, path_app ):
        inst = super( Config, cls ).load_yaml( path_yaml )
        inst.__path_app = path_app
        inst.fix_paths()
        return inst

    @property
    def path_app( self ):
        return self.__path_app

    def fix_paths( self ):
        path_store = self.path_store.replace( '$APP', self.__path_app )
        path_config = self.path_config.replace( '$APP', self.__path_app )
        self.update2( path_store=path_store, path_config=path_config )

    @property
    def user_conf( self ):
        try:
            return self.__user_conf
        except Exception:
            try:
                with open( self.path_config ) as f:
                    self.__user_conf = yaml.load( f )
            except IOError as e:
                logging.warn( 'User config could not be read' )
                logging.warn( e )
            except Exception as e:
                logging.exception( e )
            else:
                return self.__user_conf

    def load_user_conf( self ):
        if self.user_conf:
            user_conf = {k: self.user_conf[k]
                         for k in USER_CONF_KEYS if k in self.user_conf}
            self.update2( **user_conf )
            self.fix_paths()

    def save_user_conf( self ):
        user_conf = self.serialize()
        for k in user_conf.keys():
            if k in USER_CONF_KEYS:
                continue
            del user_conf[k]

        user_conf['path_store'] = user_conf[
            'path_store'].replace( self.__path_app, '$APP' )

        if self.user_conf != user_conf:
            try:
                with open( self.path_config, 'w' ) as f:
                    yaml.dump( user_conf, f, default_flow_style=False, )
            except IOError as e:
                logging.warn( 'User config could not be written' )
                logging.warn( e )
            except Exception as e:
                logging.exception( e )

    def charset_resolve( self, charset_id ):
        try:
            return CHARSET_CHOICES[charset_id]
        except Exception:
            charset_id_ = charset_id.lstrip( '__chars_' ).rstrip( '__' )
            try:
                CHARSET_CHOICES[charset_id] = set(
                    getattr( string, charset_id_ ) )
            except Exception:
                if not ( charset_id in self.charset_choices and charset_id.startswith( '__chars_' ) and charset_id.endswith( '__' ) ):
                    return set( charset_id )
                logging.exception( 'Unknown charset: %s', charset_id )

        return CHARSET_CHOICES[charset_id]

    @property
    def charset( self ):
        try:
            return self.__charset
        except Exception:
            self.__charset = reduce(
                lambda x,
                y: x | y,
                ( self.charset_resolve( c ) for c in self.default_charset ) )
        return self.__charset
