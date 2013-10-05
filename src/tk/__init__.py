import logging
import ttk

import Tkinter as tk
import app


class App(app.App):
    def init_ui(self):
        self._root = tk.Tk()
        self._root.title('PasswdMan')
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._main_window = ttk.Frame(self._root, width=800, height=600, padding=(3, 3, 3, 3))
        self._main_window.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._main_window.columnconfigure(0, weight=1)
        self._main_window.rowconfigure(0, weight=1)

        col_ = row_ = 0

        self._passwd_list = tk.StringVar()
        self._lst_passwds = tk.Listbox(self._main_window, listvariable=self._passwd_list, width=150)
        self._lst_passwds.grid(column=col_, row=row_, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._lst_passwds.columnconfigure(0, weight=1)
        self._lst_passwds.rowconfigure(0, weight=1)
        self._lst_passwds.bind('<<ListboxSelect>>', self.on_select)

        row_ = 1
        scroll = ttk.Scrollbar(self._main_window, orient=tk.HORIZONTAL, command=self._lst_passwds.xview)
        scroll.grid(column=col_, row=row_, sticky=(tk.E, tk.W))
        self._lst_passwds.configure(xscrollcommand=scroll.set)

        row_ = 0
        col_ = 1
        scroll = ttk.Scrollbar(self._main_window, orient=tk.VERTICAL, command=self._lst_passwds.yview)
        scroll.grid(column=col_, row=row_, sticky=(tk.N, tk.S))
        self._lst_passwds.configure(yscrollcommand=scroll.set)

        col_ = 2
        self._pnl_info = ttk.Labelframe(self._main_window)
        self._pnl_info.grid(column=col_, row=row_, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._pnl_info.columnconfigure(0, weight=0)
        self._pnl_info.rowconfigure(0, weight=1)
        
        col_ = row_ = 0
        self._btn_copy = ttk.Button(self._pnl_info, text='Copy', command=self.on_copy )
        self._btn_copy.grid(column=col_, row=row_, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._btn_copy.rowconfigure(2, weight=1)
        
        row_ += 1
        self._btn_show = ttk.Button(self._pnl_info, text='Show', command=self.on_show )
        self._btn_show.grid(column=col_, row=row_, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._btn_show.rowconfigure(2, weight=1)
        
        row_ += 1
        self._btn_change = ttk.Button(self._pnl_info, text='Change', command=self.on_change )
        self._btn_change.grid(column=col_, row=row_, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._btn_change.rowconfigure(2, weight=1)
        
        row_ += 1
        self._lbl_expires = ttk.Label(self._pnl_info, )
        self._lbl_expires.grid(column=col_, row=row_, sticky=(tk.N, tk.S, tk.E, tk.W))
        self._lbl_expires.rowconfigure(2, weight=0)
        

    def run(self):
        logging.debug('Running Tkinter UI: %s', str(tk.TkVersion))

        lst = (TkPasswdItem(x, '[>%s<]' % x) for x in xrange(10))
        self._passwd_list.set(tuple(str(x) for x in lst))
            
        self._root.mainloop()
    
    def on_copy(self, *args):
        selection = self._lst_passwds.curselection()
        print selection

    def on_show(self, *args):
        selection = self._lst_passwds.curselection()
        print selection

    def on_change(self, *args):
        selection = self._lst_passwds.curselection()
        print selection

    def on_select(self, *args):
        selection = self._lst_passwds.curselection()
        print selection


class TkPasswdItem(object):
    def __init__(self, id_, title):
        self._id = id_
        self._title = title

    def __repr__(self):
        return self._title

