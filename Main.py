from asyncio.windows_events import NULL
from cgitb import grey
from re import A
from sqlite3 import enable_shared_cache
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from tkinter.tix import DirSelectBox
import tkinter.ttk as tk
from turtle import onclick
from psycopg2 import *
import xlsxwriter
from datetime import date

global conn, connection_status
conn = ()
connection_status = 0

class basic(Widget):
    def __init__(self, parent, w_type, **sets):                         #создание класса виджетов
        w_type.__init__(self, parent)
        self.parent = parent
        self.status = 0
        self.type = w_type
        self.new_wid = self.type(parent)
        for a, b in sets.items():
            self.new_wid[a] = b
    def grid(self, col = 0, r = 0, cols = 1, rows = 1, stick = ""):     #grid для виджетов
        if self.status == 2:
            self.new_wid.grid()
            self.status = 1
            return
        self.new_wid.grid(column = col, row = r, columnspan = cols, rowspan = rows, sticky = stick)
        self.status = 1
    def remove(self):                                                   #скрытие виджетов
        self.new_wid.grid_remove()
        self.status = 2
    def upd(self, **sets):                                              #обновление виджетов
        for a, b in sets.items():
            self.new_wid[a] = b

class trees(tk.Treeview):
    def __init__(self, parent, **sets):                                 #создание класса дерева
        tk.Treeview.__init__(self, parent)
        self.status = 0
        self.tree = tk.Treeview(parent, show = "headings", selectmode = "browse")
        for a, b in sets.items():
            self.tree[a] = b
        self.scroll = tk.Scrollbar(parent, command = self.tree.yview)
        self.tree.configure(yscrollcommand = self.scroll.set)
    def grid(self, col = 0, r = 0, cols = 1, rows = 1, stick = ""):     #grid для дерева
        if self.status == 2:
            self.tree.grid()
            self.scroll.grid()
            self.status = 1
            return
        self.tree.grid(column = col, row = r, columnspan = cols, rowspan = rows, sticky = stick)
        self.scroll.grid(column = col + cols, row = r, columnspan = 1, rowspan = rows, sticky = N + S)
        self.status = 1
    def size(self, col_n, **sets):                                      #определение колонок дерева
        a = 0
        while a <= col_n:
                self.tree.heading("#{}".format(a), text = sets.get("text_{}".format(a), ""))
                self.tree.column("#{}".format(a), minwidth = sets.get("minwidth_{}".format(a), 0), width = sets.get("width_{}".format(a), 100), \
                        stretch = sets.get("stretch_{}".format(a,), "YES"))
                a += 1
    def remove(self):                                                   #скрытие дерева
        self.tree.grid_remove()
        self.status = -1

class wind(Tk):
    def __init__(self, parent = None, **sets):              #создание класса окон
        Toplevel.__init__(self, parent)
        self.title(sets.get('text', ""))
        self.withdraw()
        self.status = -1
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", sets.get("close", self.closing))
    def closing(self):                                      #процесс закрытия окон по нажатию х
        self.status = 0
        self.withdraw()
    def open(self):                                         #процесс открытия окон при нажатии кнопки в главном окне
        if self.status == 1:
            return
        self.status = 1
        self.deiconify()
    def table(self, *sets):                                 #верстка окна
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

class TreeEntry(Entry):                                 #Класс для изменения дерева
    def __init__(self, parent, iid, col, text = "", **kw):
        super().__init__(parent, **kw)
        self.field = parent
        self.iid = iid
        self.col = col
        self.insert(0, text)
        self['exportselection'] = False
        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())
        self.bind("<FocusOut>", self.on_return) #???? мб сделать запись в таком случае ????
    def on_return(self, event):
        self.field.set(self.iid, self.col, value = self.get())
        self.destroy()
    def select_all(self, *ignore):
        self.selection_range(0, 'end')
        return 'break'

