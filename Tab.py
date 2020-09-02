from tkinter import Button, Entry, Frame, Label, LEFT, RIGHT, OptionMenu, StringVar
from tkinter.ttk import Separator
from FluctuatingValue import FluctuatingValue
from PolygonEffect import PolygonEffect
from ColorWidget import color_widget
from Epsilon import epsilon

import json
import utils


class Tab(object):
    def __init__(self, parent, index, name):
        self.parent = parent  # this will point to the notebook
        self.index = index  # so you can find this tab in the notebook
        self.name = StringVar()
        self.name.set(name)

        self.file_to_load = StringVar()

        self.root = Frame(parent)

    def load_tab(self):
        # add all the components
        self.name_entry(self.root).grid(row=0, column=0, columnspan=7)

        self.titles(self.root, row=1)

        Label(self.root, text="Low Threshold").grid(row=3, column=0)
        self.low_thresh = color_widget(self.root, row=2, column=1)

        Separator(self.root, orient="horizontal").grid(row=5, sticky="ew", columnspan=7)

        Label(self.root, text="High Threshold").grid(row=7, column=0)
        self.high_thresh = color_widget(self.root, row=6, column=1)

        Separator(self.root, orient="horizontal").grid(row=9, sticky="ew", columnspan=7)

        Label(self.root, text="Color").grid(row=11, column=0)
        self.color = color_widget(self.root, row=10, column=1)

        Separator(self.root, orient="horizontal").grid(row=13, sticky="ew", columnspan=7)

        Label(self.root, text="Epsilon").grid(row=14, column=0)
        self.epsilon = epsilon(self.root, row=14, column=1)

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
        Button(frame, text="activate", command=self.activate).grid(row=0, column=0)
        OptionMenu(frame, self.file_to_load, *utils.list_files()).grid(row=0, column=1)
        Button(frame, text="load", command=self.load).grid(row=0, column=2)
        Button(frame, text="save", command=self.save).grid(row=0, column=3)
        return frame

    def activate(self):
        utils.effects[self.name.get()] = PolygonEffect(
            low_thresh=self.get_RGB(self.low_thresh),
            high_thresh=self.get_RGB(self.high_thresh),
            color=self.get_RGB(self.color),
            epsilon=self.get_epsilon()
        )

    def load(self):
        data_object = json.loads(utils.load(self.file_to_load.get()))
        self.name.set(data_object["name"])
        self.low_thresh.from_dict(data_object["low thresh"])
        self.high_thresh.from_dict(data_object["high thresh"])
        self.color.from_dict(data_object["color"])
        self.epsilon.from_dict(data_object["epsilon"])

    def save(self):
        utils.save(self.name.get(), json.dumps(self.to_dict()))

    def to_dict(self):
        return {
            "name": self.name.get(),
            "low thresh": self.low_thresh.to_dict(),
            "high thresh": self.high_thresh.to_dict(),
            "color": self.color.to_dict(),
            "epsilon": self.epsilon.to_dict()
        }

    def get_epsilon(self):
        return FluctuatingValue(
                    initial_val=self.epsilon.value.initial_value.get_value(),
                    low_val=self.epsilon.value.low_value.get_value(),
                    high_val=self.epsilon.value.high_value.get_value(),
                    min_freq=self.epsilon.value.min_freq_entry.get_value(),
                    max_freq=self.epsilon.value.max_freq_entry.get_value(),
                    min_level=self.epsilon.value.min_level_entry.get_value(),
                    max_level=self.epsilon.value.max_level_entry.get_value(),
                    function=self.epsilon.value.function.get_value(),
                    fluctuate_on=self.epsilon.value.fluctuate.get_value()
            )

    def get_RGB(self, attr):
        return [
                self.get_fluct_for_color(attr.blue),
                self.get_fluct_for_color(attr.green),
                self.get_fluct_for_color(attr.red)
            ]

    def get_fluct_for_color(self, color):
        return FluctuatingValue(
                    initial_val=color.initial_value.get_value(),
                    low_val=color.low_value.get_value(),
                    high_val=color.high_value.get_value(),
                    min_freq=color.min_freq_entry.get_value(),
                    max_freq=color.max_freq_entry.get_value(),
                    min_level=color.min_level_entry.get_value(),
                    max_level=color.max_level_entry.get_value(),
                    function=color.function.get_value(),
                    fluctuate_on=color.fluctuate.get_value()
                )

    def titles(self, root, row):
        # video
        Label(root, text="default").grid(row=row, column=2)
        Label(root, text="low").grid(row=row, column=3)
        Label(root, text="high").grid(row=row, column=4)

        # audio
        Label(root, text="min freq (Hz)").grid(row=row, column=5)
        Label(root, text="max freq (Hz)").grid(row=row, column=6)
        Label(root, text="min level").grid(row=row, column=7)
        Label(root, text="max level").grid(row=row, column=8)

        Label(root, text="function").grid(row=row, column=9)
        Label(root, text="enabled").grid(row=row, column=10)
