from Tkinter import StringVar
import datetime
import logging
import ttk

import Tkinter as tk
import app


class App( app.App ):

    def init_ui( self ):
        self._sel_index = None

        self._root = tk.Tk()
        self._root.title( 'PasswdMan' )
        self._root.columnconfigure( 0, weight=1 )
        self._root.rowconfigure( 0, weight=1 )

        col_ = row_ = 0
        self._btn_new = ttk.Button(
            self._root,
            text='New',
            command=self.on_new )
        self._btn_new.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._btn_new.rowconfigure( 2, weight=0 )

        row_ += 1
        self._txt_show_var = tk.StringVar()
        self._txt_show = ttk.Entry(
            self._root,
            show='*',
            textvariable=self._txt_show_var )
        self._txt_show.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._txt_show.rowconfigure( 2, weight=0 )

        row_ += 1
        self._lbl_expires_var = tk.StringVar()
        self._lbl_expires = ttk.Label(
            self._root,
            textvariable=self._lbl_expires_var )
        self._lbl_expires.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._lbl_expires.rowconfigure( 2, weight=1 )

        row_ += 1
        self._btn_copy = ttk.Button(
            self._root,
            text='Copy',
            command=self.on_copy )
        self._btn_copy.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._btn_copy.rowconfigure( 2, weight=0 )

        row_ += 1
        self._btn_show_hide = ttk.Button(
            self._root,
            text='Show',
            command=self.on_show )
        self._btn_show_hide.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._btn_show_hide.rowconfigure( 2, weight=0 )

        row_ += 1
        self._btn_change = ttk.Button(
            self._root,
            text='Change',
            command=self.on_edit )
        self._btn_change.grid(
            column=col_,
            row=row_,
            sticky=tk.NSEW )
        self._btn_change.rowconfigure( 2, weight=0 )

        row_span = row_
        col_ += 1
        row_ = 0

        self._passwd_list = tk.StringVar()
        self._lst_passwds = tk.Listbox(
            self._root,
            listvariable=self._passwd_list,
            width=150 )
        self._lst_passwds.grid(
            column=col_,
            row=row_,
            rowspan=row_span,
            sticky=tk.NSEW )
        self._lst_passwds.columnconfigure( 0, weight=0 )
        self._lst_passwds.rowconfigure( 0, weight=1 )
        self._lst_passwds.bind( '<<ListboxSelect>>', self.on_select )

        row_ += row_span
        scroll = ttk.Scrollbar(
            self._root,
            orient=tk.HORIZONTAL,
            command=self._lst_passwds.xview )
        scroll.grid( column=col_, row=row_, sticky=tk.EW )
        self._lst_passwds.configure( xscrollcommand=scroll.set )

        row_ = 0
        col_ += 1
        scroll = ttk.Scrollbar(
            self._root,
            orient=tk.VERTICAL,
            command=self._lst_passwds.yview )
        scroll.grid( column=col_, row=row_,
                     rowspan=row_span,
                     sticky=tk.NS )
        self._lst_passwds.configure( yscrollcommand=scroll.set )

    def run( self ):
        logging.debug( 'Running Tkinter UI: %s', str( tk.TkVersion ) )

        self.input_master_passwd()
        self.load_list()

        self._root.mainloop()

    def input_master_passwd( self ):
        def read_callback( errors ):
            if errors:
                self._root.destroy()

        def on_cancel():
            # self._root.quit()
            self._root.destroy()
            return False

        temp = {}
        if self._passwdman.is_new_store():
            def on_confirm( passwd ):
                if temp['passwd'] == passwd:
                    self._passwdman.read( read_callback, passwd )
                    return True

                self._root.destroy()
                return False

            def on_ok( passwd ):
                temp['dlg_pass0'].withdraw()
                temp['dlg_pass1'] = dlg_pass1 = TkInputDlg( self._root,
                                                            'Confirm',
                    passwd=True,
                    on_ok=on_confirm,
                    on_cancel=on_cancel )
                temp['passwd'] = passwd
                self._root.wait_window( dlg_pass1 )

                return True

        else:
            def on_ok( passwd ):
                self._passwdman.read( read_callback, passwd )
                return True

        dlg_pass0 = temp['dlg_pass0'] = TkInputDlg( self._root,
                        'Master Password',
                        passwd=True,
                        on_ok=on_ok,
                        on_cancel=on_cancel )
        self._root.wait_window( dlg_pass0 )

    def load_list( self ):
        self._passwd_dict_dict = {
            x['title']: x for x in self._passwdman.load()}
        self._passwd_title_tpl = tuple(
            sorted( self._passwd_dict_dict.keys() ) )
        self._passwd_dict_tpl = tuple(
            [self._passwd_dict_dict[x] for x in self._passwd_title_tpl] )
        self._passwd_list.set( self._passwd_title_tpl )
        self.clear_fields()

    def clear_fields( self ):
        self._txt_show.config( show='*' )
        self._btn_show_hide.config( text='Show' )
        self._txt_show_var.set( '' )
        self._lbl_expires_var.set( '' )

    @property
    def _dlg_edit_( self ):
        try:
            dlg_edit = self._dlg_edit
            dlg_edit.deiconify()
        except:
            dlg_edit = self._dlg_edit = TkEditPasswdDlg(
                self._root,
                on_cancel=lambda: False,
                on_ok=self.on_save,
                on_generate=self.on_generate )
        return dlg_edit

    def on_new( self, *args ):
        dlg_new = self._dlg_edit_
        dlg_new.set_values( dlg_title='New', title='', passwd_str='' )
        self._root.wait_window( dlg_new )

    @property
    def selection( self ):
        selection = self._lst_passwds.curselection()
        if selection:
            ( i, ) = selection
            if i < len( self._passwd_dict_tpl ):
                return self._passwd_dict_tpl[i]

    def on_select( self, *args ):
        selection = self.selection
        if selection:
            self._txt_show_var.set( selection['passwd'] )
            expires = selection['passwd_ts'] + datetime.timedelta(
                days=selection['expire'] )
            expires = expires.date()
            expires_str = expires.strftime( '%F' )
            self._lbl_expires_var.set( 'Expires: ' + expires_str )
            today_ = datetime.date.today()
            if today_ >= expires:
                self._lbl_expires.config( foreground='#880000' )
            else:
                self._lbl_expires.config( foreground='#000000' )
        else:
            self.clear_fields()

    def on_edit( self, *args ):
        selection = self.selection
        if selection:
            dlg_edit = self._dlg_edit = self._dlg_edit_
            dlg_edit.set_values(
                dlg_title='Edit',
                id_=selection['id'],
                title=selection['title'],
                passwd_str=selection['passwd'] )
            self._root.wait_window( dlg_edit )

    def on_generate( self, id_ ):
        return self._passwdman.generate( id_ )

    def on_save( self, id_, title, passwd ):
        self._passwdman.save( id_, title, passwd )
        self.load_list()
        return False

    def on_copy( self, *args ):
        selection = self.selection
        if selection:
            self._root.clipboard_clear()
            self._root.clipboard_append( selection['passwd'] )

    def on_show( self, *args ):
        selection = self.selection
        if selection:
            if self._txt_show.config()['show'][-1] == '*':
                self._txt_show.config( show='' )
                self._btn_show_hide.config( text='Hide' )
            else:
                self._txt_show.config( show='*' )
                self._btn_show_hide.config( text='Show' )
        else:
            self._txt_show.config( show='*' )


