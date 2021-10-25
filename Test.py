from tkinter import *
import tkinter.ttk as tk
from psycopg2 import *

global conn, status_now
conn = ()
status_now = 0

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
            self.new_wid[a] = b

class trees(tk.Treeview):
    def __init__(self, parent, **sets):
        self.parentt = parent
        self.status = 0
        self.tree = tk.Treeview(parent, show = "headings", selectmode = "browse")
        for a, b in sets.items():
            self.tree[a] = b
        self.scroll = tk.Scrollbar(parent, command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.scroll.set)
    def grid(self, col = 0, r = 0, cols = 1, rows = 1, stick = ""):
        if self.status == 2:
            self.tree.grid()
            self.scroll.grid()
            self.status = 1
            return
        self.tree.grid(column = col, row = r, columnspan = cols, rowspan = rows, sticky = stick)
        self.scroll.grid(column = col + cols, row = r, columnspan = 1, rowspan = rows, sticky = N + S)
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
                if cr == 'c':
                    self.columnconfigure(num, minsize = ms)
                test = 0

class programm:
    def __init__(self, root):
        root.title("База данных цен")
        root.geometry('590x220+{}+{}'.format((root.winfo_screenwidth() // 2 - 300), (root.winfo_screenheight() // 2 - 100)))
        #root.protocol("WN_DELETE_WINDOW")

        self.mat_w = mat_w(root, text = "Материалы")
        self.box_w = wind(root, text = "Корпуса")
        self.sch_w = wind(root, text = "Схемы")
        self.auth_w = auth_w(root, text = "Авторизация", close = lambda: root.destroy())
        self.sett_w = wind(root, text = "Настройки")

        wind.table(root, "r", 0, 20, "r", 1, 30, "r", 2, 20, "c", 0, 20, "c", 1, 50, "c", 2, 20, "c", 3, 50, "c", 4, 20, "c", 5, 50, "c", 6, 20)
        self.mat_w_open = basic(root, Button, text = "Материалы", command = lambda: self.mat_w.open(), width = 10)
        self.mat_w_open.grid(1, 1, 1, 1, N + S + W + E)
        self.box_w_open = basic(root, Button, text = "Корпуса", command = lambda: self.box_w.open(), width = 10)
        self.box_w_open.grid(3, 1, 1, 1, N + S + W + E)
        self.sch_w_open = basic(root, Button, text = "Схемы", command = lambda: self.sch_w.open(), width = 10)
        self.sch_w_open.grid(5, 1, 1, 1, N + S + W + E)
        self.setts = basic(root, Button, bitmap = 'gray12', command = lambda: self.sett_w.open())
        self.setts.grid(0, 3, 1, 1, N + S + W + E)
        self.status = basic(root, Label, text = "Not connected...", bg = 'grey')
        self.status.grid(1, 3, 7, 1, N + S + W + E)

class auth_w(wind):
    def __init__(self, parent, **sets):
        self.auth_w = wind.__init__(self, parent, **sets)
        self.open()
        self.grab_set()
        self.status = "Введите логин/пароль"
        self.note = basic(self, Label, text = self.status)
        self.entry_log = basic(self, Entry, width = 30)
        self.entry_pass = basic(self, Entry, width = 30, show = "*")
        self.butt_ok = basic(self, Button, text = "Ок", width = 8, command = lambda: self.try_auth())
        self.butt_cancel = basic(self, Button, text = "Отмена", width = 8, command = lambda: main_w.destroy())
        self.note.grid(1, 1, 3, 1, N + S + W + E)
        self.entry_log.grid(1, 2, 3, 1, N + S + W + E)
        self.entry_pass.grid(1, 4, 3, 1, N + S + W + E)
        self.butt_ok.grid(1, 6, 1, 1, N + S + W + E)
        self.butt_cancel.grid(3, 6, 1, 1, N + S + W + E)
        self.table('r', 0, 20, 'r', 3, 10, 'r', 5, 20, 'r', 7, 20, 'c', 0, 20, 'c', 4, 20)
    def try_auth(self):
        global conn, status_now
        self.login = self.entry_log.new_wid.get()
        self.passw = self.entry_pass.new_wid.get()
        try:
            conn = connect(dbname = "Prices", user = self.login, password = self.passw, port = "5432")
            status_now = 1
            main.status.upd(text = "Connected as {}".format(self.login))
            self.grab_release()
            self.closing()
        except:
            self.status = "Неверный логин/пароль"
            self.note.upd(text = self.status)
    def check_conn(self):
        global conn, status_now
        try:
            self.cur = conn.cursor()
            self.cur.execute("SELECT")
            self.cur.close()
            status_now = 1
        except:
            status_now = 0
            self.open()
            self.grab_set()
        
        

            
class mat_w(wind):
    def __init__(self, parent, **sets):
        self.mat_w = wind.__init__(self, parent, **sets)
        self.tree_m_gr = trees(self, columns = "Name")
        self.tree_m_u = trees(self, columns = ("Name", "Price", "Date"))
        self.tree_m_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.tree_m_u.size(3, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO, \
            text_2 = "Цена", width_2 = 80, minwidth_2 = 80, stretch_2 = NO, \
                text_3 = "Дата", width_3 = 80, minwidth_3 = 80, stretch_3 = NO)
        self.tree_m_gr.grid(0, 1, 1, 1, N + S + W + E)
        self.tree_m_u.grid(2, 1, 1, 1, N + S + W + E)
        self.fill()
    def fill(self):
        pass
    #    i = 0
    #    self.cur = conn.cursor()
    #    self.cur.execute("SELECT name FROM material_group ORDER BY name")
    #    group = self.cur.fetchall()
    #    for a in group:
    #        self.tree_m_gr.insert(parent = '', index = i, iid = a, values = a)
    #        i += 1
    #    self.cur.close()



#def connection():
#    global conn, status

main_w = Tk()
main = programm(main_w)
main_w.mainloop()
