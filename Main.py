from tkinter import *   #подключение библиотеки GUI
from psycopg2 import *  #подключение библиотеки для postgreSQL

status_now = "Not connected"    #Начальный статус соединения
conn = ()   #переменная для установки соединения с БД

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

#создание основного окна

main_w =  Tk()
main_w.title("База данных цен")

main_w.geometry('590x220+{}+{}'.format((main_w.winfo_screenwidth() // 2 - 300), (main_w.winfo_screenheight() // 2 - 100)))
main_w.resizable(0, 0)

auth(main_w)    #вызов окна авторизации

#верстка главного окна

but_Mat_group = Button(main_w, text = "Группы\nматериалов", justify = CENTER, width = 12, height = 2)
but_Prod_group = Button(main_w, text = "Группы\nпродукции", justify = CENTER, width = 12, height = 2)
but_Prod_box = Button(main_w, text = "Корпуса", width = 12, height = 2)
but_Mat = Button(main_w, text = "Материалы", width = 12, height = 2)
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
