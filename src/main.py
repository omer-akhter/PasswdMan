import logging
import os
import sys

from app import App
import argparse2
import config


def main( *args ):
    pathstr_source = os.path.dirname( __file__ )
    pathstr_conf_d = os.path.join( pathstr_source, 'config.yaml' )
    conf_inst = config.Config.load_yaml( pathstr_conf_d, pathstr_source )

    parser = argparse2.ArgParser2( description='Password Manager' )
    parser.add_argument(
        '-s', '--store', type=argparse2.PathType( canonical=True, check_write=True ),
        default=conf_inst.path_store, help='Store file. Default: %s' % conf_inst.path_store )
    parser.add_argument(
        '-c', '--config', type=argparse2.PathType( canonical=True ),
        default=conf_inst.path_config, help='Configuration file. Default: %s' % conf_inst.path_config )
    parser.add_argument(
        '-i', '--ui', default=conf_inst.ui, choices=conf_inst.ui_choices,
        help='UI to be used. Default: %s' % conf_inst.ui )
    parser.add_argument(
        '-l', '--logging', type=argparse2.LogType(), choices=argparse2.LogType.choices,
        default=conf_inst.logging, help='Logging level. Default: %s' % conf_inst.logging )

    if args:
        args = parser.parse_args( args )
    else:
        args = parser.parse_args()

    conf_inst.update2(
        path_store=args.store,
        path_config=args.config,
        ui=args.ui,
        logging=args.logging )
    conf_inst.load_user_conf()
    conf_inst.save_user_conf()

    App.instance( conf_inst ).run()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelno)s: %(message)s',
        level=logging.DEBUG )
    try:
        main()
    except Exception as e:
        logging.error( 'Fatal Error, application will now exit' )
        logging.error( e, exc_info=True )
        sys.exit( 1 )
