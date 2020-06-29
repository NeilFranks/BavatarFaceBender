from tkinter import Tk
from tkinter.ttk import Notebook
from Tab import Tab


class PolygonControl(object):
    def __init__(self, root):
        self.notebook = Notebook(root)

        self.tabs = []

        self.tabs.append(Tab(self.notebook, 0, "tab1"))
        self.tabs.append(Tab(self.notebook, 1, "tab2"))
        self.tabs.append(Tab(self.notebook, 2, "tab3"))

        for tab in self.tabs:
            self.notebook.add(tab.get_tab(), text=tab.name.get())
            tab.load_tab()

        self.notebook.pack()


root = Tk()
PolygonControl(root)
root.mainloop()
