from tkinter import Button, Entry, Frame, Label, LEFT, RIGHT, StringVar
from tkinter.ttk import Separator
from FluctuatingValue import FluctuatingValue
from FluctuatingValueControl import FluctuatingValueControl
from PolygonEffect import PolygonEffect
from Video import effects

import json
import pickle


class Tab(object):
    def __init__(self, parent, index, name):
        self.parent = parent  # this will point to the notebook
        self.index = index  # so you can find this tab in the notebook
        self.name = StringVar()
        self.name.set(name)

        self.root = Frame(parent)

    def load_tab(self):
        # add all the components
        self.name_entry(self.root).grid(row=0, column=0, columnspan=7)

        self.titles(self.root, row=1)

        Label(self.root, text="Low Threshold").grid(row=3, column=0)
        self.low_thresh = self.color_widget(self.root, row=2, column=1)

        Separator(self.root, orient="horizontal").grid(row=5, sticky="ew", columnspan=7)

        Label(self.root, text="High Threshold").grid(row=7, column=0)
        self.hi_thresh = self.color_widget(self.root, row=6, column=1)

        Separator(self.root, orient="horizontal").grid(row=9, sticky="ew", columnspan=7)

        Label(self.root, text="Color").grid(row=11, column=0)
        self.color = self.color_widget(self.root, row=10, column=1)

        Separator(self.root, orient="horizontal").grid(row=13, sticky="ew", columnspan=7)

        Label(self.root, text="Epsilon").grid(row=14, column=0)
        self.epsilon = self.epsilon(self.root, row=14, column=1)

        self.button_menu(self.root).grid(row=15, column=0, columnspan=7)

    def get_tab(self):
        return self.root

    def name_entry(self, root):
        frame = Frame(root)

        Label(frame, text="effect name: ").pack(side=LEFT)

        # "focusout" validation means it will call the validate command when you click on another object on the panel
        Entry(frame, textvariable=self.name, validate="focusout", validatecommand=self.change_name).pack(side=RIGHT)

        return frame

    def change_name(self, **args):
        self.parent.tab(self.index, text=self.name.get())
        return True  # supposedly I have to return Bool because I'm cheating and using validation method

    def button_menu(self, root):
        frame = Frame(root)
        Button(frame, text="activate", command=self.activate).pack(side=LEFT)
        Button(frame, text="save", command=self.save).pack(side=RIGHT)
        return frame

    def activate(self):
        effects[self.name.get()] = PolygonEffect(
            low_thresh=self.get_RGB(self.low_thresh),
            hi_thresh=self.get_RGB(self.hi_thresh),
            color=self.get_RGB(self.color),
            epsilon=self.get_epsilon()
        )

    def save(self):
        print(json.dumps(self.to_dict()))

    def to_dict(self):
        return {
            "name": self.name.get(),
            "low thresh": self.low_thresh.to_dict(),
            "high thresh": self.hi_thresh.to_dict(),
            "color": self.color.to_dict(),
            "epsilon": self.epsilon.to_dict()
        }

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

    def titles(self, root, row):
        Label(root, text="default").grid(row=row, column=2)
        Label(root, text="low").grid(row=row, column=3)
        Label(root, text="high").grid(row=row, column=4)
        Label(root, text="enabled").grid(row=row, column=5)
        Label(root, text="function").grid(row=row, column=6)

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
                "green": self.red.to_dict(),
                "blue": self.red.to_dict(),
            }

    class epsilon(object):
        def __init__(self, root, row, column):
            self.value = FluctuatingValueControl(root, row=row, column=column+1)

        def to_dict(self):
            return {
                "value": self.value.to_dict(),
            }
