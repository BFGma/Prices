from tkinter import *
import tkinter.ttk as tk

class widgets:

    def __init__(self, parent, w_type, **sets):
        self.parent = parent
        self.status = 0
        self.type = w_type
        self.new_wid = self.type(parent)
        for a, b in sets.items():
            self.new_wid[a] = b
        if self.type == tk.Treeview:
            self.scroll = tk.Scrollbar(parent, command = self.new_wid.yview)
            self.new_wid.configure(yscrollcommand = self.scroll.set)

    def wid_grid(self, **sets):
        self.new_wid.grid(column = sets.get("column"), row = sets.get("row"), columnspan = sets.get("columnspan", 1), \
                rowspan = sets.get("rowspan", 1), sticky = sets.get("sticky", ""))
        if self.type == tk.Treeview:
            self.scroll.grid(column = sets.get("column") + 1, row = sets.get("row"), columnspan = sets.get("columnspan", 1), \
                    rowspan = sets.get("rowspan", 1), sticky = N + S)
        self.status = 1

    def wid_forget(self):
        self.new_wid.grid_forget()
        if self.type == tk.Treeview:
            self.scroll.grid_forget()
        self.status = 2

    def wid_upd(self, **sets):
        for a, b in sets.items():
            self.mew_wid.config(a = b)

    def treeview_param(self, col_n, **sets):
        if self.type == tk.Treeview:
            a = 0
            while a <= col_n:
                self.new_wid.heading("#{}".format(a), text = sets.get("text_{}".format(a), ""))
                self.new_wid.column("#{}".format(a), minwidth = sets.get("minwidth_{}".format(a), 0), width = sets.get("width_{}".format(a), 100), \
                        stretch = sets.get("stretch_{}".format(a,), "YES"))
                a += 1

root = Tk()
zaloopa = widgets(root, Button, text = "ebat")
zaloopa.wid_grid(column = 1, row = 1)
zaloopa.wid_forget()
zaloopa.wid_grid(column = 1, row = 1)
zaloopa.wid_upd()
puk = widgets(root, tk.Treeview, show = "headings", column = ("Name", "Price"), selectmode = "browse")
puk.wid_grid(column = 1, row = 2)
puk2 = widgets(root, tk.Treeview, show = "headings", column = "Name", selectmode = "browse")
puk2.wid_grid(column = 3, row = 2)
puk.treeview_param(2, text_1 = "puk", minwidth_1 = 10, width_1 = 100, stretch_1 = "NO", text_2 ="srenk", minwidth_2 = 10, width_2 = 100, stretch_2 = "NO")
puk2.treeview_param(1, text_1 = "puki", minwidth_1 = 10, width_1 = 100, stretch_1 = "NO")
puk2.new_wid.insert("1", "2")
root.mainloop()