class TkPasswdItem( object ):

    def __init__( self, id_, title ):
        self._id = id_
        self._title = title

    def __repr__( self ):
        return self._title


class TkInputDlg( tk.Toplevel ):

    def __init__( self, master, title, msg=None,
                  passwd=False, on_ok=None, on_cancel=None, cnf=None ):
        if cnf is None:
            cnf = {}
        tk.Toplevel.__init__( self, master, cnf, takefocus=True )
        self.title( title )
        # self.transient( master )

        self.master.withdraw()

        row = 0
        if msg:
            tk.Label( self, text=msg ).grid( row=row, column=0, sticky=tk.E )
            row += 1

        if passwd:
            self._txt0 = tk.Entry( self, show='*' )
        else:
            self._txt0 = tk.Entry( self )
        self._txt0.grid( row=row, column=0, sticky=tk.EW )

        row += 1
        btn = tk.Button( self, text='OK', command=self.on_ok )
        btn.grid( row=row, column=0, sticky=tk.EW )

        row += 1
        btn = tk.Button( self, text='Cancel', command=self.on_cancel )
        btn.grid( row=row, column=0, sticky=tk.EW )

        self._on_ok = on_ok
        self._on_cancel = on_cancel

    def on_ok( self ):
        do_destroy = True
        if self._on_ok:
            do_destroy = self._on_ok( self._txt0.get() )
        if do_destroy:
            self.master.deiconify()
            self.destroy()

    def on_cancel( self ):
        do_destroy = True
        if self._on_cancel:
            do_destroy = self._on_cancel()
        if do_destroy:
            self.master.deiconify()
            self.destroy()


