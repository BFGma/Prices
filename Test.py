from tkinter import *
import tkinter.ttk as tk
from psycopg2 import *

conn = ()

class basic(Widget):

    def __init__(self, parent, w_type, **sets):
        self.parent = parent
        self.status = 0
        self.type = w_type
        self.new_wid = self.type(parent)
        for a, b in sets.items():
            self.new_wid[a] = b
       
    def grid(self, col = 0, r = 0, cols = 1, rows = 1, stick = ""):
        if self.status == 2:
            self.new_wid.grid()
            self.status = 1
            return
        self.new_wid.grid(column = col, row = r, columnspan = cols, rowspan = rows, sticky = stick)
        self.status = 1

    def remove(self):
        self.new_wid.grid_remove()
        self.status = 2

    def upd(self, **sets):
        for a, b in sets.items():
            self.mew_wid.config(a = b)

class trees(tk.Treeview):

    def __init__(self, parent, **sets):
        self.parent = parent
        self.status = 0
        self.tree = tk.Treeview(parent, show = "headings", selectmode = "browse")
        for a, b in sets.items():
            self.tree[a] = b
        self.scroll = tk.Skrollbar(parent, command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.scroll.set)

    def grid(self, col = 0, r = 0, cols = 1, rows = 1, stick = ""):
        if self.status == 2:
            self.tree.grid()
            self.scroll.grid()
            self.status = 1
            return
        self.tree.grid(column = col, row = r, columnspan = cols, rowspan = rows, sticky = stick)
        self.scroll.grid(column = col + 1, row = r, columnspan = 1, rowspan = rows, sticky = N + S)
        self.status = 1

    def size(self, col_n, **sets):
        a = 0
        while a <= col_n:
                self.tree.heading("#{}".format(a), text = sets.get("text_{}".format(a), ""))
                self.tree.column("#{}".format(a), minwidth = sets.get("minwidth_{}".format(a), 0), width = sets.get("width_{}".format(a), 100), \
                        stretch = sets.get("stretch_{}".format(a,), "YES"))
                a += 1

    def remove(self):
        self.tree.grid_remove()
        self.status = -1

class wind(Tk):

    def __init__(self, parent = None, **sets):
        Toplevel.__init__(self, parent)
        self.title(sets.get('text', ""))
        self.withdraw()
        self.status = 0
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", sets.get("close", self.closing))
    
    def closing(self):
        self.status = 0
        self.withdraw()

    def open(self):
        if self.status == 1:
            return
        self.status = 1
        self.deiconify()

    def table(self, *sets):
        test = 0
        cr = 0
        num = 0
        ms = 0
        for a in sets:
            print(a)
            if test == 0:
                test = 1
                cr = a
            elif test == 1:
                test = 2
                num = a
            elif test == 2:
                ms = a
                if cr == 'r':
                    self.rowconfigure(num, minsize = ms)
                    print("row", num,ms)
                if cr == 'c':
                    self.columnconfigure(num, minsize = ms)
                    print("col",num,ms)
                test = 0

main_w = Tk()
main_w.title("База данных цен")
main_w.geometry('590x220+{}+{}'.format((main_w.winfo_screenwidth() // 2 - 300), (main_w.winfo_screenheight() // 2 - 100)))
main_w.protocol("WN_DELETE_WINDOW")

mat_w = wind(main_w, text = "Материалы", )
box_w = wind(main_w, text = "Корпуса")
sch_w = wind(main_w, text = "Схемы")
mat_w.table("r", 0 , 20, "r", 3, 39, "r", 5, 20, 'c', 0, 20, 'c', 2, 20, 'c', 4, 20, 'c', 6, 20, 'c', 8, 20, 'c', 10, 200)

main_mat_w_open = basic(main_w, Button, text = "Материалы", command = lambda: mat_w.open())
main_mat_w_open.grid(1, 1, 1, 1, N + S + W + E)
main_box_w_open = basic(mat_w, Button, text = "Корпуса", command = lambda:box_w.open())
main_box_w_open.grid(1, 1, 1, 1, N + S + W + E)
main_sch_w_open = basic(main_w, Button, text = "Схемы", command = lambda: sch_w.open())
main_sch_w_open.grid(5, 1, 1, 1, N + S + W + E)

main_w.mainloop()
