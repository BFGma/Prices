from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tk
from psycopg2 import *

global conn, status_now
conn = ()
status_now = 0
role = 1

class basic(Widget):
    def __init__(self, parent, w_type, **sets):     #создание класса виджетов
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
        self.status = -1
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
        root.protocol("WN_DELETE_WINDOW", self.closing)
        self.mat_w = mat_w(root, text = "Материалы", close = lambda: mat_w.close(self.mat_w))
        self.box_w = box_w(root, text = "Корпуса")
        self.sch_w = wind(root, text = "Схемы")
        self.auth_w = auth_w(root, text = "Авторизация", close = lambda: root.destroy())
        self.sett_w = wind(root, text = "Настройки")
        wind.table(root, "r", 0, 20, "r", 1, 30, "r", 2, 20, "c", 0, 20, "c", 1, 50, "c", 2, 20, "c", 3, 50, "c", 4, 20, "c", 5, 50, "c", 6, 20)
        self.mat_w_open = basic(root, Button, text = "Материалы", command = lambda: self.mat_w.reopen(), width = 10)
        self.mat_w_open.grid(1, 1, 1, 1, N + S + W + E)
        self.box_w_open = basic(root, Button, text = "Корпуса", command = lambda: self.box_w.reopen(), width = 10)
        self.box_w_open.grid(3, 1, 1, 1, N + S + W + E)
        self.sch_w_open = basic(root, Button, text = "Схемы", command = lambda: self.sch_w.open(), width = 10)
        self.sch_w_open.grid(5, 1, 1, 1, N + S + W + E)
        self.setts = basic(root, Button, bitmap = 'gray12', command = lambda: self.sett_w.open())
        self.setts.grid(0, 3, 1, 1, N + S + W + E)
        self.status = basic(root, Label, text = "Not connected...", bg = 'grey')
        self.status.grid(1, 3, 7, 1, N + S + W + E)
    def closing(self):      #закртыие соединения при закрытии окна
        if (conn):
            conn.close()
        main_w.destroy()

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
        self.butt_cancel = basic(self, Button, text = "Отмена", width = 8, command = lambda: main.closing())
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
            conn.set_session(autocommit = True)
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
        self.widgets()
    def widgets(self):      #виджеты
        self.tree_m_gr = trees(self, columns = "Name", height = 20)
        self.tree_m_u = trees(self, columns = ("Name", "Price", "Date"))
        self.tree_m_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.tree_m_u.size(3, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO, \
            text_2 = "Цена", width_2 = 80, minwidth_2 = 80, stretch_2 = NO, \
                text_3 = "Дата", width_3 = 80, minwidth_3 = 80, stretch_3 = NO)
        self.status_separ = basic(self, tk.Separator, orient = HORIZONTAL)
        self.status_bar = basic(self, Label, text = "-")
        self.tree_m_gr.grid(0, 1, 4, 1, N + S + W + E)
        self.tree_m_u.grid(5, 1, 8, 1, N + S + W + E)
        self.status_separ.grid(0, 4, 14, 1, N + S + W + E)
        self.status_bar.grid(0, 5, 14, 1, N + S + W + E)
        self.tree_m_gr.tree.bind('<ButtonRelease-1>', lambda event: self.fill_unit(self.tree_m_gr.tree.focus()))
        self.tree_m_gr.tree.bind('<Double-Button-1>', lambda event: self.edit_gr(self.tree_m_gr.tree.focus()))
        self.tree_m_u.tree.bind('<Double-Button-1>', lambda event: self.edit_u(self.tree_m_u.tree.focus()))
    def add_fields_gr(self):     #создание полей добавления групп
        self.entry_m_gr = basic(self, Entry)
        self.button_m_gr = basic(self, Button, text = "+", command = lambda: self.add_gr_write())
        self.entry_m_gr.grid(2, 2, 1, 1)
        self.button_m_gr.grid(3, 2, 1, 1, N + S + W + E)
        self.fields_gr_status = 'Add'
    def add_fields_u(self):     #создание полей добавление материалов
        self.entry_m_u_gr = basic(self, tk.Combobox, values = self.m_gr, width = 22, state = 'readonly')
        self.entry_m_u_gr.new_wid.current(0)
        self.entry_m_u_name = basic(self, tk.Entry)
        self.entry_m_u_price = basic(self, tk.Entry, width = 13)
        self.entry_m_u_measure = basic(self, tk.Combobox, values = ['шт', 'кг', 'л', 'м'], width = 5, state = 'readonly')
        self.entry_m_u_measure.new_wid.current(0)
        self.button_m_u = basic(self, Button, text = "+", command = lambda: self.add_u_write())
        self.entry_m_u_producer = basic(self, tk.Entry)
        self.label_m_u_help = basic(self, Label, text = "Типовое:")
        self.check_m_u_typical = basic(self, Checkbutton)
        self.entry_m_u_gr.grid(7, 2, 1, 1)
        self.entry_m_u_name.grid(8, 2, 1, 1)
        self.entry_m_u_price.grid(9, 2, 2, 1)
        self.entry_m_u_measure.grid(11, 2, 1, 1)
        self.button_m_u.grid(12, 2, 1, 1)
        self.entry_m_u_producer.grid(8, 3, 1, 1)
        self.label_m_u_help.grid(9, 3, 1, 1)
        self.check_m_u_typical.grid(10, 3, 1, 1)
        self.fields_u_status = 'Add'
    def fill(self):     #заполнение дерева группы материалов
        self.tree_m_gr.tree.delete(*self.tree_m_gr.tree.get_children())
        self.tree_m_gr.tree.insert(parent = '', iid = "Все", index = 0, values = "Все")
        i = 1
        self.cur = conn.cursor()
        self.cur.execute("SELECT name FROM material_group ORDER BY name;")
        self.m_gr = self.cur.fetchall()
        self.m_gr = [a[0] for a in self.m_gr]
        for a in self.m_gr:
            self.tree_m_gr.tree.insert(parent = '', iid = a, index = i, values = a)
            i += 1
        self.cur.close()
    def fill_unit(self, group):     #заполнение дерева материалов
        print(group)
        self.tree_m_u.tree.delete(*self.tree_m_u.tree.get_children())
        i = 0
        self.cur = conn.cursor()
        if group == "Все":
            self.cur.execute("SELECT №, name, price, upddate FROM material_unit ORDER BY name")
        else:
            self.cur.execute("SELECT №, name, price, upddate FROM material_unit WHERE group_name = %s ORDER BY name", (group,))
        self.m_u = self.cur.fetchall()
        for a, b, c, d in self.m_u:
            self.tree_m_u.tree.insert(parent = '', index = i, iid = a, values = (b, c, d))
            i += 1
        self.cur.close()
    def add_gr_write(self):       #добавление группы
        self.to_add_gr = self.entry_m_gr.new_wid.get()
        self.cur = conn.cursor()
        try:
            self.cur.execute("INSERT INTO material_group(name) VALUES (%s)", (self.to_add_gr,))
            self.status_bar.upd(text = "Новая группа добавлена")
        except:
            self.status_bar.upd(text = "Ошибка записи новой группы")
        self.cur.close()
        self.fill()
        self.entry_m_u_gr.upd(values = self.m_gr)
    def edit_gr(self, group):      #изменение/удаление группы
        if self.fields_gr_status == 'Edit':
            self.edit_gr_close()
        self.entry_m_gr.new_wid.delete(0, "end")
        self.entry_m_gr.new_wid.insert(0, group)
        self.button_m_gr.upd(text = "Upd", command = lambda: self.edit_gr_write(group)) 
        self.button_m_gr_del = basic(self, tk.Button, text = "DEL", width = 3, command = lambda: self.del_gr(group))
        self.button_m_gr_close_edit = basic(self, Button, text ="x", command = lambda: self.edit_gr_close())
        self.button_m_gr_close_edit.grid(0, 2, 1, 1)
        self.button_m_gr_del.grid(1, 2, 1, 1)
        self.fields_gr_status = 'Edit'
    def edit_gr_write(self,group):        #изменение группы - запись результата в бд
        self.to_upd_gr = self.entry_m_gr.new_wid.get()
        self.cur = conn.cursor()
        try:
            self.cur.execute("UPDATE material_group SET name = '{new_name}' where name = '{name}'".format(new_name = self.to_upd_gr, name = group))
            self.cur.close()
            self.status_bar.upd(text = "Группа {name} переименована в {new_name}".format(name = group, new_name = self.to_upd_gr))
            self.fill()
            self.entry_m_u_gr.upd(values = self.m_gr)
            self.entry_m_gr.new_wid.delete(0, "end")
        except:
            self.status_bar.upd(text = "Ошибка изменения группы {}".format(group))
    def del_gr(self, group):        #удаление группы
        self.check_del_gr = messagebox.askokcancel(title = 'Удаление группы', parent = self, message = 'Удалить группу {}? Все вложенные записи будут перемещены в "Без группы"'.format(group), icon = messagebox.WARNING)
        if self.check_del_gr == TRUE:
            self.cur = conn.cursor()
            try:
                self.cur.execute("DELETE FROM material_group WHERE name = '{}'".format(group))
                self.cur.close()
                self.status_bar.upd(text = "Удалена группа {}".format(group))
                self.fill()
                self.entry_m_u_gr.upd(values = self.m_gr)
                self.entry_m_gr.new_wid.delete(0, "end")
            except:
                self.status_bar.upd(text = "Ошибка удаления группы {}".format(group))
    def edit_gr_close(self):        #изменение группы - закрытие (открытие добавления группы)
        self.entry_m_gr.new_wid.delete(0, "end")
        self.button_m_gr.upd(text = "+", command = lambda: self.add_gr_write())
        self.button_m_gr_close_edit.new_wid.grid_forget()
        self.button_m_gr_del.new_wid.grid_forget()
        self.fields_gr_status = 'Add'
    def add_u_write(self):        #добавление материала
        self.cur = conn.cursor()
        try:
            self.cur.execute("INSERT INTO material_unit(group_name, name, price, measure, producer) values('{group_name}', '{name}', {price}, '{meas}', '{prod}')"\
                .format(group_name = self.entry_m_u_gr.new_wid.get(), name = self.entry_m_u_name.new_wid.get(), price = self.entry_m_u_price.new_wid.get(), \
                    meas = self.entry_m_u_measure.new_wid.get(), prod = self.entry_m_u_producer.new_wid.get()))
            self.status_bar.upd(text = "Новый материал добавлен")
        except:
            self.status_bar.upd(text = "Ошибка добавления нового материала")
        self.cur.close()
        self.fill_unit(self.tree_m_gr.tree.focus())
    def edit_u(self, unit):       #изменение/удаление материала - сюда передается № выбранного материала
        if self.fields_u_status == 'Edit':
            self.edit_u_close()
        self.cur = conn.cursor()
        self.cur.execute("SELECT group_name, name, price, measure, producer, typical, upddate FROM material_unit WHERE № = {}".format(unit))
        self.u_to_edit = self.cur.fetchall()
        self.cur.close()
        self.entry_m_u_measure.new_wid.set(self.u_to_edit[0][3])
        self.entry_m_u_gr.new_wid.set(self.u_to_edit[0][0])
        self.entry_m_u_name.new_wid.delete(0, "end")
        self.entry_m_u_name.new_wid.insert(0, self.u_to_edit[0][1])
        self.entry_m_u_price.new_wid.delete(0, "end")
        self.entry_m_u_price.new_wid.insert(0, self.u_to_edit[0][2])
        self.entry_m_u_producer.new_wid.delete(0,"end")
        self.entry_m_u_producer.new_wid.insert(0,self.u_to_edit[0][4])
        self.button_m_u_del = basic(self, Button, text = "DEL", command = lambda: self.del_u(unit))
        self.button_m_u_close_edit = basic(self, Button, text = "x", command = lambda: self.edit_u_close())
        self.button_m_u_del.grid(6, 2, 1, 1)
        self.button_m_u_close_edit.grid(5, 2, 1, 1)
        self.button_m_u.upd(text = "Upd", command = lambda: self.edit_u_write(unit))
        self.fields_u_status = 'Edit'
    def edit_u_write(self, unit):       #изменение материала - запись результата в бд
        self.cur = conn.cursor()
        try:
            self.cur.execute("UPDATE material_unit SET group_name = '{group_name}', name = '{name}', price = {price}, producer = '{prod}', measure = '{meas}' WHERE № = {unit}"\
                .format(group_name = self.entry_m_u_gr.new_wid.get(), name = self.entry_m_u_name.new_wid.get(), price = self.entry_m_u_price.new_wid.get(), \
                    meas = self.entry_m_u_measure.new_wid.get(), prod = self.entry_m_u_producer.new_wid.get(), unit = unit))
            self.cur.close()
            self.status_bar.upd(text = "Материал {name} переименован".format(name = self.entry_m_u_name.new_wid.get()))
            self.fill_unit(self.tree_m_gr.tree.focus())
            self.entry_m_u_producer.new_wid.delete(0, "end")
            self.entry_m_u_name.new_wid.delete(0, "end")
            self.entry_m_u_price.new_wid.delete(0, "end")
            self.entry_m_u_measure.new_wid.current(0)
            self.entry_m_u_gr.new_wid.current(0)
        except:
            self.status_bar.upd(text = "Ошибка изменения материала")
    def del_u(self,unit):      #удаление материала 
        self.check_del_u = messagebox.askokcancel(title = 'Удаление материала', parent = self, message = 'Удалить материал?', icon = messagebox.WARNING)
        if self.check_del_u == TRUE:
            self.cur = conn.cursor()
            try:
                self.cur.execute("DELETE FROM material_unit WHERE № = {}".format(unit))
                self.cur.close()
                self.status_bar.upd(text = "Удален материал {}".format(unit))
                self.fill_unit(self.tree_m_gr.tree.focus())
                self.entry_m_u_producer.new_wid.delete(0, "end")
                self.entry_m_u_name.new_wid.delete(0, "end")
                self.entry_m_u_price.new_wid.delete(0, "end")
                self.entry_m_u_measure.new_wid.current(0)
                self.entry_m_u_gr.new_wid.current(0)
            except:
                self.status_bar.upd(text = "Ошибка удаления материала {}".format(unit))
    def edit_u_close(self):     #изменение материала - закрытие (открытие добавления материала)
        self.entry_m_u_name.new_wid.delete(0, "end")
        self.entry_m_u_price.new_wid.delete(0, "end")
        self.entry_m_u_producer.new_wid.delete(0,"end")
        self.entry_m_u_measure.new_wid.current(0)
        self.entry_m_u_gr.new_wid.current(0)
        self.button_m_u.upd(text = "+", command = lambda: self.add_u_write())
        self.button_m_u_del.new_wid.grid_forget()
        self.button_m_u_close_edit.new_wid.grid_forget()
        self.fields_u_status = 'Add'
    def reopen(self):   #открытие окна материалов по нажатию кнопки в главном окне
        self.open()
        self.fill()
        self.status_bar.upd(text = "-")
        if role == 1:
            self.add_fields_gr()
            self.add_fields_u()
    def close(self):        #доп. опции закрытия окна
        self.closing()
        if self.fields_gr_status == 'Edit':
            self.edit_gr_close()
        if self.fields_u_status == 'Edit':
            self.edit_u_close()

