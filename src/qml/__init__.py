import logging
import os

from PySide import QtCore, QtDeclarative, QtGui, QtOpenGL

import app
import ioutil
import sys


class App( app.App ):
    def run( self ):
        logging.debug( 'Running qml UI' )

        path_qml_base = ioutil.path_con( os.path.join( self._config_inst.path_app, 'qml' ) )
        path_qml_main = os.path.join( path_qml_base, 'passwdman.qml' )

        qtapp = QtGui.QApplication( ['PasswdMan'] )
        qtwindow = QtGui.QMainWindow()
        qtview = QtDeclarative.QDeclarativeView()
        qtglw = QtOpenGL.QGLWidget()
        qtview.setViewport( qtglw )
        qtview.setResizeMode( QtDeclarative.QDeclarativeView.SizeRootObjectToView )

        passwd_model = QtPasswdModel( [QtPasswdItem( {c: '%s%02d' % ( c, i )
            for c in QtPasswdItem.COLUMNS } ) for i in xrange( 1 )] )

        qtrc = qtview.rootContext()
        qtrc.setContextProperty( 'passwd_model', passwd_model )
        #qtrc.setContextProperty( 'passwd_callbacks', QtPasswdItem )


        qtview.setSource( path_qml_main )
        qtwindow.setCentralWidget( qtview )
        qtwindow.show()
        qtapp.exec_()


class QtPasswdItem( QtCore.QObject ):
    COLUMNS = ( 'title', 'passwd', 'expiry' )
    CALLBACKS = ( 'on_select', )
    ALL = COLUMNS + CALLBACKS
    def __init__( self, passwd_inst ):
        QtCore.QObject.__init__( self )
        self._passwd_inst = passwd_inst

    def __getitem__( self, i ):
        if isinstance( i, ( int, long ) ):
            try:
                i = self.COLUMNS[i]
            except Exception:
                i = self.ALL[i]
                return getattr( self, i )
        return self._passwd_inst[i]

    def _title( self ):
        return self._passwd_inst['title']

    changed = QtCore.Signal()
    title = QtCore.Property( unicode, _title, notify=changed )

    @QtCore.Slot()
    def on_select( self ):
        print 'User clicked on:'


class QtPasswdModel( QtCore.QAbstractListModel ):

    def __init__( self, qt_passwd_item_list ):
        QtCore.QAbstractListModel.__init__( self )
        self.setRoleNames( dict( enumerate( QtPasswdItem.ALL ) ) )
        self._qt_passwd_item_list = qt_passwd_item_list

    def rowCount( self, *args, **kwargs ):
        return len( self._qt_passwd_item_list )

    def data( self, index, role ):
        if index.isValid():
            return self._qt_passwd_item_list[index.row()][role]
        return None
