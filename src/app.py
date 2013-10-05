'''
Created on Sep 30, 2013

@author: omera
'''
import importlib
import logging


class App( object ):
    @classmethod
    def instance( cls, config_inst ):
        if config_inst.logging is None:
            logging.disable( logging.DEBUG )
        else:
            logging.getLogger().setLevel( level=config_inst.logging )

        ui_module = importlib.import_module( config_inst.ui )
        app_inst = ui_module.App( config_inst )
        app_inst.init_ui()
        return app_inst

    def __init__( self, config_inst ):
        self._config_inst = config_inst

    def init_ui(self):
        raise Exception( 'UI not implemented (1)' )

    def run( self ):
        raise Exception( 'UI not implemented (2)' )