class box_w(wind):
    def __init__(self, parent, **sets):
        self.box_w = wind.__init__(self,parent, **sets)
        self.box_gr_opened = ''
        self.widgets_frame()
    def widgets_frame(self):        #создание фрэймов
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
        self.frame_box_mat_choose_fill(self.frame_box_mat_choose)
        self.frame_box_status_fill(self.frame_box_status)
        self.frame_box_gr.grid(0, 1, 1, 3)
        self.frame_box.grid(1, 1, 1, 3)
        self.frame_box_info.grid(2, 1, 1, 1)
        self.frame_box_det.grid(2, 2, 1, 1)
        self.frame_box_mat.grid(2, 3, 1, 1)
        self.frame_box_mat_choose.grid(3, 1, 1, 1)
        self.frame_box_status.grid(0, 4, 4, 1)
    def frame_box_gr_fill(self, frame):     #виджеты - группы корпусов !!!!!
        self.tree_box_gr = trees(frame.new_wid, columns = "Name", height = 30)
        self.tree_box_gr.size(1, text_1 = "Название группы", width_1 = 200, minwidth_1 = 200, stretch_1 = NO)
        self.butt_box_gr = basic(frame.new_wid, tk.Button, text = "Добавить")
        self.tree_box_gr.grid(0, 0, 1, 1, N + S + W + E)
        self.butt_box_gr.grid(0, 1, 1, 1, N + S + W + E)
        self.tree_box_gr.tree.bind('<ButtonRelease-1>', lambda event: self.tree_box_fill(self.tree_box_gr.tree.focus()))
    def tree_box_gr_fill(self):
        self.tree_box_gr.tree.delete(*self.tree_box_gr.tree.get_children())
        i = 0
        self.cur = conn.cursor()
        self.cur.execute("SELECT name FROM product_group ORDER BY name")
        self.box_gr = self.cur.fetchall()
        for a in self.box_gr:
            self.tree_box_gr.tree.insert(parent = '', index = i, iid = a, values = (a[0], ))
            i += 1
        self.cur.close()
    def frame_box_fill(self, frame):        #виджеты - корпуса !!!!!
        self.tree_box = trees(frame.new_wid, columns = "Name", height = 30)
        self.tree_box.size(1, text_1 = "Название", width_1 = 300, minwidth_1 = 300, stretch_1 = NO)
        self.butt_box = basic(frame.new_wid, tk.Button, text = "Добавить")
        self.tree_box.grid(0, 0, 1, 1, N + S + W + E)
        self.butt_box.grid(0, 1, 1, 1, N + S + W + E)
        self.tree_box.tree.bind('<ButtonRelease-1>', lambda event: self.box_info_fill(self.tree_box.tree.focus()))
    def tree_box_fill(self, group):
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
    def frame_box_info_fill(self, frame):       #виджеты - инфо о корпусе !!!!!
        self.frame_info_gr = basic(frame.new_wid, tk.Labelframe, text = "Группа:")
        self.info_gr = basic(self.frame_info_gr.new_wid, tk.Combobox, state = 'readonly')
        self.frame_info_name = basic(frame.new_wid, tk.Labelframe, text = "Название:")
        self.info_name = basic(self.frame_info_name.new_wid, tk.Entry)
        self.frame_info_size = basic(frame.new_wid, tk.Labelframe, text = "Размер:")
        self.info_size = basic(self.frame_info_size.new_wid, tk.Entry)
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
    def frame_box_det_fill(self, frame):        #виджеты - детали в корпусе !!!!!
        self.frame_detail_top = basic(frame.new_wid, tk.Frame)
        self.detail_top_names = [["№", 20], ["Название", 20], ["Материал", 20], ["Вес", 3], ["S1", 3], ["S2", 3], ["S3", 3], ["Примечание", 20], ["Кол-во", 6]]
        for a, b in self.detail_top_names:
            print(a, b)
        self.detail_label_1 = basic(self.frame_detail_top.new_wid, tk.Entry, width = 3)
        self.detail_label_1.new_wid.insert(0, "№")
        self.detail_label_1.new_wid.config(state = DISABLED)
        self.detail_label_2 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "Назв.", width = 20)
        self.detail_label_3 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "Мат.", width = 20)
        self.detail_label_4 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "Вес", width = 3)
        self.detail_label_5 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "S1", width = 3)
        self.detail_label_6 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "S2", width = 3)
        self.detail_label_7 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "S3", width = 3)
        self.detail_label_8 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "Прим.", width = 20)
        self.detail_label_9 = basic(self.frame_detail_top.new_wid, tk.Entry, text = "К-во", width = 6)
        self.detail_label_1.grid(0, 0, 1, 1)
        self.detail_label_2.grid(1, 0, 1, 1)
        self.detail_label_3.grid(2, 0, 1, 1)
        self.detail_label_4.grid(3, 0, 1, 1)
        self.detail_label_5.grid(4, 0, 1, 1)
        self.detail_label_6.grid(5, 0, 1, 1)
        self.detail_label_7.grid(6, 0, 1, 1)
        self.detail_label_8.grid(7, 0, 1, 1)
        self.detail_label_9.grid(8, 0, 1, 1)
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
            self.detail_fields[i].append(basic(self.detail_frame[i].new_wid, tk.Entry, width = 20))
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
    def frame_box_mat_fill(self, frame):        #виджеты - материалы в корпусе !!!!!
        pass
    def box_info_fill(self, box):
        print('suka')
        pass
    def frame_box_mat_choose_fill(self, frame):     #виджеты - выбор материала !!!!!
        pass
    def frame_box_status_fill(self, frame):     #виджеты - статус
        self.status_bar = basic(frame.new_wid, Label, text = "-")
        self.status_bar.grid(0, 0, 1, 1, N + S + W + E)
    def reopen(self):   #открытие окна материалов по нажатию кнопки в главном окне
        self.open()
        self.tree_box_gr_fill()
        self.status_bar.upd(text = "-")

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

main_w = Tk()
main_w.bind_all("<Key>", _onKeyRelease, "+")
main = programm(main_w)
main_w.mainloop()
