from tkinter import *   #подключение библиотеки GUI
import tkinter.ttk as tk       #подключение дополнительной библиотеки GUI
from psycopg2 import *  #подключение библиотеки для postgreSQL

status_now = "Not connected"    #Начальный статус соединения
conn = ()   #переменная для установки соединения с БД
material_unit_w_status = {} #словарь параметров окна материалов
scheme_w_status = {} #словарь параметров окна схемы

#функция авторизации

def login(string1, string2, name, name2):
    global conn
    global status_now
    try:
        conn = connect(dbname = "Prices", user = string1, password = string2, port = "5432")
        status_now = "Connected"
        status_bar.config(text = status_now)
        name.destroy()  #закрытие окна авторизации при успешном подключении
    except:
        result_log = "Неверный логин/пароль"
        name2.config(text = result_log)

#создание окна авторизации

def auth(name):
    result_log = "Введите логин и пароль"
    auth_w = Toplevel(name)
    auth_w.title = "Авторизация"
    auth_w.geometry('+{}+{}'.format((main_w.winfo_screenwidth() // 2 - 300 - 200), (main_w.winfo_screenheight() // 2 - 100)))
    auth_w.resizable(0, 0)
    stat = Label(auth_w, text = result_log) 
    auth_log = Entry(auth_w, width = 20)
    auth_pass = Entry(auth_w, width = 20, show = "*")
    but_try_log = Button(auth_w, width = 8, height = 1, text = "Ок", command = lambda: login(auth_log.get(), auth_pass.get(), auth_w, stat))
    but_cancel_log = Button(auth_w, width = 8, height = 1, text = "Отмена", command = lambda: name.destroy())
    auth_w.columnconfigure(0, minsize = 20)
    auth_w.columnconfigure(4, minsize = 20)
    auth_w.rowconfigure(4, minsize = 10)
    auth_w.rowconfigure(6, minsize = 20)
    stat.grid(column = 1, row = 0, columnspan = 3)
    auth_log.grid(column = 1, row = 1, columnspan = 3)
    auth_pass.grid(column = 1, row = 3, columnspan = 3)
    but_try_log.grid(column = 1, row = 5)
    but_cancel_log.grid(column = 3, row = 5)
    auth_w.protocol("WM_DELETE_WINDOW", name.destroy)

#функция закрытия окна по кнопке Х

def closing():
    if (conn):
        conn.close()
    main_w.destroy()

#функция проверки наличия соединения раз в 60000 мс

def check_connection_status():
    global status_now
    if (conn):
        try:
            cur = conn.cursor()
            cur.execute("SELECT")
            cur.close()
            status_now = "Connected"
        except:
            status_now = "Disconnected by server"
            auth(main_w)    #вызов повторной авторизации при отсутствии соединения
    else:
        status_now = "Not connected"
    status_bar.config(text = status_now)
    main_w.after(60000, check_connection_status)

#функция заполнения таблицы группы материалов

def fill_material_group(tree):
    i = 0
    cur = conn.cursor()
    cur.execute("SELECT name FROM material_group ORDER BY name")
    group = cur.fetchall()
    for a in group:
        tree.insert(parent = '', index = i, iid = a, values = a)
        i += 1
    cur.close()

#заполнение дерева из таблицы материалов

nowopened_material_unit_w = ""

def tree_material_unit_fill(opened, treeto):
    i = 0
    global nowopened_material_unit_w
    if opened == nowopened_material_unit_w:
        return
    treeto.delete(*treeto.get_children())
    nowopened_material_unit_w = opened
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT №, name, price FROM material_unit WHERE group_name = %s', (opened,))
        unit = cur.fetchall()
        for a, b, c in unit:
            treeto.insert(parent = '', index = i, iid = a, values = (b, c))
            i += 1
        cur.close()

#создание окна добавления/изменения групп материалов

def material_group_window():
    material_group_w = Toplevel(main_w)
    material_group_w.title = "Таблица групп материалов"
    material_group_w.resizable(0, 0)
    tree_group = tk.Treeview(material_group_w, show = "headings", columns = "Name", selectmode = "browse")
    tree_group.heading("#1", text = "Название")
    tree_group.column("#1", minwidth = 300, width = 300, stretch = NO)
    scroll = tk.Scrollbar(material_group_w, command = tree_group.yview)
    tree_group.configure(yscrollcommand = scroll.set)
    tree_group.grid(column = 0, row = 1, sticky = N + W + S)
    scroll.grid(column = 1, row = 1, sticky = N + S)
    fill_material_group(tree_group)

#добаление группы

def popup_change_group(window):
    global material_unit_w_status
    material_unit_w_status['entry_name'] = Entry(window, text = "")
    material_unit_w_status['but_del'] = Button(window, text = "del")
    material_unit_w_status['but_add'] = Button(window, text = "add")
    material_unit_w_status['entry_name'].grid(column = 1, row = 4, columnspan = 3, sticky = N + S + W + E)
    material_unit_w_status['but_del'].grid(column = 1, row = 6, sticky = N + S + W + E)
    material_unit_w_status['but_add'].grid(column = 3, row = 6, sticky = N + S + W + E)
    window.update()
    material_unit_w_status['addgroup'] = "1"

#создание окна добавления/изменения материалов

def material_unit_window():
    material_unit_w = Toplevel(main_w)
    material_unit_w.title = "Таблица материалов"
    material_unit_w.resizable(0, 0)
    tree_group = tk.Treeview(material_unit_w, show = "headings", column = "Name", selectmode = "browse")
    tree_group.heading("#1", text = "Название")
    tree_group.column("#1", minwidth = 300, width = 300, stretch = NO)
    scroll = tk.Scrollbar(material_unit_w, command = tree_group.yview)
    tree_group.configure(yscrollcommand = scroll.set)
    tree_unit = tk.Treeview(material_unit_w, show = "headings", columns = ("Name", "Price"), selectmode = "browse")
    tree_unit.heading("#1", text = "Название")
    tree_unit.heading("#2", text = "Цена")
    tree_unit.column("#1", minwidth = 300, width = 300, stretch = NO)
    tree_unit.column("#2", minwidth = 100, width = 100, stretch = NO)
    scroll2 = tk.Scrollbar(material_unit_w, command = tree_unit.yview)
    tree_unit.configure(yscrollcommand = scroll2.set)
    if 1:#CHANGE FOR USERS
        butt_add_group = Button(material_unit_w, text = "Добавление группы", command = lambda: popup_change_group(material_unit_w))
        butt_add_unit = Button(material_unit_w, text = "Добавление комплектующих")
        butt_add_group.grid(column = 0, row = 2, columnspan = 6, sticky = N + S + W + E)
        butt_add_unit.grid(column = 7, row = 2, columnspan = 8, sticky = N + S + W + E) 
    tree_group.grid(column = 0, row = 1, columnspan = 6, sticky = N + S + W + E)
    scroll.grid(column = 6, row = 1, sticky = N + S + W + E)
    tree_unit.grid(column = 7, row = 1, columnspan = 8, sticky = N + S + W + E)
    scroll2.grid(column = 15, row = 1, sticky = N + S + W + E)
    fill_material_group(tree_group)
    tree_group.bind('<ButtonRelease-1>', lambda event: tree_material_unit_fill(tree_group.focus(), tree_unit))


#создание основного окна

main_w =  Tk()
main_w.title("База данных цен")

main_w.geometry('590x220+{}+{}'.format((main_w.winfo_screenwidth() // 2 - 300), (main_w.winfo_screenheight() // 2 - 100)))
main_w.resizable(0, 0)

auth(main_w)    #вызов окна авторизации

#верстка главного окна

but_Mat_group = Button(main_w, text = "Группы\nматериалов", justify = CENTER, width = 12, height = 2, command = material_group_window)
but_Prod_group = Button(main_w, text = "Группы\nпродукции", justify = CENTER, width = 12, height = 2)
but_Prod_box = Button(main_w, text = "Корпуса", width = 12, height = 2)
but_Mat = Button(main_w, text = "Материалы", width = 12, height = 2, command = material_unit_window)
but_Scheme = Button(main_w, text = "Схемы", width = 12, height = 2)
but_print_mat = Button(main_w, text = "Печать цен\nматериалов", justify = CENTER, width = 12, height = 2)
but_print_prod = Button(main_w, text = "Печать прайса", width = 12, height = 2)
but_settings = Button(main_w, text = "Настройки", width = 12, height = 2)
status_bar = Label(main_w, text = status_now)

main_w.rowconfigure(0, minsize = 20)
main_w.rowconfigure(3, minsize = 40)
main_w.rowconfigure(5, minsize = 20)
main_w.columnconfigure(0, minsize = 20)
main_w.columnconfigure(2, minsize = 20)
main_w.columnconfigure(4, minsize = 20)
main_w.columnconfigure(6, minsize = 20)
main_w.columnconfigure(8, minsize = 20)
main_w.columnconfigure(10, minsize = 20)
but_Mat_group.grid(column = 1, row = 1)
but_Prod_group.grid(column = 5, row = 1)
but_Prod_box.grid(column = 9, row = 1)
but_Mat.grid(column = 3, row = 2)
but_Scheme.grid(column = 7, row = 2)
but_print_mat.grid(column = 7, row = 4)
but_print_prod.grid(column = 9, row = 4)
but_settings.grid(column = 1, row = 4)
status_bar.grid(column = 1, row = 6, columnspan = 8)

main_w.protocol("WM_DELETE_WINDOW", closing)    #вызов функции при закрытии окна по кнопке Х

check_connection_status()   #первый вызов функции проверки наличия соединения
main_w.mainloop()   #основной цикл