class TkEditPasswdDlg( tk.Toplevel ):
    data_fields = (
        'id_'
        'title',
        'expiry',
        'passwd_str',
        'expire',
        'charset',
        'min',
        'max' )

    def __init__( self, master, title=None,
                 on_ok=None, on_cancel=None, on_generate=None, cnf=None, **kwargs ):
        data = {
            f: kwargs.pop(
                '_' +
                f ) if (
                    '_' +
                    f ) in kwargs else None for f in self.data_fields }
        if cnf is None:
            cnf = {}
        tk.Toplevel.__init__( self, master, cnf, takefocus=True, **kwargs )
        if title:
            self.title( title )
        # self.transient( master )

        self.master.withdraw()

        row = 0
        tk.Label( self, text='Title:' ).grid( row=row, column=0, sticky=tk.E )
        self._txt_title_var = tk.StringVar()
        self._txt_title = tk.Entry( self, textvariable=self._txt_title_var )
        self._txt_title.grid( row=row, column=1, sticky=tk.EW )

        row += 1

        tk.Label(
            self,
            text='Password:' ).grid(
                row=row,
                column=0,
                sticky=tk.E )
        self._txt_passwd_var = tk.StringVar()
        self._txt_passwd = tk.Entry(
            self,
            textvariable=self._txt_passwd_var,
            show='*' )
        self._txt_passwd.grid( row=row, column=1, sticky=tk.EW )

        btn = tk.Button( self, text='Generate', command=self.on_generate )
        btn.grid( row=row, column=2, sticky=tk.EW )

        row += 1

        btn = tk.Button( self, text='OK', command=self.on_ok )
        btn.grid( row=row, column=0, sticky=tk.EW )

        btn = tk.Button( self, text='Cancel', command=self.on_cancel )
        btn.grid( row=row, column=1, sticky=tk.EW )

        self._on_ok = on_ok
        self._on_cancel = on_cancel
        self._on_generate = on_generate

        self.set_values( **data )

    def set_values( self, dlg_title=None, id_=None,
                   title=None, passwd_str=None, **kwargs ):
        if dlg_title is not None:
            self.title( dlg_title )

        self.id_ = id_
        if title is not None:
            self._txt_title_var.set( title )
        if passwd_str is not None:
            self._txt_passwd_var.set( passwd_str )

        self._txt_title.focus_set()

    def get_values( self ):
        return {
            'id_': getattr( self, 'id_', None ),
            'title': self._txt_title_var.get(),
            'passwd': self._txt_passwd_var.get(),
        }

    def on_generate( self ):
        if self._on_generate:
            passwd_str = self._on_generate( self.get_values()['id_'] )
            self._txt_passwd_var.set( passwd_str )

    def on_ok( self ):
        do_destroy = True
        if self._on_ok:
            do_destroy = self._on_ok( **self.get_values() )

        self.master.deiconify()
        if do_destroy:
            self.destroy()
        else:
            self.withdraw()

    def on_cancel( self ):
        do_destroy = True
        if self._on_cancel:
            do_destroy = self._on_cancel()

        self.master.deiconify()
        if do_destroy:
            self.destroy()
        else:
            self.withdraw()
