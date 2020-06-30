from tkinter import Label
from FluctuatingValueControl import FluctuatingValueControl


class color_widget(object):
    def __init__(self, root, row, column):
        Label(root, text="R").grid(row=row, column=column)
        Label(root, text="G").grid(row=row+1, column=column)
        Label(root, text="B").grid(row=row+2, column=column)

        self.red = FluctuatingValueControl(root, row=row, column=column+1)
        self.green = FluctuatingValueControl(root, row=row+1, column=column+1)
        self.blue = FluctuatingValueControl(root, row=row+2, column=column+1)

    def to_dict(self):
        return {
            "red": self.red.to_dict(),
            "green": self.green.to_dict(),
            "blue": self.blue.to_dict(),
        }

    def from_dict(self, data_object):
        self.red.from_dict(data_object["red"])
        self.green.from_dict(data_object["green"])
        self.blue.from_dict(data_object["blue"])
