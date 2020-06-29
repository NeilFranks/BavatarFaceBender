from tkinter import Entry, StringVar, Checkbutton, IntVar, OptionMenu


class FluctuatingValueControl(object):
    def __init__(self, root, row, column):
        self.row = row
        self.initial_value = self.num_entry(root, row, column)
        self.low_value = self.num_entry(root, row, column + 1)
        self.high_value = self.num_entry(root, row, column + 2)
        self.fluctuate = self.fluctuate_check(root, row, column + 3)
        self.function = self.function(root, row, column + 4)

    def to_dict(self):
        return {
            "initial value": self.initial_value.get_value(),
            "low value": self.low_value.get_value(),
            "high value": self.high_value.get_value(),
            "fluctuate": self.fluctuate.get_value(),
            "function": self.function.get_key()
        }

    class num_entry(object):
        def __init__(self, root, row, column):
            self.low = 0
            self.high = 255

            self.v = StringVar()
            self.e = Entry(root, textvariable=self.v, width=3, validate="focusout", validatecommand=self.validate)
            self.e.grid(row=row, column=column)

            self.v.set(self.low)

        def validate(self):
            try:
                val = int(self.v.get())
                if val < self.low:
                    self.v.set(self.low)
                elif val > self.high:
                    self.v.set(self.high)
            except Exception as e:
                self.v.set(self.low)
            finally:
                return True

        def get_value(self):
            self.validate()
            return int(self.v.get())

    class fluctuate_check(object):
        def __init__(self, root, row, column):
            self.root = root

            self.v = IntVar()
            self.c = Checkbutton(root, variable=self.v)
            self.c.grid(row=row, column=column)

        def get_value(self):
            return self.v.get()

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
