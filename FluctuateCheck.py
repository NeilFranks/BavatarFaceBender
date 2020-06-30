from tkinter import Checkbutton, IntVar


class fluctuate_check(object):
    def __init__(self, root, row, column):
        self.root = root

        self.v = IntVar()
        self.c = Checkbutton(root, variable=self.v)
        self.c.grid(row=row, column=column)

    def get_value(self):
        return self.v.get()

    def set_value(self, value):
        self.v.set(value)
