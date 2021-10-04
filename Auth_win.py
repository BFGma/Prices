from tkinter import *
from psycopg2 import *

conn = ()

def login(string1, string2, name, name2):
    global conn
    try:
        conn = connect(dbname = "Prices", user = string1, password = string2, port = "5432")
        name.destroy()
    except:
        result_log = "Неверный логин/пароль"
        name2.config(text = result_log)

def auth(name):
    result_log = "Введите логин и пароль"
    auth_w = Toplevel(name)
    stat = Label(auth_w, text = result_log) 
    auth_log = Entry(auth_w, width = 20)
    auth_pass = Entry(auth_w, width = 20, show = "*")
    but_try_log = Button(auth_w, width = 8, height = 1, text = "Ок", command = lambda: login(auth_log.get(), auth_pass.get(), auth_w, stat))
    but_cancel_log = Button(auth_w, width = 8, height = 1, text = "Отмена", command = lambda: name.destroy())
    error_login = "as"
    stat.grid(column = 1, row = 0, columnspan = 3)
    auth_log.grid(column = 1, row = 1, columnspan = 3)
    auth_pass.grid(column = 1, row = 3, columnspan = 3)
    but_try_log.grid(column = 1, row = 5)
    but_cancel_log.grid(column = 3, row = 5)
    return conn
