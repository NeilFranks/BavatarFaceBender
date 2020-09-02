from tkinter import Entry, IntVar


class int_entry(object):
    def __init__(self, root, low, high, row, column):
        self.low = low
        self.high = high

        self.v = IntVar()
        self.e = Entry(root, textvariable=self.v, width=5, validate="focusout", validatecommand=self.validate)
        self.e.grid(row=row, column=column)

        self.v.set(self.low)

    def validate(self):
        try:
            val = self.v.get()
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
        return self.v.get()

    def set_value(self, value):
        self.v.set(value)