class main:
    def __init__(self, root):                               #инициализация + виджеты
        root.title("База данных цен")
        root.geometry('+{}+{}'.format((root.winfo_screenwidth() // 2 - 295), (root.winfo_screenheight() // 2 - 110)))
        root.protocol("WN_DELETE_WINDOW", self.close)
        self.mat = mat(root, text = "Материалы", close = lambda: mat.close(self.mat))
        self.box_w = box_w(root, text = "Корпуса")
        self.sch_w = wind(root, text = "Схемы")
        self.auth_w = auth(root, text = "Авторизация", close = lambda: root.destroy())
        self.sett_w = wind(root, text = "Настройки")
        wind.table(root, "r", 0, 20, "r", 2, 30, "r", 3, 20, "r", 4, 30, "r", 5, 20, "r", 6, 30, "r", 7, 20, \
            "r", 10, 30, "c", 0, 20, "c", 1, 20, "c", 2, 100, "c", 4, 40)
        self.mat_open = basic(root, Button, text = "Материалы", command = lambda: self.mat.reopen(), width = 10)
        self.mat_open.grid(2, 2, 2, 1, N + S + W + E)
        self.box_w_open = basic(root, Button, text = "Корпуса", command = lambda: self.box_w.reopen(), width = 10)
        self.box_w_open.grid(2, 4, 2, 1, N + S + W + E)
        self.sch_w_open = basic(root, Button, text = "Схемы", command = lambda: self.sch_w.open(), width = 10)
        self.sch_w_open.grid(2, 6, 2, 1, N + S + W + E)
        self.setts = basic(root, Button, bitmap = 'gray12', command = lambda: self.sett_w.open())
        self.setts.grid(0, 10, 1, 1, N + S + W + E)
        self.status = basic(root, Label, text = "Not connected...", bg = '#BABABA')
        self.status.grid(1, 10, 5, 1, N + S + W + E)
    def close(self):                                        #закртыие соединения при закрытии окна
        if (conn):
            conn.close()
        programm.destroy()

class auth(wind):
    def __init__(self, parent, **sets):                     #инициализация + виджеты
        self.auth_w = wind.__init__(self, parent, **sets)
        self.geometry('+{}+{}'.format((parent.winfo_screenwidth() // 2 - 110), (parent.winfo_screenheight() // 2 - 80)))
        self.var()
        self.open()
        self.grab_set()
        self.status = "Введите логин/пароль"
        self.note = basic(self, Label, text = self.status)
        self.entry_log = basic(self, Entry, width = 30)
        self.entry_pass = basic(self, Entry, width = 30, show = "*")
        self.butt_ok = basic(self, Button, text = "Ок", width = 8, command = lambda: self.auth())
        self.butt_cancel = basic(self, Button, text = "Отмена", width = 8, command = lambda: main_w.close())
        self.note.grid(1, 1, 3, 1, N + S + W + E)
        self.entry_log.grid(1, 2, 3, 1, N + S + W + E)
        self.entry_pass.grid(1, 4, 3, 1, N + S + W + E)
        self.butt_ok.grid(1, 6, 1, 1, N + S + W + E)
        self.butt_cancel.grid(3, 6, 1, 1, N + S + W + E)
        self.table('r', 0, 20, 'r', 3, 10, 'r', 5, 20, 'r', 7, 20, 'c', 0, 20, 'c', 4, 20)
    def var(self):                                          #переменные
        self.role = 1                            #класс роли
    def auth(self):                                         #авторизация
        global conn, connection_status
        self.login = self.entry_log.new_wid.get()
        self.passw = self.entry_pass.new_wid.get()
        try:
            conn = connect(dbname = "Prices_v0.2", user = self.login, password = self.passw, port = "5432")
            connection_status = 1
            main_w.status.upd(text = "Connected as {}".format(self.login))
            conn.set_session(autocommit = True)
            self.grab_release()
            self.check()
            self.closing()
        except:
            self.status = "Неверный логин/пароль"
            self.note.upd(text = self.status)
    def check(self):                                        #автопроверка авторизации
        global conn, connection_status
        try:
            self.cur = conn.cursor()
            self.cur.execute("SELECT")
            self.cur.close()
            connection_status = 1
            main_w.status.upd(text = "Connected as {}".format(self.login))
        except Exception as error:
            connection_status = 0
            main_w.status.upd(text = "Disconnected by server: {}".format(error))
            self.open()
            self.grab_set()
        self.after(10000, self.check)
        
class mat(wind):                                        #Закончено: -добавить автоопределение группы при добавлении материала
    def __init__(self, parent, **sets):                     #инициализация
        self.mat = wind.__init__(self, parent, **sets)
        self.var()
        self.wid()
    def var(self):                                          #переменные (UND)
        self.wind_status = 0
        self.f1_wind_status = 0
        self.f2_wind_status = 0
        self.change_vend_wind_status = 0
        self.change_seq_wind_status = 0
        self.vendor_list = {0:0}
        self.mat_gr_list = {0:0}
        self.mat_list = {0:0}
        self.m_u = [([0]*3 + [''] + [0] + ['']*6),]
    def wid(self):                                          #виджеты
        self.f1 = trees(self, columns = ("Code","Name"), displaycolumns = ("Name"), height = 20)
        self.f2 = trees(self, columns = ("Name", "Price", "Meas", "Prod", "Date"), displaycolumns = ("Name", "Price", "Meas", "Prod", "Date"))
        self.f1.size(1, text_1 = "Название группы", width_1 = 220, minwidth_1 = 220, stretch_1 = NO)
        self.f2.size(5, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO, \
            text_2 = "Цена", width_2 = 80, minwidth_2 = 80, stretch_2 = NO, \
                text_3 = "Ед", width_3 = 30, minwidth_3 = 80, stretch_3 = NO, \
                    text_4 = "Произв.", width_4 = 80, minwidth_4 = 80, stretch_4 = NO, \
                        text_5 = "Дата", width_5 = 80, minwidth_5 = 80, stretch_5 = NO)
        self.status_separ = basic(self, tk.Separator, orient = HORIZONTAL)
        self.status_bar = basic(self, Label, text = "-")
        self.top_menu()
        self.f1_menu()
        self.f2_menu()
        self.f2_menu_empty()
        self.f1.grid(0, 1, 1, 1, N + S + W + E)
        self.f2.grid(2, 1, 1, 1, N + S + W + E)
        self.status_separ.grid(0, 2, 4, 1, N + S + W + E)
        self.status_bar.grid(0, 2, 4, 1, N + S + W + E)
        self.bind('<F5>', lambda event: self.f1_fill())
        #self.f1.tree.bind('<ButtonRelease-1>', lambda event: self.f2_fill(self.f1.tree.focus()))
        self.f1.tree.bind('<ButtonRelease-1>', self.f2_fill)
    def get_vendor(self):
        self.cur = conn.cursor()
        self.cur.execute("SELECT code, name FROM vendor ORDER BY name")
        self.vendor_list = dict(self.cur.fetchall())
        self.vendor_list[0] = '---'
        self.cur.close()
    def change_vendor(self):
        if self.change_vend_wind_status == 1:
            return
        self.change_vend_wind = Toplevel(self)
        x = programm.winfo_screenwidth()/2
        y = programm.winfo_screenheight()/2
        self.change_vend_wind.geometry('+%d+%d' % (x, y))
        self.change_vend_wind.resizable(0, 0)
        self.change_vend_wind.grab_set()
        self.change_vend_wind_status = 1
        self.change_vend_f = trees(self.change_vend_wind, columns = ("Code", "Name"))
        self.change_vend_f.size(2, text_1 = "Код", width_1 = 30, stretch_1 = NO, text_2 = "Название", width_2 = 240, stretch_2 = NO)
        self.change_vend_toadd = StringVar()
        self.change_vend_entry = basic(self.change_vend_wind, tk.Entry, width = 30, textvariable = self.change_vend_toadd)
        self.change_vend_button = basic(self.change_vend_wind, tk.Button, width = 30, text = "Добавить", command = lambda: self.change_vend_add(self.change_vend_toadd.get()))
        self.change_vend_button_status = 1
        self.change_vend_popup = Menu(self, tearoff = 0)
        self.change_vend_popup.add_command(label = "Удалить", command = lambda: self.change_vend_del(self.change_vend_target))
        self.change_vend_popup.add_command(label = "Переименовать", command = lambda:self.change_vend_ren(self.change_vend_target))
        self.change_vend_f.tree.bind('<Button-3>', self.change_vend_menu)
        self.change_vend_f.grid(0, 0, 1, 1, N + S + W + E)
        self.change_vend_entry.grid(0, 1, 1, 1, N + S + W + E)
        self.change_vend_button.grid(0, 2, 1, 1, N + S + W + E)
        self.change_vend_fill()
        self.change_vend_wind.protocol("WM_DELETE_WINDOW", self.change_vend_wind_close)
    def change_vend_wind_close(self):
        self.change_vend_wind_status = 0
        self.change_vend_wind.grab_release()
        self.change_vend_wind.destroy()
    def change_vend_menu(self, event):                          #открытие меню для Д1
        self.change_vend_target = self.change_vend_f.tree.identify_row(event.y)
        if self.change_vend_target:
            self.change_vend_f.tree.selection_set(self.change_vend_target)
            self.change_vend_popup.tk_popup(event.x_root, event.y_root)
    def change_vend_fill(self):
        self.change_vend_drop()
        self.get_vendor()
        print('asdasd')
        for a in self.vendor_list:
            if a == 0:
                continue
            self.change_vend_f.tree.insert(parent = '', iid = a, index = a, values = (a, self.vendor_list[a])) 
    def change_vend_drop(self):
        self.change_vend_f.tree.delete(*self.change_vend_f.tree.get_children())
    def change_vend_add(self, target):
        self.cur = conn.cursor()
        self.cur.execute("INSERT INTO Vendor(code, name) VALUES (DEFAULT, '{}')".format(target))
        self.cur.close()
        self.change_vend_fill()
    def change_vend_del(self, target):
        self.cur = conn.cursor()
        self.cur.execute("DELETE FROM Vendor WHERE code = {}".format(target))
        self.cur.close()
        self.change_vend_fill()
    def change_vend_ren(self, target):
        self.change_vend_toadd.set(self.vendor_list[int(target)])
        self.change_vend_button.upd(text = "Изменить", command = lambda: self.change_vend_revr(target, self.change_vend_toadd.get()))
        self.change_vend_button_status = -1
        self.change_vend_wind.bind('<Escape>', lambda event: self.change_vend_back())
    def change_vend_back(self):
        if self.change_vend_button_status == 1:
            return
        self.change_vend_button.upd(text = "Добавить", command = lambda: self.change_vend_add(self.change_vend_toadd.get()))
        self.change_vend_toadd.set('')
        self.change_vend_button_status = 1
    def change_vend_revr(self, code, target):
        #print("UPDATE Vendor SET name = '{}' WHERE code = {}".format(target, code))
        self.cur = conn.cursor()
        self.cur.execute("UPDATE Vendor SET name = '{}' WHERE code = {}".format(target, code))
        self.cur.close()
        self.change_vend_fill()
    def change_seq(self):
        if self.change_seq_wind_status == 1:
            return
        self.change_seq_wind = Toplevel(self)
        x = programm.winfo_screenwidth()/2
        y = programm.winfo_screenheight()/2
        self.change_seq_wind.geometry('+%d+%d' % (x, y))
        self.change_seq_wind.resizable(0, 0)
        self.change_seq_wind.grab_set()
        self.change_seq_wind_status = 1
        self.change_seq_button = basic(self.change_seq_wind, tk.Button, text = "Выгрузить значения", command = lambda: self.change_seq_get())
        self.change_seq_gr_frame = basic(self.change_seq_wind, tk.Labelframe, text = "Посл. групп:")
        self.change_seq_mat_frame = basic(self.change_seq_wind, tk.Labelframe, text = "Посл. материалов:")
        self.change_seq_vend_frame = basic(self.change_seq_wind, tk.Labelframe, text = "Посл. производителей:")
        self.change_seq_button.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_gr_frame.grid(0, 1, 1, 1, N + S + W + E)
        self.change_seq_mat_frame.grid(0, 2, 1, 1, N + S + W + E)
        self.change_seq_vend_frame.grid(0, 3, 1, 1, N + S + W + E)
        self.change_seq_gr_now_frame = basic(self.change_seq_gr_frame.new_wid, tk.Labelframe, text = "Тек.:")
        self.change_seq_gr_max_frame = basic(self.change_seq_gr_frame.new_wid, tk.Labelframe, text = "Maкс.:")
        self.change_seq_gr_upd = basic(self.change_seq_gr_frame.new_wid, tk.Button, state = DISABLED, text = "Записать", command = lambda: self.change_seq_upd(1))
        self.change_seq_gr_now_frame.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_gr_max_frame.grid(1, 0, 1, 1, N + S + W + E)
        self.change_seq_gr_upd.grid(2, 0, 1, 1, N + S + W + E)
        self.change_seq_gr_now_text = StringVar()
        self.change_seq_gr_max_text = StringVar()
        self.change_seq_gr_now = basic(self.change_seq_gr_now_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_gr_now_text)
        self.change_seq_gr_now.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_gr_max = basic(self.change_seq_gr_max_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_gr_max_text)
        self.change_seq_gr_max.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_mat_now_frame = basic(self.change_seq_mat_frame.new_wid, tk.Labelframe, text = "Тек.:")
        self.change_seq_mat_max_frame = basic(self.change_seq_mat_frame.new_wid, tk.Labelframe, text = "Maкс.:")
        self.change_seq_mat_upd = basic(self.change_seq_mat_frame.new_wid, tk.Button, state = DISABLED, text = "Записать", command = lambda: self.change_seq_upd(2))
        self.change_seq_mat_now_frame.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_mat_max_frame.grid(1, 0, 1, 1, N + S + W + E)
        self.change_seq_mat_upd.grid(2, 0, 1, 1, N + S + W + E)
        self.change_seq_mat_now_text = StringVar()
        self.change_seq_mat_max_text = StringVar()
        self.change_seq_mat_now = basic(self.change_seq_mat_now_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_mat_now_text)
        self.change_seq_mat_now.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_mat_max = basic(self.change_seq_mat_max_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_mat_max_text)
        self.change_seq_mat_max.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_vend_now_frame = basic(self.change_seq_vend_frame.new_wid, tk.Labelframe, text = "Тек.:")
        self.change_seq_vend_max_frame = basic(self.change_seq_vend_frame.new_wid, tk.Labelframe, text = "Maкс.:")
        self.change_seq_vend_upd = basic(self.change_seq_vend_frame.new_wid, tk.Button, state = DISABLED, text = "Записать", command = lambda: self.change_seq_upd(3))
        self.change_seq_vend_now_frame.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_vend_max_frame.grid(1, 0, 1, 1, N + S + W + E)
        self.change_seq_vend_upd.grid(2, 0, 1, 1, N + S + W + E)
        self.change_seq_vend_now_text = StringVar()
        self.change_seq_vend_max_text = StringVar()
        self.change_seq_vend_now = basic(self.change_seq_vend_now_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_vend_now_text)
        self.change_seq_vend_now.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_vend_max = basic(self.change_seq_vend_max_frame.new_wid, tk.Entry, state = DISABLED, textvariable = self.change_seq_vend_max_text)
        self.change_seq_vend_max.grid(0, 0, 1, 1, N + S + W + E)
        self.change_seq_wind.protocol("WM_DELETE_WINDOW", self.change_seq_wind_close)
    def change_seq_get(self):
        self.cur = conn.cursor()
        self.cur.execute("select last_value, is_called FROM mat_gr_code_seq")
        for a, b in self.cur.fetchall():
            if b == FALSE:
                self.change_seq_gr_now_text.set(a - 1)
            else:
                self.change_seq_gr_now_text.set(a)
        self.cur.execute("select MAX(code) FROM mat_gr")
        a = self.cur.fetchone()[0]
        if not a:
            self.change_seq_gr_max_text.set(0)
        else:
            self.change_seq_gr_max_text.set(a)
        if self.change_seq_gr_now_text.get() == self.change_seq_gr_max_text.get():
            self.change_seq_gr_upd.upd(state = DISABLED)
        else:
            self.change_seq_gr_upd.upd(state = NORMAL)

        self.cur.execute("select last_value, is_called FROM mat_code_seq")
        for a, b in self.cur.fetchall():
            if b == FALSE:
                self.change_seq_mat_now_text.set(a - 1)
            else:
                self.change_seq_mat_now_text.set(a)
        self.cur.execute("select MAX(code) FROM mat")
        a = self.cur.fetchone()[0]
        if not a:
            self.change_seq_mat_max_text.set(0)
        else:
            self.change_seq_mat_max_text.set(a)
        if self.change_seq_mat_now_text.get() == self.change_seq_mat_max_text.get():
            self.change_seq_mat_upd.upd(state = DISABLED)
        else:
            self.change_seq_mat_upd.upd(state = NORMAL)

        self.cur.execute("select last_value, is_called FROM vendor_code_seq")
        for a, b in self.cur.fetchall():
            if b == FALSE:
                self.change_seq_vend_now_text.set(a - 1)
            else:
                self.change_seq_vend_now_text.set(a)
        self.cur.execute("select MAX(code) FROM vendor")
        a = self.cur.fetchone()[0]
        if not a:
            self.change_seq_vend_max_text.set(0)
        else:
            self.change_seq_vend_max_text.set(a)
        if self.change_seq_vend_now_text.get() == self.change_seq_vend_max_text.get():
            self.change_seq_vend_upd.upd(state = DISABLED)
        else:
            self.change_seq_vend_upd.upd(state = NORMAL)

        self.cur.close()

    def change_seq_upd(self, task):
        self.cur = conn.cursor()
        if task == 1:
                self.cur.execute("ALTER SEQUENCE mat_gr_code_seq RESTART WITH {}".format(int(self.change_seq_gr_max_text.get()) + 1))
        elif task == 2:
            self.cur.execute("ALTER SEQUENCE mat_code_seq RESTART WITH {}".format(int(self.change_seq_mat_max_text.get()) + 1))
        elif task == 3:
            self.cur.execute("ALTER SEQUENCE vendor_code_seq RESTART WITH {}".format(int(self.change_seq_vend_max_text.get()) + 1))
        self.cur.close()
        self.change_seq_get()
    def change_seq_wind_close(self):
        self.change_seq_wind_status = 0
        self.change_seq_wind.grab_release()
        self.change_seq_wind.destroy()
    def top_menu(self):
        self.all_menu = Menu(self.mat)
        self.config(menu = self.all_menu)
        self.edit_menu = Menu(self.all_menu, tearoff = 0)
        self.edit_menu.add_command(label = "Обновить", command = lambda: self.f1_fill())
        self.edit_menu.add_command(label = "Изм. произв.", command = lambda: self.change_vendor())
        self.edit_menu.add_command(label = "Создать таблицу", command = lambda: self.generate_mat_excel())
        self.all_menu.add_cascade(label = "Ред.", menu = self.edit_menu)
        self.razr_menu = Menu(self.all_menu, tearoff = 0)
        self.razr_menu.add_command(label = "Настройки последовательностей", command = lambda: self.change_seq())
        #self.razr_menu.add_command(label = "Ошибка в id мат-лов", command = lambda: self.change_mat_seq())
        self.all_menu.add_cascade(label = "Разработчик", menu = self.razr_menu)
    def f1_fill(self):                                      #заполнение Д1
        self.f2_drop()
        self.f1_drop()
        self.f1.tree.insert(parent = '', iid = -1, index = 0, values = (0, "Все"))
        i = 1
        self.cur = conn.cursor()
        self.cur.execute("SELECT code, name FROM Mat_gr ORDER BY CASE WHEN code > 0 THEN code END;")
        self.mat_gr_list = dict(self.cur.fetchall())
        for a in self.mat_gr_list:
            self.f1.tree.insert(parent = '', iid = a, index = i, values = (a, self.mat_gr_list[a]))
            i += 1
        #self.mat_gr_list[0] = '---'
        self.cur.close()
    def f1_drop(self):                                      #очистка Д1
        self.f1.tree.delete(*self.f1.tree.get_children())
    def f1_menu(self):                                      #выпадающее меню для Д1
        self.f1_popup = Menu(self, tearoff = 0)
        self.f1_popup.add_command(label = "Удалить", command = lambda: self.f1_del(self.f1_target))
        self.f1_popup.add_command(label = "Изменить", command = lambda: self.f1_wind_open(self.f1_target))
        self.f1_popup.add_command(label = "Добавить", command = lambda: self.f1_wind_open())
        self.f1.tree.bind('<Button-3>', self.f1_menu_open)
    def f1_menu_open(self, event):                          #открытие меню для Д1
        self.f1_target = self.f1.tree.identify_row(event.y)
        if self.f1_target:
            self.f1.tree.selection_set(self.f1_target)
            self.f1_popup.tk_popup(event.x_root, event.y_root)
    def f1_wind_open(self, target = ''):                    #открытие окна добавления в Д1
        if self.f1_wind_status == 1:
            return
        self.f1_wind = Toplevel(self)
        x = programm.winfo_screenwidth()/2
        y = programm.winfo_screenheight()/2
        self.f1_wind.geometry('+%d+%d' % (x, y))
        self.f1_wind_status = 1
        if target:
            self.f1_wind.title("Изменение группы")
        else:
            self.f1_wind.title("Добавление группы")
        self.f1_wind.resizable(0, 0)
        self.f1_wind.grab_set()
        self.target = StringVar()
        self.target.set(self.f1.tree.set(target, column = "Name"))
        self.f1_wind_entry = basic(self.f1_wind, tk.Entry, width = 30, textvariable = self.target)
        self.f1_wind_cancel = basic(self.f1_wind, tk.Button, width = 10, text = "Отмена", command = lambda: self.f1_wind_close())
        if target:
            self.f1_wind_ok = basic(self.f1_wind, tk.Button, width = 10, text = "Изменить", command = lambda: self.f1_change(self.target.get(), target))
        else:
            self.f1_wind_ok = basic(self.f1_wind, tk.Button, width = 10, text = "Добавить", command = lambda: self.f1_add(self.target.get()))
        self.f1_wind_entry.grid(1, 1, 3, 1, N + S + W + E)
        self.f1_wind_cancel.grid(1, 3, 1, 1, N + S + W + E)
        self.f1_wind_ok.grid(3, 3, 1, 1, N + S + W + E)
        self.f1_wind.columnconfigure(0, minsize = 20)
        self.f1_wind.columnconfigure(2, minsize = 60)
        self.f1_wind.columnconfigure(4, minsize = 20)
        self.f1_wind.rowconfigure(0, minsize = 20)
        self.f1_wind.rowconfigure(2, minsize = 20)
        self.f1_wind.rowconfigure(4, minsize = 20)
        self.f1_wind.protocol("WM_DELETE_WINDOW", self.f1_wind_close)
    def f1_wind_close(self):                                #закрытие окна добавления в Д1
        self.f1_wind_status = 0
        self.f1_wind.grab_release()
        self.f1_wind.destroy()
    def f1_add(self, target):                               #добавление в Д1 
        try:
            self.cur = conn.cursor()
            self.cur.execute("INSERT INTO Mat_gr(name) VALUES ('{}')".format(target))
            self.cur.close()
            self.status_bar.upd(text = "Добавлена группа {}".format(target))
            self.f1_fill()
        except:
            self.status_bar.upd(text = "Ошибка добавления группы {}".format(target))
    def f1_change(self, target, code):                       #изменение в Д1
        if not target:
            self.status_bar.upd(text = "Поле не может быть пустым")
            return
        try:
            self.cur = conn.cursor()
            self.cur.execute("UPDATE Mat_gr SET name = '{new}' WHERE code = '{code}'".format(new = target, code = code))
            self.cur.close()
            self.status_bar.upd(text = "Группа {code} переименована в {new}".format(code = self.mat_gr_list[int(code)], new = target))
            self.f1_fill()
            self.f1_wind_close()
            self.f1_wind_open(code)
        except:
            self.status_bar.upd(text = "Ошибка изменения группы {}".format(self.mat_gr_list[int(code)]))
    def f1_del(self, target):                               #удаление в Д1 (UND)
        self.f1_del_check = messagebox.askokcancel(title = "Удаление группы", \
            parent = self, message = \
                "Удалить группу {}? Все вложенные записи будут перемещены в \"Без группы\""\
                    .format(self.mat_gr_list[int(target)]), icon = messagebox.WARNING)
        if self.f1_del_check == TRUE:
            try:
                self.cur = conn.cursor()
                self.cur.execute("DELETE FROM mat_gr WHERE code = {}".format(target))
                self.cur.close()
                self.status_bar.upd(text = "Удалена группа {}".format(self.mat_gr_list[int(target)]))
                self.f1_fill()
            except:
                self.status_bar.upd(text = "Ошибка удаления группы {}".format(target))
    def f2_fill(self, event = None):                        #заполнение Д2
        if event:
            target = self.f1.tree.identify_row(event.y)
        else:
            try:
                target = self.f2_grouptofill
            except:
                return
        if not target:
            return
        self.f1.tree.selection_set(target)
        self.f2_grouptofill = target
        self.f2_drop()
        i = 1
        self.cur = conn.cursor()
        if target == "-1":
            self.cur.execute("SELECT m.code, m.code_gr, m.code_producer, v.name, m.code_vendor, m.producer_code, m.vendor_code, m.name, m.price, m.meas, m.upddate FROM mat AS m INNER JOIN vendor as v ON (m.code_producer = v.code) ORDER BY m.name")
        else:
            pass
            self.cur.execute("SELECT m.code, m.code_gr, m.code_producer, v.name, m.code_vendor, m.producer_code, m.vendor_code, m.name, m.price, m.meas, m.upddate FROM mat as m INNER JOIN vendor as v on (m.code_producer = v.code) WHERE m.code_gr = %s ORDER BY m.name", (target,))
        self.m_u = self.cur.fetchall()
        self.mat_list = dict()
        self.mat_list[0] = 0
        for a, b, c, d, e, f, g, h, j, k, l in self.m_u:
            self.f2.tree.insert(parent = '', index = i, iid = a, values = (h, j, k, d, l))
            self.mat_list[a] = i
            i += 1
        self.m_u.insert(0, ([0]*3 + [''] + [0] + ['']*6))
        self.cur.close()
    def f2_drop(self):                                      #очистка Д2
        self.f2.tree.delete(*self.f2.tree.get_children())
    def f2_menu(self):                                      #выпадающее меню для Д2 (UND)
        self.f2_popup = Menu(self, tearoff = 0)
        self.f2_popup.add_command(label = "Удалить", command = lambda: self.f2_del(self.f2_target))
        self.f2_popup.add_command(label = "Изменить", command = lambda: self.f2_wind_open(self.f2_target))
        self.f2_popup.add_command(label = "Добавить", command = lambda: self.f2_wind_open())
        self.f2.tree.bind('<Button-3>', self.f2_menu_open)
    def f2_menu_empty(self):                                #выпадающее меню для Д2 - только добавление
        self.f2_popup_empty = Menu(self, tearoff = 0)
        self.f2_popup_empty.add_command(label = "Добавить", command = lambda: self.f2_wind_open())
        self.f2.tree.bind('<Button-3>', self.f2_menu_open)
    def f2_menu_open(self, event):                          #открытие меню для Д2 (UND)
        self.f2_target = self.f2.tree.identify_row(event.y)
        if self.f2_target:
            self.f2.tree.selection_set(self.f2_target)
            self.f2_popup.tk_popup(event.x_root, event.y_root)
        else:
            self.f2_popup_empty.tk_popup(event.x_root, event.y_root)
    def f2_wind_open(self, target = 0):                    #открытие окна добавления в Д2 (UND)
        if self.f2_wind_status == 1:
            return
        self.f2_wind = Toplevel(self)
        #центровка окна
        x = programm.winfo_screenwidth()/2
        y = programm.winfo_screenheight()/2
        self.f2_wind.geometry('+%d+%d' % (x, y))
        self.f2_wind_status = 1
        self.f2_wind_status_text = StringVar()
        self.f2_target_code = StringVar()
        self.f2_target_gr = StringVar()
        self.f2_target_name = StringVar()
        self.f2_target_pr = StringVar()
        self.f2_target_v = StringVar()
        self.f2_target_pr_code = StringVar()
        self.f2_target_v_code = StringVar()
        self.f2_target_price = StringVar()
        self.f2_target_meas = StringVar()
        self.f2_target_updd = StringVar()
        self.f2_target_price_error = StringVar()
        if target:
            #print(self.m_u[self.f2.tree.index(target)])
            #target = self.f2.tree.item(self.f2_target).get('values')
            self.f2_wind.title("Изменение материала")
            self.f2_wind_status_text.set("Изменение материала")
            #print(target, self.m_u[self.mat_list[int(target)]][0])
            self.f2_target_code.set(target)
            self.f2_target_gr.set(self.mat_gr_list[self.m_u[self.mat_list[int(target)]][1]])
            self.f2_wind_ok = basic(self.f2_wind, tk.Button, width = 15, text = "Изменить", command = lambda: self.f2_change(target))
        else:
            try:
                self.cur = conn.cursor()
                self.cur.execute("select last_value, is_called FROM mat_code_seq")
                for a, b in self.cur.fetchall():
                    if b == True:
                        self.f2_target_code.set(a + 1)
                    else:
                        self.f2_target_code.set(a)
                self.cur.close()
            except:
                pass    
            self.f2_wind.title("Добавление материала")   
            self.f2_wind_status_text.set("Добавление материала")
            if self.f1.tree.focus() == '-1' or self.f1.tree.focus() == '':
                self.f2_target_gr.set(self.mat_gr_list[0])
            else:
                self.f2_target_gr.set(self.mat_gr_list[int(self.f1.tree.focus())])
            self.f2_wind_ok = basic(self.f2_wind, tk.Button, width = 15, text = "Добавить", command = lambda: self.f2_add())
        self.f2_wind.resizable(0, 0)
        self.f2_wind.grab_set()
        i = 0
        self.f2_target_name.set(self.m_u[self.mat_list[int(target)]][7])
        self.f2_target_pr.set(self.vendor_list[self.m_u[self.mat_list[int(target)]][2]])
        self.f2_target_v.set(self.vendor_list[self.m_u[self.mat_list[int(target)]][4]])
        self.f2_target_pr_code.set(self.m_u[self.mat_list[int(target)]][5])
        self.f2_target_v_code.set(self.m_u[self.mat_list[int(target)]][6])
        self.f2_target_price.set(self.m_u[self.mat_list[int(target)]][8])
        self.f2_target_meas.set(self.m_u[self.mat_list[int(target)]][9])
        self.f2_target_updd.set(self.m_u[self.mat_list[int(target)]][10])
        ######виджеты 
        self.f2_wind_frame_code = basic(self.f2_wind, tk.Labelframe, text = "Артикул:")
        self.f2_wind_code = basic(self.f2_wind_frame_code.new_wid, tk.Entry, state = DISABLED, textvariable = self.f2_target_code)
        self.f2_wind_status_textbox = basic(self.f2_wind, tk.Label, textvariable = self.f2_wind_status_text)
        self.f2_wind_frame_name = basic(self.f2_wind, tk.Labelframe, text = "Название:")
        self.f2_wind_name = basic(self.f2_wind_frame_name.new_wid, tk.Entry, textvariable = self.f2_target_name)
        self.f2_wind_frame_price = basic(self.f2_wind, tk.Labelframe, text = "Цена:")
        self.f2_wind_price_validate = (self.register(self.f2_wind_validate), '%P')
        self.f2_wind_price = basic(self.f2_wind_frame_price.new_wid, tk.Entry, validate = 'key', validatecommand = self.f2_wind_price_validate, \
            textvariable = self.f2_target_price)
        self.f2_wind_frame_meas = basic(self.f2_wind, tk.Labelframe, text = "Изм.:")
        self.f2_wind_meas = basic(self.f2_wind_frame_meas.new_wid, tk.Combobox, state = 'readonly', textvariable = self.f2_target_meas, \
            values = ["шт", "кг", "м", "м2", "м3", "л"])
        self.f2_wind_frame_gr = basic(self.f2_wind, tk.Labelframe, text = "Группа:")
        self.f2_wind_gr = basic(self.f2_wind_frame_gr.new_wid, tk.Combobox, state = 'readonly', textvariable = self.f2_target_gr, \
            values = list(self.mat_gr_list.values()))
        self.f2_wind_frame_updd = basic(self.f2_wind, tk.Labelframe, text = "Дата")
        self.f2_wind_updd = basic(self.f2_wind_frame_updd.new_wid, tk.Entry, textvariable = self.f2_target_updd)
        self.f2_wind_frame_prod = basic(self.f2_wind, tk.Labelframe, text = "Производитель:")
        self.f2_wind_prod = basic(self.f2_wind_frame_prod.new_wid, tk.Combobox, state = 'readonly', textvariable = self.f2_target_pr, \
            values = list(self.vendor_list.values()))
        self.f2_wind_frame_v = basic(self.f2_wind, tk.Labelframe, text = "Поставщик:")
        self.f2_wind_v = basic(self.f2_wind_frame_v.new_wid, tk.Combobox, state = 'readonly', textvariable = self.f2_target_v, \
            values = list(self.vendor_list.values()))
        self.f2_wind_frame_pr_code = basic(self.f2_wind, tk.Labelframe, text = "Код поставщика:")
        self.f2_wind_pr_code = basic(self.f2_wind_frame_pr_code.new_wid, tk.Entry, textvariable = self.f2_target_pr_code)
        self.f2_wind_frame_v_code = basic(self.f2_wind, tk.Labelframe, text = "Код поставщика:")
        self.f2_wind_v_code = basic(self.f2_wind_frame_v_code.new_wid, tk.Entry, textvariable = self.f2_target_v_code)
        self.f2_wind_cancel = basic(self.f2_wind, tk.Button, width = 15, text = "Отмена", command = lambda: self.f2_wind_close())
        self.f2_wind_price_error = basic(self.f2_wind, tk.Label, textvariable = self.f2_target_price_error)
        ######расстановка виджетов
        self.f2_wind_status_textbox.grid(11, 3, 8, 1)
        self.f2_wind_frame_code.grid(1, 1, 7, 1, N + S + W + E)
        self.f2_wind_frame_name.grid(1, 5, 14, 1, N + S + W + E)
        self.f2_wind_frame_price.grid(16, 5, 5, 1, N + S + W + E)
        self.f2_wind_price_error.grid(16, 6, 5, 1, N + S + W + E)
        self.f2_wind_frame_meas.grid(22, 5, 3, 1, N + S + W + E)
        self.f2_wind_frame_gr.grid(1, 7, 8, 1, N + S + W + E)
        self.f2_wind_frame_prod.grid(10, 7, 7, 1, N + S + W + E)
        self.f2_wind_frame_v.grid(18, 7, 7, 1, N + S + W + E)
        self.f2_wind_frame_updd.grid(1, 9, 8, 1, N + S + W + E)
        self.f2_wind_frame_pr_code.grid(10, 9, 7, 1, N + S + W + E)
        self.f2_wind_frame_v_code.grid(18, 9, 7, 1, N + S + W + E)
        self.f2_wind_cancel.grid(2, 11, 5, 1, N + S + W + E)
        self.f2_wind_ok.grid(19, 11, 5, 1, N + S + W + E)

        self.f2_wind_code.new_wid.pack(fill=X)#grid(1, 1, 1, 1)
        self.f2_wind_name.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_price.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_meas.new_wid.pack(fill=X)#grid(0, 0, 3, 1)
        self.f2_wind_gr.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_prod.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_v.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_updd.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        self.f2_wind_pr_code.new_wid.pack(fill=X)#grid(0, 0 ,1 ,1)
        self.f2_wind_v_code.new_wid.pack(fill=X)#grid(0, 0, 1, 1)
        ######обрамление 
        i = 0
        while i < 26:
            self.f2_wind.columnconfigure(i, minsize = 20)
            i = i + 1
        i = 0
        while i < 13:
            self.f2_wind.rowconfigure(i, minsize = 10)
            i = i + 1
        self.f2_wind.protocol("WM_DELETE_WINDOW", self.f2_wind_close)
    def f2_wind_validate(self, value):                      #проверка введенных данных в Д2
        if value:
            try:
                float(value)
                self.f2_target_price_error.set('')
                return True
            except ValueError:
                self.f2_target_price_error.set('Неверные символы')
                return False
        else:
            #self.f2_wind_status_text.set('Цена не может быть пустой')
            return True
    def f2_wind_close(self):                                #закрытие окна добавления в Д2 (UND)
        self.f2_wind_status = 0
        self.f2_wind.grab_release()
        self.f2_wind.destroy()
    def f2_add(self):                                       #добавление в Д2 (UND)
        try:
            if not self.f2_target_price.get():
                self.f2_target_price.set(0)
            self.cur = conn.cursor()
            self.cur.execute("INSERT INTO mat(name, code_gr, price, meas, code_producer, upddate, code_vendor, producer_code, vendor_code) VALUES \
            ('{name}', {gr}, {price}, '{meas}', {prod}, '{upddate}', {vend}, '{prod_code}', '{vend_code}')".format(name = self.f2_target_name.get(), \
                gr = list(self.mat_gr_list.keys())[list(self.mat_gr_list.values()).index(self.f2_target_gr.get())], price = self.f2_target_price.get(), meas = self.f2_target_meas.get(), \
                    prod = list(self.vendor_list.keys())[list(self.vendor_list.values()).index(self.f2_target_pr.get())], upddate = date.today().strftime('%Y-%m-%d'), \
                        vend = list(self.vendor_list.keys())[list(self.vendor_list.values()).index(self.f2_target_v.get())], prod_code = self.f2_target_pr_code.get(), \
                            vend_code = self.f2_target_v_code.get()))
            self.cur.close()
            self.status_bar.upd(text = "Добавлен материал {}".format(self.f2_target_name.get()))
            self.f2_fill()
            self.f2_wind_close()
            self.f2_wind_open()
        except:
            self.status_bar.upd(text = "Ошибка добавления материала {}".format(self.f2_target_name.get()))
    def f2_change(self, code_target):               #изменение в Д2 (UND)
        try:
            if not self.f2_target_price.get():
                self.f2_target_price.set(0)
            self.cur = conn.cursor()
            self.cur.execute("UPDATE mat SET name = '{name}', code_gr = {gr}, price = {price}, meas = '{meas}', code_producer = {prod}, \
                    upddate = '{upddate}', code_vendor = {vend}, producer_code = '{prod_code}', vendor_code = '{vend_code}' WHERE code = {code}".format(name = self.f2_target_name.get(), \
                        gr = list(self.mat_gr_list.keys())[list(self.mat_gr_list.values()).index(self.f2_target_gr.get())], price = self.f2_target_price.get(), \
                            meas = self.f2_target_meas.get(), prod = list(self.vendor_list.keys())[list(self.vendor_list.values()).index(self.f2_target_pr.get())], \
                                upddate = date.today().strftime('%Y-%m-%d'), \
                                    vend = list(self.vendor_list.keys())[list(self.vendor_list.values()).index(self.f2_target_v.get())], prod_code = self.f2_target_pr_code.get(), \
                                        vend_code = self.f2_target_v_code.get(), code = code_target))
            self.cur.close()
            self.status_bar.upd(text = "Изменен материал {}".format(self.f2_target_name.get()))
            self.f2_fill()
            self.f2_wind_close()
            #self.f2_wind_open(code_target)
        except:
            self.status_bar.upd(text = "Ошибка изменения материала {}".format(self.f2_target_name.get()))
    def f2_del(self, target):                               #удаление в Д2 (UND)
        if target:
            target_name = self.m_u[self.mat_list[int(target)]][7]
        self.f2_del_check = \
            messagebox.askokcancel(title = "Удаление материала", \
                parent = self, message = "Удалить материал {}?"\
                    .format(target_name), icon = messagebox.WARNING)
        if self.f2_del_check == TRUE:
            try:
                self.cur = conn.cursor()
                self.cur.execute("DELETE FROM mat WHERE code = {}".format(target))
                self.cur.close()
                self.status_bar.upd(text = "Удален материал {}".format(target_name))
                self.f2_fill()
                self.f2_wind_close()
            except:
                self.status_bar.upd(text = "Ошибка удаления материала {}".format(target_name))
    def generate_mat_excel(self):
        files = [('Excel file', '*.xlsx')]
        file = asksaveasfilename(filetypes = files, defaultextension = files)
        if file == '':
            return
        self.mat_excel = xlsxwriter.Workbook(file)
        self.mat_excel_1sheet = self.mat_excel.add_worksheet('Цены')
        self.cur = conn.cursor()
        self.cur.execute('SELECT m.code as "Код", gr.name as "Группа", v.name as "Производитель", \
            vv.name as "Поставщик", m.producer_code as "Код произв.", m.vendor_code as "Код пост.", m.name as "Название", \
                m.price as "Цена", m.meas as "Ед.", m.upddate "Дата обновл." FROM mat AS m INNER JOIN vendor as v ON (m.code_producer = v.code) \
                    INNER JOIN mat_gr as gr ON (m.code_gr = gr.code) INNER JOIN vendor as vv ON (m.code_vendor = vv.code) order by gr.name, m.name;')
        self.mat_excel_list = self.cur.fetchall()

        self.mat_excel_format_top = self.mat_excel.add_format({'font_size': '18', 'font_color': '#191970', 'bold': True})
        self.mat_excel_format_names = self.mat_excel.add_format({'bold': True})
        sizes = (('Код', 6, ''), ('Название', 64, ''), ('Цена', 12, {'num_format': '0.00'}), ('Ед.', 5, ''), ('Дата', 12, {'num_format': 'dd.mm.YY'}), \
            ('Производитель', 18, ''), ('Код произв.', 18, {'font_color': '#808080'}), ('Поставщик', 18, ''), ('Код поставщ.', 18, {'font_color': '#808080'}))
        self.mat_excel_format = []
        col = 0
        for a, b, c in sizes:
            self.mat_excel_format.append(self.mat_excel.add_format(c))
            self.mat_excel_1sheet.set_column(col, col, b, self.mat_excel_format[col])
            self.mat_excel_1sheet.write_string(0, col, a, self.mat_excel_format_names)
            col = col + 1
        
        prev_gr = ''
        row = 1
        col = 0
        for a, b, c, d, e, f, g, h, i, j in self.mat_excel_list:
            if not prev_gr == b:
                self.mat_excel_1sheet.merge_range(row, col, row, col + 8, b, self.mat_excel_format_top)
                row = row + 1
            self.mat_excel_1sheet.write(row, col, a)        #код
            self.mat_excel_1sheet.write(row, col + 1, g)    #название
            self.mat_excel_1sheet.write(row, col + 2, h)    #цена   
            self.mat_excel_1sheet.write(row, col + 3, i)    #измерение
            self.mat_excel_1sheet.write(row, col + 4, j)    #дата обновления
            self.mat_excel_1sheet.write(row, col + 5, c)    #производитель
            self.mat_excel_1sheet.write(row, col + 6, e)    #код у производителя
            self.mat_excel_1sheet.write(row, col + 7, d)    #поставщик
            self.mat_excel_1sheet.write(row, col + 8, f)    #код у поставщика
            row = row + 1
            prev_gr = b
        self.mat_excel.close()
    def reopen(self):                                       #открытие окна материалов по нажатию кнопки в главном окне
        self.open()
        if self.wind_status == 0:
            self.f1_fill()
            self.get_vendor()
            self.wind_status = 1
        self.status_bar.upd(text = "-")
    def close(self):                                        #доп. опции закрытия окна
        self.closing()

class box_w(wind):
    def __init__(self, parent, **sets):
        self.box_w = wind.__init__(self,parent, **sets)
        self.box_gr_opened = ''
        self.var()
        self.widgets_frame()
    def var(self):
        self.box_gr_list = {0:0}
        self.add_box_gr_status = 0
        self.info = ['', '', '', '']
        self.info_det = [[]]
    def widgets_frame(self):                                #создание фрэймов
        self.frame_box_gr = basic(self, tk.Frame)
        self.frame_box = basic(self, tk.Frame)
        self.frame_box_info = basic(self, tk.Frame)
        self.frame_box_det = basic(self, tk.Labelframe, text = "Детали")
        self.frame_box_mat = basic(self, tk.Labelframe, text = "Стандартные материалы")
        self.frame_box_mat_choose = basic(self, tk.Frame)
        self.frame_box_status = basic(self, tk.Frame)
        self.frame_box_gr_fill(self.frame_box_gr)
        self.frame_box_fill(self.frame_box)
        self.frame_box_info_fill(self.frame_box_info)
        self.frame_box_det_fill(self.frame_box_det)
        self.frame_box_mat_fill(self.frame_box_mat)
        self.frame_box_status_fill(self.frame_box_status)
        self.frame_box_gr.grid(0, 1, 1, 3)
        self.frame_box.grid(1, 1, 1, 3)
        self.frame_box_info.grid(2, 1, 1, 1)
        self.frame_box_det.grid(2, 2, 1, 1)
        self.frame_box_mat.grid(2, 3, 1, 1)
        self.frame_box_status.grid(0, 4, 3, 1)
    def frame_box_gr_fill(self, frame):                     #виджеты фрейма_1 (группы)
        self.tree_box_gr = trees(frame.new_wid, columns = ("Code", "Name"), displaycolumns = ("Name"), height = 30)
        self.tree_box_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.popup_menu = Menu(self, tearoff = 0)
        self.popup_menu.add_command(label = "Удалить", command = lambda: self.del_box_gr(self.chosed_box_gr))
        self.popup_menu.add_command(label = "Изменить", command = lambda: self.add_box_gr(self.chosed_box_gr))
        self.popup_menu.add_command(label = "Добавить", command = lambda: self.add_box_gr())
        self.tree_box_gr.grid(0, 0, 1, 1, N + S + W + E)
        self.tree_box_gr.tree.bind('<ButtonRelease-1>', lambda event: self.tree_box_fill(self.tree_box_gr.tree.focus()))
        self.tree_box_gr.tree.bind('<Button-3>', self.box_gr_popup)
    def tree_box_gr_fill(self):                             #заполение фрейма_1
        self.tree_box_gr_drop()
        i = 0
        self.cur = conn.cursor()
        self.cur.execute("SELECT code, name FROM prod_gr ORDER BY name")
        self.box_gr_list = dict(self.cur.fetchall())
        for a in self.box_gr_list:
            self.tree_box_gr.tree.insert(parent = '', index = i, iid = a, values = (a, self.box_gr_list[a]))
            i += 1
        self.cur.close()
        try:
            self.info_gr.upd(values = list(self.box_gr_list.values()))
        except:
            pass
    def tree_box_gr_drop(self):
        self.tree_box_gr.tree.delete(*self.tree_box_gr.tree.get_children())
    def box_gr_popup(self, event):                          #вып. меню для д1
        self.chosed_box_gr = self.tree_box_gr.tree.identify_row(event.y)
        if self.chosed_box_gr:
            self.popup_menu.entryconfigure(0, state = ACTIVE)
            self.popup_menu.entryconfigure(1, state = ACTIVE)
            self.tree_box_gr.tree.selection_set(self.chosed_box_gr)
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.popup_menu.entryconfigure(0, state = DISABLED)
            self.popup_menu.entryconfigure(1, state = DISABLED)
            self.popup_menu.tk_popup(event.x_root, event.y_root)
    def add_box_gr(self, edit = None):                      #добавление через add_1 (группы)
        if self.add_box_gr_status == 1:
            return
        self.add_box_gr_w = Toplevel(self)
        self.add_box_gr_status = 1
        self.add_box_gr_w.resizable(0, 0)
        self.add_box_gr_value = StringVar()
        self.add_box_gr_note_value = StringVar()
        if edit:
            self.add_box_gr_w.title('Изменение группы')
            self.add_box_gr_value.set(self.box_gr_list[int(edit)])
            self.add_box_gr_ok = basic(self.add_box_gr_w, tk.Button, width = 10, text= "Изменить", command = lambda: self.add_box_gr_edit(self.add_box_gr_entry.new_wid.get(), edit))
            self.add_box_gr_w.bind('<Return>', lambda event:self.add_box_gr_edit(self.add_box_gr_entry.new_wid.get(), self.box_gr_list[int(edit)]))
        else:
            self.add_box_gr_w.title('Добавление группы')
            self.add_box_gr_value.set('')
            self.add_box_gr_ok = basic(self.add_box_gr_w, tk.Button, width = 10, text= "Добавить", command = lambda: self.add_box_gr_add(self.add_box_gr_entry.new_wid.get()))
            self.add_box_gr_w.bind('<Return>', lambda event:self.add_box_gr_add(self.add_box_gr_entry.new_wid.get()))
        self.add_box_gr_w.grab_set()
        self.add_box_gr_entry = basic(self.add_box_gr_w, tk.Entry, width = 30, textvariable = self.add_box_gr_value)
        self.add_box_gr_note = basic(self.add_box_gr_w, tk.Label, textvariable = self.add_box_gr_note_value)
        self.add_box_gr_cancel = basic(self.add_box_gr_w, tk.Button, width = 10, text = "Отмена", command = lambda: self.add_box_gr_close())
        self.add_box_gr_entry.grid(1, 1, 3, 1, N + S + W + E)
        self.add_box_gr_note.grid(1, 2, 3, 1, N + S + W + E)
        self.add_box_gr_cancel.grid(1, 3, 1, 1, N + S + W + E)
        self.add_box_gr_ok.grid(3, 3, 1, 1, N + S + W + E)
        self.add_box_gr_w.columnconfigure(0, minsize = 20)
        self.add_box_gr_w.columnconfigure(2, minsize = 60)
        self.add_box_gr_w.columnconfigure(4, minsize = 20)
        self.add_box_gr_w.rowconfigure(0, minsize=20)
        self.add_box_gr_w.rowconfigure(2, minsize=20)
        self.add_box_gr_w.rowconfigure(4, minsize=20)
        self.add_box_gr_w.protocol("WM_DELETE_WINDOW", self.add_box_gr_close)
    def add_box_gr_close(self):                             #закрытие окна добавления+
        self.add_box_gr_status = 0
        self.add_box_gr_w.grab_release()
        self.add_box_gr_w.destroy()
    def del_box_gr(self, target):                           #удаление из д1+
        print(target)
        self.del_check1 = messagebox.askokcancel(title = 'Удаление группы', parent = self, message = 'Удалить группу {}? Все вложенные записи будут перемещены в "Без группы"'.\
            format(self.box_gr_list[int(target)]), icon = messagebox.WARNING)
        if self.del_check1 == TRUE:
            self.cur = conn.cursor()
            try:
                self.cur.execute("DELETE FROM prod_gr WHERE code = {}".format(target))
                self.cur.close()
                self.status_bar.upd(text = "Удалена группа {}".format((self.box_gr_list[int(target)])))
                self.tree_box_gr_fill()
            except:
                self.status_bar.upd(text = "Ошибка удаления группы {}".format((self.box_gr_list[int(target)])))
    def add_box_gr_add(self, target):                       #добавление строки д1+
        self.cur = conn.cursor()
        try:
            self.cur.execute("INSERT INTO prod_gr(name) VALUES ('{}')".format(target))
            self.cur.close()
            self.status_bar.upd(text = "Добавлена группа {}".format(target))
            self.tree_box_gr_fill()
        except:
            self.status_bar.upd(text = "Ошибка добавления группы {}".format(target))
    def add_box_gr_edit(self, edited, target):              #изменение строки д1+
        if self.box_gr_list[int(target)] == edited:
            self.add_box_gr_note_value.set('Имя не изменилось!')
            return
        elif edited == '':
            self.add_box_gr_note_value.set('Имя не может быть пустым!')
            return
        try:
            self.cur = conn.cursor()
            self.cur.execute("UPDATE prod_gr SET name = '{}' where code = {}".format(edited, target))
            self.cur.close()
            self.status_bar.upd(text = "Группа {} переименована в {}".format(self.box_gr_list[int(target)], edited))
            self.tree_box_gr_fill()
            self.add_box_gr_close()
            self.add_box_gr(target)
        except:
            self.status_bar.upd(text = "Ошибка изменения группы {}".format(self.box_gr_list[int(target)]))
    def frame_box_fill(self, frame):                        #виджеты фрейма_2 (корпуса)
        self.tree_box = trees(frame.new_wid, columns = ("Code", "Name"), displaycolumns = ("Name") , height = 30)
        self.tree_box.size(1, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO)
        self.popup_box_menu = Menu(self, tearoff = 0)
        self.popup_box_menu.add_command(label = "Удалить", command = lambda: self.del_box(self.chosed_box))
        self.popup_box_menu.add_command(label = "Изменить", command = lambda: self.add_box(self.chosed_box))
        self.popup_box_menu.add_command(label = "Добавить", command = lambda: self.add_box())
        self.tree_box.grid(0, 0, 1, 1, N + S + W + E)
        self.tree_box.tree.bind('<Button-3>', self.box_popup)
        self.tree_box.tree.bind('<ButtonRelease-1>', lambda event: self.box_info_fill(self.tree_box.tree.focus(), self.box_gr_opened))
    def tree_box_fill(self, group):                         #заполнение фрейма_2
        #if self.box_gr_opened == group:
        #    return
        #self.box_gr_opened = group
        self.tree_box_fill_drop()
        i = 0
        self.cur = conn.cursor()
        self.cur.execute("SELECT code, name FROM prod_box WHERE code_gr = {} ORDER BY name".format(int(group)))
        print("SELECT code, name FROM prod_box WHERE code_gr = {} ORDER BY name".format(int(group)))
        self.box_list = dict(self.cur.fetchall())
        for a in self.box_list:
            self.tree_box.tree.insert(parent = '', index = i, iid = a, values = (a, self.box_list[a]))
            i += 1
        self.cur.close()
    def tree_box_fill_drop(self):
        self.tree_box.tree.delete(*self.tree_box.tree.get_children())
    def box_popup(self, event):                             #выпадающее меню фрейма_2
        self.chosed_box = self.tree_box.tree.identify_row(event.y)
        if self.chosed_box:
            self.popup_box_menu.entryconfigure(0, state = ACTIVE)
            self.popup_box_menu.entryconfigure(1, state = ACTIVE)
            self.tree_box.tree.selection_set(self.chosed_box)
            self.popup_box_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.popup_box_menu.entryconfigure(0, state = DISABLED)
            self.popup_box_menu.entryconfigure(1, state = DISABLED)
            self.popup_box_menu.tk_popup(event.x_root, event.y_root)
    def frame_box_info_fill(self, frame):                   #виджеты фрейма_3 (информация)
        self.info_changed_status = 0
        self.frame_info_gr = basic(frame.new_wid, tk.Labelframe, text = "Группа:")
        self.info_gr = basic(self.frame_info_gr.new_wid, tk.Combobox, state = 'readonly', values = list(self.box_gr_list.keys()))
        self.frame_info_name = basic(frame.new_wid, tk.Labelframe, text = "Название:")
        self.info_name_value = StringVar()
        self.info_name = basic(self.frame_info_name.new_wid, tk.Entry, textvariable = self.info_name_value)
        self.frame_info_size = basic(frame.new_wid, tk.Labelframe, text = "Размер:")
        self.info_size_value = StringVar()
        self.info_size = basic(self.frame_info_size.new_wid, tk.Entry, textvariable = self.info_size_value)
        self.frame_info_note = basic(frame.new_wid, tk.Labelframe, text = "Описание:")
        self.info_note = basic(self.frame_info_note.new_wid, Text, height = 3, width = 35)
        self.info_gr.grid(0, 0, 1, 1)
        self.info_name.grid(0, 0, 1, 1)
        self.info_size.grid(0, 0, 1, 1)
        self.info_note.grid(0, 0, 1, 1)
        self.frame_info_gr.grid(0, 0, 1, 1)
        self.frame_info_name.grid(1, 0, 1, 1)
        self.frame_info_size.grid(1, 1, 1, 1)
        self.frame_info_note.grid(0, 2, 2, 1)
    #def info_changed(self, *args):
    #    print(*args)
    #    print(self.info_name_value.get())
    #    pisya = tk.Style()
    #    if self.info_changed_status == 0:
    #        pisya.configure('Red.TEntry', foreground = 'red')
    #    self.info_changed_status = 1
    #    self.info_name.new_wid.configure(style = "Red.TEntry")
    def box_info_fill(self, box, box_gr):                   #заполение фрейма_3
        print(box, box_gr)
        #if box == '':
        #    return
        #if box[-1] == '}' and box[0] == '{':
        #    box = (box[:-1])[1:]
        #if box_gr[-1] == '}' and box_gr[0] == '{':
        #    box_gr = (box_gr[:-1])[1:]
        #self.cur = conn.cursor()
        #self.cur.execute("SELECT size, notes, price, code FROM prod_box WHERE name = '{}' AND group_name = '{}'".format(box, box_gr))
        #self.box_info = self.cur.fetchall()
        #self.cur.close()
        #self.info[1] = box
        #self.info[0] = box_gr
        #self.info = [box_gr, box, self.box_info[0][0], self.box_info[0][1]]
        #print(self.info)
        #self.info_gr.new_wid.set(box_gr)
        #self.info_name_value.set(box)
        #self.info_name_value.trace_add("write", self.info_changed)
        #try:
        #    self.info_size_value.set(self.box_info[0][0])
        #except:
        #    pass
        #self.info_size_value.trace_add("write", self.info_changed)
        #self.info_note.new_wid.delete('1.0', "end")
        #try:
        #    self.info_note.new_wid.insert('1.0', self.box_info[0][1])
        #except:
        #    pass
        #self.tree_box_det_fill()
    def frame_box_det_fill(self, frame):                    #виджеты фрейма_4 (детали)
        self.detail_list = trees(frame.new_wid, columns = ("№", "Name", "Mat", "Weight", "S1", "S2", "S3", "Notes", "Num"), \
            displaycolumns = ("№", "Name", "Mat", "Weight", "S1", "S2", "S3", "Notes", "Num"))
        self.detail_list.size(9, text_1 = "№", width_1 = 30, minwidth_1 = 30, stretch_1 = NO, text_2 = "Название", width_2 = 150, minwidth_2 = 150, \
            stretch_2 = NO, text_3 = "Материал", width_3 = 150, minwidth_3 = 150, stretch = NO, text_4 = "Вес", width_4 = 40, minwidth_4 = 40, \
                stretch_4 = NO, text_5 = "S1", width_5 = 40, minwidth_5 = 40, stretch_5 = NO, text_6 = "S2", width_6 = 40, minwidth_6 = 40, \
                    stretch_6 = NO, text_7 = "S3", width_7 = 40, minwidth_7 = 40, stretch_7 = NO, text_8 = "Примечание", width_8 = 250, minwidth_8 = 250, \
                        stretch_8 = NO, text_9 = "Кол-во", width_9 = 60, minwidth_9 = 60, stretch_9 = NO)
        self.detail_list.tree.bind('<Double-Button-1>', lambda event: self.change_field(event))
        self.detail_list.grid(0, 0, 1, 1)
    def tree_box_det_fill(self):
        self.cur = conn.cursor()
        self.cur.execute("SELECT name, material, weight, s_primer, s_enamel, s_powderpaint, notes, num FROM product_detail WHERE box_name = {} ORDER BY material, name".format("\'" + \
            self.info[0] + "/" + self.info[1] + "\'"))
        self.test = self.cur.fetchall()
        self.cur.close()
        self.frame_box_det_drop()
        i = 1
        for a, b, c, d, e, f, g, h in self.test:
            self.detail_list.tree.insert(parent = '', index = i, iid = i, values = (i, a, b, c, d, e, f, g, h))
            i += 1
            print(a)
    def change_field(self, event):                          #создание окна изменения детали
        row = self.detail_list.tree.identify_row(event.y)
        col = self.detail_list.tree.identify_column(event.x)
        if row == '':
            return
        x, y, width, height = self.detail_list.tree.bbox(row, col)
        text = self.detail_list.tree.item(row, 'values')
        print(int(''.join(c for c in col if c.isdigit())))
        print(text)
        coltoprint = int(''.join(c for c in col if c.isdigit())) - 1
        self.entry_popup = TreeEntry(self.detail_list.tree, row, col, text[coltoprint])
        self.entry_popup.place (x = x, y = y + height // 2, anchor = W, width = width, height = height)
    def frame_box_det_drop(self):
        self.detail_list.tree.delete(*self.detail_list.tree.get_children())
    def frame_box_mat_fill(self, frame):                    #виджеты фрейма_5 (материалы) UNDONE
        pass   
    def frame_box_status_fill(self, frame):                 #виджеты фрейма_статус
        self.status_bar = basic(frame.new_wid, Label, text = "-")
        self.status_bar.grid(0, 0, 1, 1, N + S + W + E)   
    def reopen(self):                                       #открытие окна материалов по нажатию кнопки в главном окне
        if self.status == -1:
            self.tree_box_gr_fill()
            self.status_bar.upd(text = "-")
        self.open()

class change_mat_gr_w(wind):
    def __init__(self, parent, **sets):
        self.change_w = wind.__init__(self,parent, **sets)
    def reopen(self, type, to_change=''):
        self.choose_type(type, to_change)
        self.open()
    def choose_type(self, type, to_change):
        if type == 'add':
            self.add_fields()
        elif type == 'change':
            self.change_fields(to_change)
        else:
            print("В вызове редактирования материалов что-то не так!!")

class change_mat(wind):
    def __init__(self, parent, **sets):
        self.change_w = wind.__init__(self,parent, **sets)
        self.add_fields()

class change_box_w(wind):
    def __init__(self, parent, **sets):
        self.change_w = wind.__init__(self,parent, **sets)
        self.add_fields()
    def reopen(self, to_add):
        self.open()

def _onKeyRelease(event):                                   #добавление эвентов на русской раскладке (ctrl+a, ctrl+v, ctrl+x, ctrl+c)
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")
    if event.keycode==86 and ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")
    if event.keycode==67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
    if event.keycode==65 and ctrl and event.keysym.lower() != "a": 
        event.widget.event_generate("<<SelectAll>>")

programm = Tk()
programm.bind_all("<Key>", _onKeyRelease, "+")
main_w = main(programm)
programm.mainloop()