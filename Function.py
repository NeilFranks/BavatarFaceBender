from tkinter import StringVar, OptionMenu


class function(object):
    def __init__(self, root, row, column):
        self.root = root

        self.functions = {
            "linear": lambda frac, whole: frac*whole,
            "binary": lambda frac, whole: whole if frac >= 0.5 else 0,
        }

        options = self.functions.keys()
        self.default = list(options)[0]

        self.v = StringVar()
        self.v.set(self.default)
        self.o = OptionMenu(
            self.root,
            self.v,
            *options
        )
        self.o.grid(row=row, column=column)

    def get_key(self):
        return self.v.get()

    def get_value(self):
        return self.functions[self.v.get()]

    def set_value(self, value):
        self.v.set(value)
