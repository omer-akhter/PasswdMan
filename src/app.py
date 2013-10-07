'''
Created on Sep 30, 2013

@author: omera
'''
import importlib
import logging

from logic import PasswdMan


class App( object ):

    @classmethod
    def instance( cls, config_inst ):
        try:
            return App._instance
        except:
            pass

        if config_inst.logging is None:
            logging.disable( logging.DEBUG )
        else:
            logging.getLogger().setLevel( level=config_inst.logging )

        ui_module = importlib.import_module( config_inst.ui )
        App._instance = ui_module.App( config_inst )
        App._instance.init_ui()
        return App._instance

    def __init__( self, config_inst ):
        self._config_inst = config_inst
        self._passwdman = PasswdMan.instance( config_inst )

    def init_ui( self ):
        raise Exception( 'UI not implemented (1)' )

    def run( self ):
        raise Exception( 'UI not implemented (2)' )
