from tkinter import *
import tkinter.ttk as tk
from psycopg2 import *

global conn, status_now
conn = ()
status_now = 0

class basic(Widget):
    def __init__(self, parent, w_type, **sets):     #создание класса виджетов
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
    def remove(self):       #скрытие виджетов
        self.new_wid.grid_remove()
        self.status = 2
    def upd(self, **sets):      #обновление виджетов
        for a, b in sets.items():
            self.new_wid[a] = b

class trees(tk.Treeview):
    def __init__(self, parent, **sets):     #создание класса дерева
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
    def size(self, col_n, **sets):      #определение колонок дерева
        a = 0
        while a <= col_n:
                self.tree.heading("#{}".format(a), text = sets.get("text_{}".format(a), ""))
                self.tree.column("#{}".format(a), minwidth = sets.get("minwidth_{}".format(a), 0), width = sets.get("width_{}".format(a), 100), \
                        stretch = sets.get("stretch_{}".format(a,), "YES"))
                a += 1
    def remove(self):       #скрытие дерева
        self.tree.grid_remove()
        self.status = -1

class wind(Tk):
    def __init__(self, parent = None, **sets):      #создание класса окон
        Toplevel.__init__(self, parent)
        self.title(sets.get('text', ""))
        self.withdraw()
        self.status = 0
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", sets.get("close", self.closing))
    def closing(self):      #процесс закрытия окон по нажатию х
        self.status = 0
        self.withdraw()
    def open(self):     #процесс открытия окон при нажатии кнопки в главном окне
        if self.status == 1:
            return
        self.status = 1
        self.deiconify()
    def table(self, *sets):     #верстка окна
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
    def __init__(self, root):       #инициализация главного окна
        root.title("База данных цен")
        root.geometry('590x220+{}+{}'.format((root.winfo_screenwidth() // 2 - 300), (root.winfo_screenheight() // 2 - 100)))
        #root.protocol("WN_DELETE_WINDOW")
        self.mat_w = mat_w(root, text = "Материалы")
        self.box_w = wind(root, text = "Корпуса")
        self.sch_w = wind(root, text = "Схемы")
        self.auth_w = auth_w(root, text = "Авторизация", close = lambda: root.destroy())
        self.sett_w = wind(root, text = "Настройки")
        wind.table(root, "r", 0, 20, "r", 1, 30, "r", 2, 20, "c", 0, 20, "c", 1, 50, "c", 2, 20, "c", 3, 50, "c", 4, 20, "c", 5, 50, "c", 6, 20)
        self.mat_w_open = basic(root, Button, text = "Материалы", command = lambda: self.mat_w.reopen(), width = 10)
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
    def __init__(self, parent, **sets):     #инициализация окна авторизации
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
    def try_auth(self):     #процесс авторизации
        global conn, status_now
        self.login = self.entry_log.new_wid.get()
        self.passw = self.entry_pass.new_wid.get()
        try:
            conn = connect(dbname = "Prices", user = self.login, password = self.passw, port = "5432")
            status_now = 1
            main.status.upd(text = "Connected as {}".format(self.login))
            self.grab_release()
            self.check_conn()
            self.closing()
        except:
            self.status = "Неверный логин/пароль"
            self.note.upd(text = self.status)
    def check_conn(self):       #постоянная проверка наличия соединения
        global conn, status_now
        try:
            self.cur = conn.cursor()
            self.cur.execute("SELECT")
            self.cur.close()
            status_now = 1
            main.status.upd(text = "Connected as {}".format(self.login))
        except:
            status_now = 0
            main.status.upd(text = "Disconnected by server")
            self.open()
            self.grab_set()
        self.after(10000, self.check_conn)
        
class mat_w(wind):
    def __init__(self, parent, **sets):     #инициализация окна материалов
        self.mat_w = wind.__init__(self, parent, **sets)
        self.tree_m_gr = trees(self, columns = "Name")
        self.tree_m_u = trees(self, columns = ("Name", "Price", "Date"))
        self.tree_m_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.tree_m_u.size(3, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO, \
            text_2 = "Цена", width_2 = 80, minwidth_2 = 80, stretch_2 = NO, \
                text_3 = "Дата", width_3 = 80, minwidth_3 = 80, stretch_3 = NO)
        self.tree_m_gr.grid(0, 1, 2, 1, N + S + W + E)
        self.tree_m_u.grid(3, 1, 5, 1, N + S + W + E)
        self.tree_m_gr.tree.bind('<ButtonRelease-1>', lambda event: self.fill_unit(self.tree_m_gr.tree.focus()))
    def add_fields_gr(self):     #создание полей добавления групп
        self.entry_m_gr = basic(self, Entry)
        self.button_m_gr = basic(self, Button, text = "+")
        self.entry_m_gr.grid(0, 2, 1, 1)
        self.button_m_gr.grid(1, 2, 1, 1, N + S + W + E)
    def add_fields_u(self):     #создание полей добавление материалов
        self.m_gr = [a[0] for a in self.m_gr]
        self.entry_m_u_gr = basic(self, tk.Combobox, values = self.m_gr, width = 22, state = 'readonly')
        self.entry_m_u_gr.new_wid.current(0)
        self.entry_m_u_name = basic(self, Entry)
        self.entry_m_u_price = basic(self, Entry)
        self.entry_m_u_measure = basic(self, tk.Combobox, values = ['шт', 'кг', 'л'], width = 5, state = 'readonly')
        self.entry_m_u_measure.new_wid.current(0)
        self.button_m_u = basic(self, Button, text = "+")
        self.entry_m_u_gr.grid(3, 2, 1, 1)
        self.entry_m_u_name.grid(4, 2, 1, 1)
        self.entry_m_u_price.grid(5, 2, 1, 1)
        self.entry_m_u_measure.grid(6, 2, 1, 1)
        self.button_m_u.grid(7, 2, 1, 1)
    def fill(self):     #заполнение дерева группы материалов
        self.tree_m_gr.tree.delete(*self.tree_m_gr.tree.get_children())
        self.tree_m_gr.tree.insert(parent = '', iid = "Все", index = 0, values = "Все")
        i = 1
        self.cur = conn.cursor()
        self.cur.execute("SELECT name FROM material_group ORDER BY name;")
        self.m_gr = self.cur.fetchall()
        print(self.m_gr)
        for a in self.m_gr:
            self.tree_m_gr.tree.insert(parent = '', iid = a, index = i, values = a)
            i += 1
        self.cur.close()
    def fill_unit(self, group):     #заполнение дерева материалов
        self.tree_m_u.tree.delete(*self.tree_m_u.tree.get_children())
        i = 0
        self.cur = conn.cursor()
        #if group.find('{') != -1:   #удаление символов { и }, если название группы состоит из нескольких слов
        #    group = group.replace('{', '')
        #    group = group.replace('}', '')
        print(group)
        if group == "Все":
            self.cur.execute("SELECT №, name, price FROM material_unit ORDER BY name")
        else:
            self.cur.execute("SELECT №, name, price FROM material_unit WHERE group_name = %s ORDER BY name", (group,))
        self.m_u = self.cur.fetchall()
        for a, b, c in self.m_u:
            self.tree_m_u.tree.insert(parent = '', index = i, iid = a, values = (b, c))
            i += 1
        self.cur.close()
    def reopen(self):   #открытие окна материалов по нажатию кнопки в главном окне
        self.open()
        self.fill()
        self.add_fields_gr()
        self.add_fields_u()

#def connection():
#    global conn, status

main_w = Tk()
main = programm(main_w)
main_w.mainloop()
