from tkinter import *
from Auth_win import *

main_w =  Tk()
main_w.title("База данных цен")

main_w.geometry('590x200+{}+{}'.format((main_w.winfo_screenwidth() // 2 - 300), (main_w.winfo_screenheight() // 2 - 100)))
main_w.resizable(0, 0)

auth(main_w)

but_Mat_group = Button(main_w, text = "Группы\nматериалов", justify = CENTER, width = 12, height = 2)
but_Prod_group = Button(main_w, text = "Группы\nпродукции", justify = CENTER, width = 12, height = 2)
but_Prod_box = Button(main_w, text = "Корпуса", width = 12, height = 2)
but_Mat = Button(main_w, text = "Материалы", width = 12, height = 2)
but_Scheme = Button(main_w, text = "Схемы", width = 12, height = 2)
but_print_mat = Button(main_w, text = "Печать цен\nматериалов", justify = CENTER, width = 12, height = 2)
but_print_prod = Button(main_w, text = "Печать прайса", width = 12, height = 2)
but_settings = Button(main_w, text = "Настройки", width = 12, height = 2)

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

main_w.mainloop()
