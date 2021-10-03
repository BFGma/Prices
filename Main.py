import tkinter
from tkinter import *

main_w =  Tk()
main_w.title("База данных цен")

but_Mat_group = Button(main_w, text = "Группы\nматериалов", justify = CENTER, width = 13, height = 2)
but_Prod_group = Button(main_w, text = "Группы\nпродукции", justify = CENTER, width = 15, height = 2)
but_Prod_box = Button(main_w, text = "Корпуса", width = 15, height = 2)
but_Mat = Button(main_w, text = "Материалы", width = 15, height = 2)
but_Scheme = Button(main_w, text = "Схемы", width = 15, height = 2)
but_print_mat = Button(main_w, text = "Печать цен\nматериалов", justify = CENTER, width = 15, height = 2)
but_print_prod = Button(main_w, text = "Печать прайса", width = 15, height = 2)


but_Mat_group.grid(column = 0, row = 0)
but_Prod_group.grid(column = 2, row = 0)
but_Prod_box.grid(column = 4, row = 0)
but_Mat.grid(column = 1, row = 1)
but_Scheme.grid(column = 3, row = 1)
but_print_mat.grid(column = 3, row = 2)
but_print_prod.grid(column = 4, row = 2)

main_w.mainloop()

