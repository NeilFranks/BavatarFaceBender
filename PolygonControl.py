from tkinter import Button, Frame, Label
from tkinter.ttk import Notebook, Separator
from FluctuatingValue import FluctuatingValue
from FluctuatingValueControl import fluct
from PolygonEffect import PolygonEffect
from Video import effects


class PolygonControl(object):
    def __init__(self, root):
        self.tabs = Notebook(root)

        tab1 = Frame(self.tabs)
        tab2 = Frame(self.tabs)
        tab3 = Frame(self.tabs)

        self.tabs.add(tab1, text="Tab One")
        self.tabs.add(tab2, text="Tab Two")
        self.tabs.add(tab3, text="Tab Three")
        self.tab(tab1, "tab1")
        self.tab(tab2, "tab2")
        self.tab(tab3, "tab3")
        self.tabs.pack()

    class tab(object):
        def __init__(self, root, name):
            self.name = name
            self.titles(root)

            Label(root, text="Low Threshold").grid(row=2, column=0)
            self.low_thresh = self.color(root, row=1, column=1)

            Separator(root, orient="horizontal").grid(row=4, sticky="ew", columnspan=7)

            Label(root, text="High Threshold").grid(row=6, column=0)
            self.hi_thresh = self.color(root, row=5, column=1)

            Separator(root, orient="horizontal").grid(row=8, sticky="ew", columnspan=7)

            Label(root, text="Color").grid(row=10, column=0)
            self.color = self.color(root, row=9, column=1)

            Separator(root, orient="horizontal").grid(row=12, sticky="ew", columnspan=7)

            Label(root, text="Epsilon").grid(row=13, column=0)
            self.epsilon = self.epsilon(root, row=13, column=1)

            Button(root, text="activate", command=self.activate).grid(row=14, column=0)

        def activate(self):
            effects[self.name] = PolygonEffect(
                low_thresh=self.get_RGB(self.low_thresh),
                hi_thresh=self.get_RGB(self.hi_thresh),
                color=self.get_RGB(self.color),
                epsilon=self.get_epsilon()
            )

        def get_epsilon(self):
            return FluctuatingValue(
                        self.epsilon.value.initial_value.get_value(),
                        self.epsilon.value.low_value.get_value(),
                        self.epsilon.value.high_value.get_value(),
                        self.epsilon.value.fluctuate.get_value(),
                        self.epsilon.value.function.get_value()
                ) 

        def get_RGB(self, attr):
            return [
                    self.get_fluct_for_color(attr.blue),
                    self.get_fluct_for_color(attr.green),
                    self.get_fluct_for_color(attr.red)
                ]

        def get_fluct_for_color(self, color):
            return FluctuatingValue(
                        color.initial_value.get_value(),
                        color.low_value.get_value(),
                        color.high_value.get_value(),
                        color.fluctuate.get_value(),
                        color.function.get_value()
                    )

        def titles(self, root):
            Label(root, text="default").grid(row=0, column=2)
            Label(root, text="low").grid(row=0, column=3)
            Label(root, text="high").grid(row=0, column=4)
            Label(root, text="enabled").grid(row=0, column=5)
            Label(root, text="function").grid(row=0, column=6)

        class color(object):
            def __init__(self, root, row, column):
                Label(root, text="R").grid(row=row, column=column)
                Label(root, text="G").grid(row=row+1, column=column)
                Label(root, text="B").grid(row=row+2, column=column)

                self.red = fluct(root, row=row, column=column+1)
                self.green = fluct(root, row=row+1, column=column+1)
                self.blue = fluct(root, row=row+2, column=column+1)

        class epsilon(object):
            def __init__(self, root, row, column):
                self.value = fluct(root, row=row, column=column+1)
