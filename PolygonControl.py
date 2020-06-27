from tkinter import Frame, Button
from tkinter.ttk import Notebook


def effect(control):
    root = control.root
    note = Notebook(root)

    tab1 = Frame(note)
    tab2 = Frame(note)
    tab3 = Frame(note)
    Button(tab1, text='Exit', command=lambda: exit(control)).pack(padx=100, pady=100)

    note.add(tab1, text="Tab One")
    note.add(tab2, text="Tab Two")
    note.add(tab3, text="Tab Three")
    return note


def exit(control):
    control.video.stop = True
    control.video.join()
    control.root.destroy()
