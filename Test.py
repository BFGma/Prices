from tkinter import *
import tkinter.ttk as tk

now_opened_box = ""

def tree_box_fill(a):
    i = 0
    global now_opened_box
    opened_box = tree_group.focus()
    if opened_box == now_opened_box:
        return
    tree_box.delete(*tree_box.get_children())
    now_opened_box = opened_box
    if tree_group.focus() == "Реле":
        for a in box1:
            tree_box.insert(parent = '', index = i, values = (a))
            i += 1
    if tree_group.focus() == "Рубильник":
        for a in box2:
            tree_box.insert(parent = '', index = i, values = (a))
            i += 1

group = ["Рубильник", "Реле", "Предохранитель", "442", "23", "44", "33", "21", "27", "11", "19", "12"]
box1 = ["1", "2", "3", "4", "5", "6"]
box2 = ["7", "8"]

root = Tk()

#paned = tk.PanedWindow(orient = HORIZONTAL)
tree_group = tk.Treeview(root, show = "headings", columns = ("Name"), selectmode = 'browse')
tree_box = tk.Treeview(root, show = "headings", columns = ("Name", "Price"), selectmode = 'browse')
tree_group.heading("#1", text = "Название")
tree_group.column("#1", minwidth = 210, width = 200, stretch = NO)
scroll = tk.Scrollbar(root, command = tree_group.yview)
tree_group.configure(yscrollcommand = scroll.set)
scroll2 = tk.Scrollbar(root, command = tree_box.yview)
tree_box.configure(yscrollcommand = scroll2.set)

i = 0

for d in group:
    tree_group.insert(parent ='', index = i, iid = d, values = d)
    i += 1

scroll.grid(column = 2, row = 0, sticky = S + E + N)
tree_group.grid(column = 0, row = 0, sticky = N + S)
tree_box.grid(column = 3, row = 0, sticky = N + S)
scroll2.grid(column = 5, row = 0, sticky = S + E + N)
#paned.add(tree_group)
#paned.add(tree_box)
#paned.grid(column = 1, row = 0)

tree_group.bind('<ButtonRelease-1>', tree_box_fill)

root.mainloop()
