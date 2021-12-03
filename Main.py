from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk
from psycopg2 import *
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

class main:
    def __init__(self, root):                               #инициализация + виджеты
        root.title("База данных цен")
        root.geometry('590x220+{}+{}'.format((root.winfo_screenwidth() // 2 - 300), (root.winfo_screenheight() // 2 - 100)))
        root.protocol("WN_DELETE_WINDOW", self.close)
        self.mat = mat(root, text = "Материалы", close = lambda: mat.close(self.mat))
        self.box_w = box_w(root, text = "Корпуса")
        self.sch_w = wind(root, text = "Схемы")
        self.auth_w = auth(root, text = "Авторизация", close = lambda: root.destroy())
        self.sett_w = wind(root, text = "Настройки")
        wind.table(root, "r", 0, 20, "r", 1, 30, "r", 2, 20, "c", 0, 20, "c", 1, 50, "c", 2, 20, "c", 3, 50, "c", 4, 20, "c", 5, 50, "c", 6, 20)
        self.mat_open = basic(root, Button, text = "Материалы", command = lambda: self.mat.reopen(), width = 10)
        self.mat_open.grid(1, 1, 1, 1, N + S + W + E)
        self.box_w_open = basic(root, Button, text = "Корпуса", command = lambda: self.box_w.reopen(), width = 10)
        self.box_w_open.grid(3, 1, 1, 1, N + S + W + E)
        self.sch_w_open = basic(root, Button, text = "Схемы", command = lambda: self.sch_w.open(), width = 10)
        self.sch_w_open.grid(5, 1, 1, 1, N + S + W + E)
        self.setts = basic(root, Button, bitmap = 'gray12', command = lambda: self.sett_w.open())
        self.setts.grid(0, 3, 1, 1, N + S + W + E)
        self.status = basic(root, Label, text = "Not connected...", bg = 'grey')
        self.status.grid(1, 3, 7, 1, N + S + W + E)
    def close(self):                                        #закртыие соединения при закрытии окна
        if (conn):
            conn.close()
        programm.destroy()

class auth(wind):
    def __init__(self, parent, **sets):                     #инициализация + виджеты
        self.auth_w = wind.__init__(self, parent, **sets)
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
            conn = connect(dbname = "Prices", user = self.login, password = self.passw, port = "5432")
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
        except:
            connection_status = 0
            main_w.status.upd(text = "Disconnected by server")
            self.open()
            self.grab_set()
        self.after(10000, self.check)
        
class mat(wind):
    def __init__(self, parent, **sets):                     #инициализация
        self.mat = wind.__init__(self, parent, **sets)
        self.var()
        self.wid()
    def var(self):                                          #переменные (UND)
        self.f1_wind_status = 0
        self.f2_wind_status = 0
    def wid(self):                                          #виджеты
        self.f1 = trees(self, columns = "Name", height = 20)
        self.f2 = trees(self, columns = ("Name", "Price", "Meas", "Prod", "Date"))
        self.f1.size(1, text_1 = "Название группы", width_1 = 220, minwidth_1 = 220, stretch_1 = NO)
        self.f2.size(5, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO, \
            text_2 = "Цена", width_2 = 80, minwidth_2 = 80, stretch_2 = NO, \
                text_3 = "Ед", width_3 = 30, minwidth_3 = 80, stretch_3 = NO, \
                    text_4 = "Произв.", width_4 = 80, minwidth_4 = 80, stretch_4 = NO, \
                        text_5 = "Дата", width_5 = 80, minwidth_5 = 80, stretch_5 = NO)
        self.status_separ = basic(self, tk.Separator, orient = HORIZONTAL)
        self.status_bar = basic(self, Label, text = "-")
        self.f1_menu()
        self.f2_menu()
        self.f2_menu_empty()
        self.f1.grid(0, 1, 1, 1, N + S + W + E)
        self.f2.grid(2, 1, 1, 1, N + S + W + E)
        self.status_separ.grid(0, 2, 4, 1, N + S + W + E)
        self.status_bar.grid(0, 2, 4, 1, N + S + W + E)
        #self.f1.tree.bind('<ButtonRelease-1>', lambda event: self.f2_fill(self.f1.tree.focus()))
        self.f1.tree.bind('<ButtonRelease-1>', self.f2_fill)
    def f1_fill(self):                                      #заполнение Д1
        self.f1_drop()
        self.f1.tree.insert(parent = '', iid = "Все", index = 0, values = "Все")
        i = 1
        self.cur = conn.cursor()
        self.cur.execute("SELECT name FROM material_group ORDER BY name;")
        self.m_gr = self.cur.fetchall()
        for a in self.m_gr:
            self.f1.tree.insert(parent = '', iid = a, index = i, values = a)
            i += 1
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
        print(x, y)
        self.f1_wind.geometry('+%d+%d' % (x, y))
        self.f1_wind_status = 1
        if target:
            self.f1_wind.title("Изменение группы")
        else:
            self.f1_wind.title("Добавление группы")
        self.f1_wind.resizable(0, 0)
        self.f1_wind.grab_set()
        if target:    
            if len(target) > 2:
                if target[-1] == '}' and target [0] == '{':
                    target = (target[:-1])[1:]
        self.target = StringVar()
        self.target.set(target)
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
            self.cur.execute("INSERT INTO material_group(name) VALUES ('{}')".format(target))
            self.cur.close()
            self.status_bar.upd(text = "Добавлена группа {}".format(target))
            self.f1_fill()
        except:
            self.status_bar.upd(text = "Ошибка добавления группы {}".format(target))
    def f1_change(self, target, old):                       #изменение в Д1
        if not target:
            self.status_bar.upd(text = "Поле не может быть пустым")
            return
        if len(target) > 2:
            if target[-1] == '}' and target[0] == '{':
                target = (target[:-1])[1:]
        try:
            self.cur = conn.cursor()
            self.cur.execute("UPDATE material_group SET name = '{new}' WHERE name = '{old}'".format(new = target, old = old))
            self.cur.close()
            self.status_bar.upd(text = "Группа {old} переименована в {new}".format(old = old, new = target))
            self.f1_fill()
            self.f1_wind_close()
            self.f1_wind_open(target)
        except:
            self.status_bar.upd(text = "Ошибка изменения группы {}".format(old))
    def f1_del(self, target):                               #удаление в Д1 (UND)
        if len(target) > 2:
            if target[-1] == '}' and target[0] == '{':
                target = (target[:-1])[1:]
        self.f1_del_check = messagebox.askokcancel(title = "Удаление группы", \
            parent = self, message = \
                "Удалить группу {}? Все вложенные записи будут перемещены в \"Без группы\""\
                    .format(target), icon = messagebox.WARNING)
        if self.f1_del_check == TRUE:
            try:
                self.cur = conn.cursor()
                self.cur.execute("DELETE FROM material_group WHERE name = '{}'".format(target))
                self.cur.close()
                self.status_bar.upd(text = "Удалена группа {}".format(target))
                self.f1_fill()
            except:
                self.status_bar.upd(text = "Ошибка удаления группы {}".format(target))
    def f2_fill(self, event = None):                               #заполнение Д2
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
        if len(target) > 2:
            if target[-1] == '}' and target[0] == '{':
                target = (target[:-1])[1:]
        self.f2_grouptofill = target
        self.f2_drop()
        i = 0
        self.cur = conn.cursor()
        if target == "Все":
            self.cur.execute("SELECT №, name, price, measure, producer, upddate FROM material_unit ORDER BY name")
        else:
            self.cur.execute("SELECT №, name, price, measure, producer, upddate FROM material_unit WHERE group_name = %s ORDER BY name", (target,))
        self.m_u = self.cur.fetchall()
        for a, b, c, d, e, f in self.m_u:
            self.f2.tree.insert(parent = '', index = i, iid = a, values = (b, c, d, e, f))
            i += 1
        self.cur.close()
    def f2_drop(self):                                      #очистка Д2
        self.f2.tree.delete(*self.f2.tree.get_children())
    def f2_menu(self):                                      #выпадающее меню для Д2 (UND)
        self.f2_popup = Menu(self, tearoff = 0)
        self.f2_popup.add_command(label = "Удалить", command = lambda: self.f2_del(self.f2_target))
        self.f2_popup.add_command(label = "Изменить", command = lambda: self.f2_wind_open(self.f2_target))
        self.f2_popup.add_command(label = "Добавить", command = lambda: self.f2_wind_open())
        self.f2.tree.bind('<Button-3>', self.f2_menu_open)
    def f2_menu_empty(self):
        self.f2_popup_empty = Menu(self, tearoff = 0)
        self.f2_popup_empty.add_command(label = "Добавить", command = lambda: self.f2_wind_open())
        self.f2.tree.bind('<Button-3>', self.f2_menu_open)
    def f2_menu_open(self, event):                          #открытие меню для Д2 (UND)
        self.f2_target = self.f2.tree.identify_row(event.y)
        if self.f2_target:
            self.f2.tree.selection_set(self.f2_target)
            #print(self.f2.tree.item(self.f2_target).get('values'))
            #print(date.today().strftime('%Y-%m-%d'))
            self.f2_popup.tk_popup(event.x_root, event.y_root)
        else:
            self.f2_popup_empty.tk_popup(event.x_root, event.y_root)
    def f2_wind_open(self, target = ''):                    #открытие окна добавления в Д2 (UND)
        if self.f2_wind_status == 1:
            return
        self.f2_wind = Toplevel(self)
        x = programm.winfo_screenwidth()/2
        y = programm.winfo_screenheight()/2
        self.f2_wind.geometry('+%d+%d' % (x, y))
        self.f2_wind_status = 1
        if target:
            target = self.f2.tree.item(self.f2_target).get('values')
            self.f2_wind.title("Изменение материала")
            self.f2_wind_ok = basic(self.f2_wind, tk.Button, width = 10, text = "Изменить", command = lambda: self.f2_change(target))
        else:
            target = [[],[],[],[],[]]
            self.f2_wind.title("Добавление материала")
            self.f2_wind_ok = basic(self.f2_wind, tk.Button, width = 10, text = "Добавить", command = lambda: self.f2_add())
        self.f2_wind.resizable(0, 0)
        self.f2_wind.grab_set()
        #if target:    
        #    if len(target) > 2:
        #        if target[-1] == '}' and target [0] == '{':
        #            target = (target[:-1])[1:]
        i = 0
        self.target_group_choose = self.m_gr.copy()
        print(self.m_gr)
        for a in self.target_group_choose:
            self.target_group_choose[i] = self.target_group_choose[i][0]
            i += 1
        self.wind_status_text = StringVar()
        self.wind_status_text.set('Изменение элемента')
        self.target_name = StringVar()
        self.target_name.set(target[0])
        self.target_price = StringVar()
        self.target_price.set(target[1])
        self.target_meas = StringVar()
        self.target_meas.set(target[2])
        self.target_prod = StringVar()
        self.target_prod.set(target[3])
        self.target_group = StringVar()
        try:
            self.target_group.set(self.f2_grouptofill)
        except:
            pass
        self.f2_wind_status_text = basic(self.f2_wind, tk.Label, textvariable = self.wind_status_text)
        self.f2_wind_frame_name = basic(self.f2_wind, tk.Labelframe, text = "Название:")
        self.f2_wind_name = basic(self.f2_wind_frame_name.new_wid, tk.Entry, width = 50, textvariable = self.target_name)
        self.f2_wind_frame_price = basic(self.f2_wind, tk.Labelframe, text = "Цена:")
        self.f2_wind_price_validate = (self.register(self.f2_wind_validate), '%P')
        self.f2_wind_price = basic(self.f2_wind_frame_price.new_wid, tk.Entry, width = 15, validate = 'key', validatecommand = self.f2_wind_price_validate, \
            textvariable = self.target_price)
        self.f2_wind_frame_meas = basic(self.f2_wind, tk.Labelframe, text = "Изм.:")
        self.f2_wind_meas = basic(self.f2_wind_frame_meas.new_wid, tk.Combobox, width = 8, state = 'readonly', textvariable = self.target_meas, \
            values = ["кг", "м", "м2", "м3", "л"])
        self.f2_wind_frame_prod = basic(self.f2_wind, tk.Labelframe, text = "Производитель:")
        self.f2_wind_prod = basic(self.f2_wind_frame_prod.new_wid, tk.Entry, width = 20, textvariable = self.target_prod)
        self.f2_wind_frame_group = basic(self.f2_wind, tk.Labelframe, text = "Группа:")
        self.f2_wind_group = basic(self.f2_wind_frame_group.new_wid, tk.Combobox, width = 30, state = 'readonly', textvariable = self.target_group, \
            values = self.target_group_choose)
        self.f2_wind_cancel = basic(self.f2_wind, tk.Button, width = 10, text = "Отмена", command = lambda: self.f2_wind_close())
        self.f2_wind_status_text.grid(1, 1, 6, 1)
        self.f2_wind_frame_name.grid(1, 2, 3, 1)
        self.f2_wind_name.grid(0, 0, 1, 1)
        self.f2_wind_frame_price.grid(4, 2, 1, 1)
        self.f2_wind_price.grid(0, 0, 1, 1)
        self.f2_wind_frame_meas.grid(5, 2, 1, 1)
        self.f2_wind_meas.grid(0, 0, 3, 1)
        self.f2_wind_frame_prod.grid(3, 3, 1, 1)
        self.f2_wind_prod.grid(0, 0, 3, 1)
        self.f2_wind_frame_group.grid(4, 3, 1, 1)
        self.f2_wind_group.grid(0, 0, 3, 1)
        self.f2_wind_cancel.grid(1, 5, 1, 1)
        self.f2_wind_ok.grid(5, 5, 1, 1)
        self.f2_wind.columnconfigure(0, minsize = 20)
        self.f2_wind.columnconfigure(6, minsize = 20)
        self.f2_wind.rowconfigure(0, minsize = 20)
        self.f2_wind.rowconfigure(3, minsize = 20)
        self.f2_wind.rowconfigure(5, minsize = 20)
        self.f2_wind.protocol("WM_DELETE_WINDOW", self.f2_wind_close)
    def f2_wind_validate(self, value):
        if value:
            try:
                float(value)
                self.wind_status_text.set('ne suka')
                return True
            except ValueError:
                self.wind_status_text.set('suka')
                return False
        else:
            self.wind_status_text.set('pusto suka')
            return True
    def f2_wind_close(self):                                #закрытие окна добавления в Д2 (UND)
        self.f2_wind_status = 0
        self.f2_wind.grab_release()
        self.f2_wind.destroy()
    def f2_add(self):                               #добавление в Д2 (UND)
        try:
            if not self.target_price.get():
                self.target_price.set(0)
            self.cur = conn.cursor()
            self.cur.execute("INSERT INTO material_unit(name, group_name, price, measure, producer, upddate) VALUES \
                ('{name}', '{gr_name}', {price}, '{meas}', '{prod}', '{upddate}')".format(name = self.target_name.get(), \
                    gr_name = self.target_group.get(), price = self.target_price.get(), meas = self.target_meas.get(), \
                        prod = self.target_prod.get(), upddate = date.today().strftime('%Y-%m-%d')))
            self.cur.close()
            self.status_bar.upd(text = "Добавлен материал {}".format(self.target_name.get()))
            self.f2_fill()
            self.f2_wind_close()
            self.f2_wind_open()
        except:
            self.status_bar.upd(text = "Ошибка добавления группы {}".format(self.target_name.get()))
    def f2_change(self, target, old):                       #изменение в Д2 (UND)
        pass
    def f2_del(self, target):                               #удаление в Д2 (UND)
        print(target)
        if target:
            target = self.f2.tree.item(self.f2_target).get('values')
        print(target)

    # def add_gr_write(self):                                 #добавление группы
    #     self.to_add_gr = self.entry_m_gr.new_wid.get()
    #     self.cur = conn.cursor()
    #     try:
    #         self.cur.execute("INSERT INTO material_group(name) VALUES (%s)", (self.to_add_gr,))
    #         self.status_bar.upd(text = "Новая группа добавлена")
    #     except:
    #         self.status_bar.upd(text = "Ошибка записи новой группы")
    #     self.cur.close()
    #     self.f1_fill()
    #     self.entry_m_u_gr.upd(values = self.m_gr)
    # def edit_gr(self, group):                               #изменение/удаление группы
    #     if self.fields_gr_status == 'Edit':
    #         self.edit_gr_close()
    #     self.entry_m_gr.new_wid.delete(0, "end")
    #     self.entry_m_gr.new_wid.insert(0, group)
    #     self.button_m_gr.upd(text = "Upd", command = lambda: self.edit_gr_write(group)) 
    #     self.button_m_gr_del = basic(self, tk.Button, text = "DEL", width = 3, command = lambda: self.del_gr(group))
    #     self.button_m_gr_close_edit = basic(self, Button, text ="x", command = lambda: self.edit_gr_close())
    #     self.button_m_gr_close_edit.grid(0, 2, 1, 1)
    #     self.button_m_gr_del.grid(1, 2, 1, 1)
    #     self.fields_gr_status = 'Edit'
    # def edit_gr_write(self,group):                          #изменение группы - запись результата в бд
    #     self.to_upd_gr = self.entry_m_gr.new_wid.get()
    #     self.cur = conn.cursor()
    #     try:
    #         self.cur.execute("UPDATE material_group SET name = '{new_name}' where name = '{name}'".format(new_name = self.to_upd_gr, name = group))
    #         self.cur.close()
    #         self.status_bar.upd(text = "Группа {name} переименована в {new_name}".format(name = group, new_name = self.to_upd_gr))
    #         self.f1_fill()
    #         self.entry_m_u_gr.upd(values = self.m_gr)
    #         self.entry_m_gr.new_wid.delete(0, "end")
    #     except:
    #         self.status_bar.upd(text = "Ошибка изменения группы {}".format(group))
    # def del_gr(self, group):                                #удаление группы
    #     self.check_del_gr = messagebox.askokcancel(title = 'Удаление группы', parent = self, message = 'Удалить группу {}? Все вложенные записи будут перемещены в "Без группы"'.format(group), icon = messagebox.WARNING)
    #     if self.check_del_gr == TRUE:
    #         self.cur = conn.cursor()
    #         try:
    #             self.cur.execute("DELETE FROM material_group WHERE name = '{}'".format(group))
    #             self.cur.close()
    #             self.status_bar.upd(text = "Удалена группа {}".format(group))
    #             self.f1_fill()
    #             self.entry_m_u_gr.upd(values = self.m_gr)
    #             self.entry_m_gr.new_wid.delete(0, "end")
    #         except:
    #             self.status_bar.upd(text = "Ошибка удаления группы {}".format(group))
    # def edit_gr_close(self):                                #изменение группы - закрытие (открытие добавления группы)
    #     self.entry_m_gr.new_wid.delete(0, "end")
    #     self.button_m_gr.upd(text = "+", command = lambda: self.add_gr_write())
    #     self.button_m_gr_close_edit.new_wid.grid_forget()
    #     self.button_m_gr_del.new_wid.grid_forget()
    #     self.fields_gr_status = 'Add'
    # def add_u_write(self):                                  #добавление материала
    #     self.cur = conn.cursor()
    #     try:
    #         self.cur.execute("INSERT INTO material_unit(group_name, name, price, measure, producer) values('{group_name}', '{name}', {price}, '{meas}', '{prod}')"\
    #             .format(group_name = self.entry_m_u_gr.new_wid.get(), name = self.entry_m_u_name.new_wid.get(), price = self.entry_m_u_price.new_wid.get(), \
    #                 meas = self.entry_m_u_measure.new_wid.get(), prod = self.entry_m_u_producer.new_wid.get()))
    #         self.status_bar.upd(text = "Новый материал добавлен")
    #     except:
    #         self.status_bar.upd(text = "Ошибка добавления нового материала")
    #     self.cur.close()
    #     self.f2_fill(self.f1.tree.focus())
    # def edit_u(self, unit):                                 #изменение/удаление материала - сюда передается № выбранного материала
    #     if self.fields_u_status == 'Edit':
    #         self.edit_u_close()
    #     self.cur = conn.cursor()
    #     self.cur.execute("SELECT group_name, name, price, measure, producer, typical, upddate FROM material_unit WHERE № = {}".format(unit))
    #     self.u_to_edit = self.cur.fetchall()
    #     self.cur.close()
    #     self.entry_m_u_measure.new_wid.set(self.u_to_edit[0][3])
    #     self.entry_m_u_gr.new_wid.set(self.u_to_edit[0][0])
    #     self.entry_m_u_name.new_wid.delete(0, "end")
    #     self.entry_m_u_name.new_wid.insert(0, self.u_to_edit[0][1])
    #     self.entry_m_u_price.new_wid.delete(0, "end")
    #     self.entry_m_u_price.new_wid.insert(0, self.u_to_edit[0][2])
    #     self.entry_m_u_producer.new_wid.delete(0,"end")
    #     self.entry_m_u_producer.new_wid.insert(0,self.u_to_edit[0][4])
    #     self.button_m_u_del = basic(self, Button, text = "DEL", command = lambda: self.del_u(unit))
    #     self.button_m_u_close_edit = basic(self, Button, text = "x", command = lambda: self.edit_u_close())
    #     self.button_m_u_del.grid(6, 2, 1, 1)
    #     self.button_m_u_close_edit.grid(5, 2, 1, 1)
    #     self.button_m_u.upd(text = "Upd", command = lambda: self.edit_u_write(unit))
    #     self.fields_u_status = 'Edit'
    # def edit_u_write(self, unit):                           #изменение материала - запись результата в бд
    #     self.cur = conn.cursor()
    #     try:
    #         self.cur.execute("UPDATE material_unit SET group_name = '{group_name}', name = '{name}', price = {price}, producer = '{prod}', measure = '{meas}' WHERE № = {unit}"\
    #             .format(group_name = self.entry_m_u_gr.new_wid.get(), name = self.entry_m_u_name.new_wid.get(), price = self.entry_m_u_price.new_wid.get(), \
    #                 meas = self.entry_m_u_measure.new_wid.get(), prod = self.entry_m_u_producer.new_wid.get(), unit = unit))
    #         self.cur.close()
    #         self.status_bar.upd(text = "Материал {name} переименован".format(name = self.entry_m_u_name.new_wid.get()))
    #         self.f2_fill(self.f1.tree.focus())
    #         self.entry_m_u_producer.new_wid.delete(0, "end")
    #         self.entry_m_u_name.new_wid.delete(0, "end")
    #         self.entry_m_u_price.new_wid.delete(0, "end")
    #         self.entry_m_u_measure.new_wid.current(0)
    #         self.entry_m_u_gr.new_wid.current(0)
    #     except:
    #         self.status_bar.upd(text = "Ошибка изменения материала")
    # def del_u(self,unit):                                   #удаление материала 
    #     self.check_del_u = messagebox.askokcancel(title = 'Удаление материала', parent = self, message = 'Удалить материал?', icon = messagebox.WARNING)
    #     if self.check_del_u == TRUE:
    #         self.cur = conn.cursor()
    #         try:
    #             self.cur.execute("DELETE FROM material_unit WHERE № = {}".format(unit))
    #             self.cur.close()
    #             self.status_bar.upd(text = "Удален материал {}".format(unit))
    #             self.f2_fill(self.f1.tree.focus())
    #             self.entry_m_u_producer.new_wid.delete(0, "end")
    #             self.entry_m_u_name.new_wid.delete(0, "end")
    #             self.entry_m_u_price.new_wid.delete(0, "end")
    #             self.entry_m_u_measure.new_wid.current(0)
    #             self.entry_m_u_gr.new_wid.current(0)
    #         except:
    #             self.status_bar.upd(text = "Ошибка удаления материала {}".format(unit))
    # def edit_u_close(self):                                 #изменение материала - закрытие (открытие добавления материала)
    #     self.entry_m_u_name.new_wid.delete(0, "end")
    #     self.entry_m_u_price.new_wid.delete(0, "end")
    #     self.entry_m_u_producer.new_wid.delete(0,"end")
    #     self.entry_m_u_measure.new_wid.current(0)
    #     self.entry_m_u_gr.new_wid.current(0)
    #     self.button_m_u.upd(text = "+", command = lambda: self.add_u_write())
    #     self.button_m_u_del.new_wid.grid_forget()
    #     self.button_m_u_close_edit.new_wid.grid_forget()
    #     self.fields_u_status = 'Add'
    def reopen(self):                                       #открытие окна материалов по нажатию кнопки в главном окне
        self.open()
        self.f1_fill()
        self.status_bar.upd(text = "-")
    def close(self):                                        #доп. опции закрытия окна
        self.closing()

class box_w(wind):
    def __init__(self, parent, **sets):
        self.box_w = wind.__init__(self,parent, **sets)
        self.box_gr_opened = ''
        self.widgets_frame()
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
        self.tree_box_gr = trees(frame.new_wid, columns = "Name", height = 30)
        self.tree_box_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.butt_box_gr = basic(frame.new_wid, tk.Button, text = "Добавить", command = lambda: self.add_box_gr())
        self.popup_menu = Menu(self, tearoff = 0)
        self.popup_menu.add_command(label = "Удалить", command = lambda: self.del_box_gr(self.chosed))
        self.popup_menu.add_command(label = "Изменить", command = lambda: self.add_box_gr(self.chosed))
        self.popup_menu.add_command(label = "Добавить", command = lambda: self.add_box_gr())
        self.tree_box_gr.grid(0, 0, 1, 1, N + S + W + E)
        self.butt_box_gr.grid(0, 1, 1, 1, N + S + W + E)
        self.tree_box_gr.tree.bind('<ButtonRelease-1>', lambda event: self.tree_box_fill(self.tree_box_gr.tree.focus()))
        self.tree_box_gr.tree.bind('<Button-3>', self.box_gr_popup)
    def tree_box_gr_fill(self):                             #заполение фрейма_1
        self.tree_box_gr.tree.delete(*self.tree_box_gr.tree.get_children())
        i = 0
        self.cur = conn.cursor()
        self.cur.execute("SELECT name FROM product_group ORDER BY name")
        self.box_gr = self.cur.fetchall()
        for a in self.box_gr:
            self.tree_box_gr.tree.insert(parent = '', index = i, iid = a, values = (a[0], ))
            i += 1
        self.cur.close()
    def box_gr_popup(self, event):                          #вып. меню для д1
        self.chosed = self.tree_box_gr.tree.identify_row(event.y)
        if self.chosed:
            self.tree_box_gr.tree.selection_set(self.chosed)
            self.popup_menu.tk_popup(event.x_root, event.y_root)
    def add_box_gr(self, edit = None):                      #добавление через add_1 (группы) UNDONE
        try:
            if self.add_box_gr_status == 1:
                return
        except:
            pass
        self.add_box_gr_w = Toplevel(self)
        self.add_box_gr_status = 1
        if edit:
            self.add_box_gr_w.title('Изменение группы')
        else:
            self.add_box_gr_w.title('Добавление группы')
        self.add_box_gr_w.resizable(0, 0)
        self.add_box_gr_w.grab_set()
        if edit:
            if edit[-1] == '}' and edit[0] == '{':
                edit = (edit[:-1])[1:]
            self.add_box_gr_entry = basic(self.add_box_gr_w, tk.Entry, width = 30, text = edit)
            self.add_box_gr_entry.new_wid.delete(0, "end")
            self.add_box_gr_entry.new_wid.insert(0, edit)
        else:
            self.add_box_gr_entry = basic(self.add_box_gr_w, tk.Entry, width = 30)
        self.add_box_gr_cancel = basic(self.add_box_gr_w, tk.Button, width = 10, text = "Отмена", command = lambda: self.add_box_gr_close())
        if edit:
            self.add_box_gr_ok = basic(self.add_box_gr_w, tk.Button, width = 10, text= "Изменить", command = lambda: self.add_box_gr_edit(self.add_box_gr_entry.new_wid.get(), edit))
        else:
            self.add_box_gr_ok = basic(self.add_box_gr_w, tk.Button, width = 10, text= "Добавить", command = lambda: self.add_box_gr_add(self.add_box_gr_entry.new_wid.get()))
        self.add_box_gr_entry.grid(1, 1, 3, 1, N + S + W + E)
        self.add_box_gr_cancel.grid(1, 3, 1, 1, N + S + W + E)
        self.add_box_gr_ok.grid(3, 3, 1, 1, N + S + W + E)
        self.add_box_gr_w.columnconfigure(0, minsize = 20)
        self.add_box_gr_w.columnconfigure(2, minsize = 60)
        self.add_box_gr_w.columnconfigure(4, minsize = 20)
        self.add_box_gr_w.rowconfigure(0, minsize=20)
        self.add_box_gr_w.rowconfigure(2, minsize=20)
        self.add_box_gr_w.rowconfigure(4, minsize=20)
        if edit:
            self.add_box_gr_w.bind('<Return>', lambda event:self.add_box_gr_edit(self.add_box_gr_entry.new_wid.get(), edit))
        else:
            self.add_box_gr_w.bind('<Return>', lambda event:self.add_box_gr_add(self.add_box_gr_entry.new_wid.get()))
        self.add_box_gr_w.protocol("WM_DELETE_WINDOW", self.add_box_gr_close)
    def add_box_gr_close(self):                             #закрытие окна добавления
        self.add_box_gr_status = 0
        self.add_box_gr_w.grab_release()
        self.add_box_gr_w.destroy()
    def del_box_gr(self, target):                           #удаление из д1
        if target[-1] == '}' and target[0] == '{':
            target = (target[:-1])[1:]
        self.del_check1 = messagebox.askokcancel(title = 'Удаление группы', parent = self, message = 'Удалить группу {}? Все вложенные записи будут перемещены в "Без группы"'.format(target), icon = messagebox.WARNING)
        if self.del_check1 == TRUE:
            self.cur = conn.cursor()
            try:
                self.cur.execute("DELETE FROM product_group WHERE name = '{}'".format(target))
                self.cur.close()
                self.status_bar.upd(text = "Удалена группа {}".format(target))
                self.tree_box_gr_fill()
            except:
                self.status_bar.upd(text = "Ошибка удаления группы {}".format(target))
    def add_box_gr_add(self, target):                       #добавление строки д1
        self.cur = conn.cursor()
        try:
            self.cur.execute("INSERT INTO product_group(name) VALUES ('{}')".format(target))
            self.cur.close()
            self.status_bar.upd(text = "Добавлена группа {}".format(target))
            self.tree_box_gr_fill()
        except:
            self.status_bar.upd(text = "Ошибка добавления группы {}".format(target))
    def add_box_gr_edit(self, edited, target):              #изменение строки д1
        if target[-1] == '}' and target[0] == '{':
            target = (target[:-1])[1:]
        self.cur = conn.cursor()
        try:
            self.cur.execute("UPDATE product_group SET name = '{}' where NAME = '{}'".format(edited, target))
            self.cur.close()
            self.status_bar.upd(text = "Группа {} переименована в {}".format(target, edited))
            self.tree_box_gr_fill()
            self.add_box_gr_close()
            self.add_box_gr(edited)
        except:
            self.status_bar.upd(text = "Ошибка изменения группы {}".format(target))
    def frame_box_fill(self, frame):                        #виджеты фрейма_2 (корпуса)
        self.tree_box = trees(frame.new_wid, columns = "Name", height = 30)
        self.tree_box.size(1, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO)
        self.butt_box = basic(frame.new_wid, tk.Button, text = "Добавить")
        self.tree_box.grid(0, 0, 1, 1, N + S + W + E)
        self.butt_box.grid(0, 1, 1, 1, N + S + W + E)
        self.tree_box.tree.bind('<ButtonRelease-1>', lambda event: self.box_info_fill(self.tree_box.tree.focus(), self.box_gr_opened))
    def tree_box_fill(self, group):                         #заполнение фрейма_2
        if self.box_gr_opened == group:
            return
        self.box_gr_opened = group
        self.tree_box.tree.delete(*self.tree_box.tree.get_children())
        i = 0
        self.cur = conn.cursor()
        if group[-1] == '}' and group[0] == '{':
            group = (group[:-1])[1:]
        self.cur.execute("SELECT name FROM product_box WHERE group_name = %s ORDER BY name", (group,))
        self.box = self.cur.fetchall()
        for a in self.box:
            self.tree_box.tree.insert(parent = '', index = i, iid = a, values = a)
            i += 1
        self.cur.close()
    def frame_box_info_fill(self, frame):                   #виджеты фрейма_3 (информация)
        self.info_changed_status = 0
        self.frame_info_gr = basic(frame.new_wid, tk.Labelframe, text = "Группа:")
        self.info_gr = basic(self.frame_info_gr.new_wid, tk.Combobox, state = 'readonly')
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
    def info_changed(self, *args):
        print(*args)
        print(self.info_name_value.get())
        pisya = tk.Style()
        if self.info_changed_status == 0:
            pisya.configure('Red.TEntry', foreground = 'red')
        self.info_changed_status = 1
        self.info_name.new_wid.configure(style = "Red.TEntry")
    def frame_box_det_fill(self, frame):                    #виджеты фрейма_4 (детали)

        self.frame_detail_top = basic(frame.new_wid, tk.Frame)
        self.detail_top_names = [["№", 3], ["Название", 20], ["Материал", 20], ["Вес", 3], ["S1", 3], ["S2", 3], ["S3", 3], ["Примечание", 20], ["Кол-во", 6]]
        i = 0
        self.detai_label = []
        for a, b in self.detail_top_names:
            self.detai_label.append(basic(self.frame_detail_top.new_wid, tk.Entry, width = b))
            self.detai_label[i].new_wid.insert(0, a)
            self.detai_label[i].new_wid.config(state = DISABLED)
            self.detai_label[i].grid(i, 0, 1, 1)
            i += 1
        self.frame_detail_top.grid(0, 0, 1, 1)
        a = 10 #здесь будет количество созданных деталей
        i = 0 #счетчик
        self.detail_frame = [] #массив для каждой детали
        self.detail_fields = [] #массив для параметров каждой детали
        while i < a:
            self.detail_fields.append([])
            self.detail_frame.append(basic(frame.new_wid, tk.Frame))
            self.detail_frame[i].grid(0, i + 1, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 3))
            self.detail_fields[i][0].new_wid.insert(0, i + 1)
            self.detail_fields[i][0].grid(0, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 20))
            self.detail_fields[i][1].grid(1, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Combobox, values = ["Сталь 0.8мм", "Сталь 1мм", "Сталь 1мм(Оц)", "Сталь 1.5мм", "Сталь 2мм", "Сталь 2мм(Оц)", \
                "Сталь 3мм(рифл)", "Сталь 5мм"], width = 17))
            self.detail_fields[i][2].grid(2, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 3))
            self.detail_fields[i][3].grid(3, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 3))
            self.detail_fields[i][4].grid(4, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 3))
            self.detail_fields[i][5].grid(5, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 3))
            self.detail_fields[i][6].grid(6, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 20))
            self.detail_fields[i][7].grid(7, 0, 1, 1)
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 6))
            self.detail_fields[i][8].grid(8, 0, 1, 1)
            i += 1
    def frame_box_mat_fill(self, frame):                    #виджеты фрейма_5 (материалы) UNDONE
        pass
    def box_info_fill(self, box, box_gr):                   #заполение фрейма_3
        if box == '':
            return
        if box[-1] == '}' and box[0] == '{':
            box = (box[:-1])[1:]

        if box_gr[-1] == '}' and box_gr[0] == '{':
            box_gr = (box_gr[:-1])[1:]
        self.cur = conn.cursor()
        self.cur.execute("SELECT size, notes, price, code FROM product_box WHERE name = '{}' AND group_name = '{}'".format(box, box_gr))
        self.box_info = self.cur.fetchall()
        self.cur.close()
        self.info_gr.new_wid.set(box_gr)
        self.info_name_value.set(box)
        self.info_name_value.trace_add("write", self.info_changed)
        #self.info_name.new_wid.delete(0, "end")
        #self.info_name.new_wid.insert(0, box)
        try:
            self.info_size_value.set(self.box_info[0][0])
        except:
            pass
        self.info_size_value.trace_add("write", self.info_changed)
        self.info_note.new_wid.delete('1.0', "end")
        try:
            self.info_note.new_wid.insert('1.0', self.box_info[0][1])
        except:
            pass
        print(self.box_info[0][3])
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

def _onKeyRelease(event):       #добавление эвентов на русской раскладке (ctrl+a, ctrl+v, ctrl+x, ctrl+c)
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