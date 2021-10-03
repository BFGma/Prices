import tkinter
from tkinter import *

material = ["1", "2", "3", "42020202020202"]
material_1gr = ["11", "12", "13"]
material_2gr = ["21", "22", "23"]
material_3gr = ["31", "32", "33"]
a = 0
c = 0
d = 0

def deletenahui():
    buttonmat.pack_forget()

def read_material(b):
    c = 0
    for mats1 in material_1gr:
        buttonmat[c] = Button(root, text = mats1)
        buttonmat[c].grid(column=1, row=c)
        c = c + 1
    a = b

def del_mat(i):
    buttons[i].grid_forget()

root = Tk()
buttons = []
for groups in material:
    button = Button(root, text = groups)
    button.grid(column=0, row=d)
    d = d + 1
    buttons.append(button)

i = 0
buttonhuis = []
while i < d:
    buttonhui = Button(root, text = i, command = lambda i=i:del_mat(i))
    buttonhui.grid(column=0, row = i+10)
    buttonhuis.append(buttonhui)
    i += 1

root.mainloop()
