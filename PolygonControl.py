from tkinter import Frame
from tkinter.ttk import Notebook


def effect(control):
    root = control.root
    note = Notebook(root)

    tab1 = Frame(note)
    tab2 = Frame(note)
    tab3 = Frame(note)

    note.add(tab1, text="Tab One")
    note.add(tab2, text="Tab Two")
    note.add(tab3, text="Tab Three")
    return note

