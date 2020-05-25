from tkinter import *
import pyaudio

class Control(object):
    def __init__(self):
        self.devices = []
        self.clicked_device = None # will be the name of the device
        self.selected_device = 0  # will be the number of the device
        
        self.setup()
    
    def setup(self):
        root = Tk()
        root.configure(bg='black')
        root.geometry('200x400')

        def myClick():
            myLabel = Label(root, text="Look! I clicked a Button!!", fg='white', bg='black')
            myLabel.pack()

        myButton = Button(root, text="Click Me!", command=myClick, fg='white', highlightbackground='black')
        myButton.pack()

        self.devices_dropdown(root)

        root.mainloop()

    def devices_dropdown(self, canvas):

        # list audio input devices
        p = pyaudio.PyAudio()
        i = 0
        n = p.get_device_count()

        while i < n:
            device = p.get_device_info_by_index(i)
            if device['maxInputChannels'] > 0:
                self.devices.append((device['name'], i))
            i += 1

        options = [device[0] for device in self.devices]

        self.clicked_device = StringVar() 
        self.clicked_device.set(options[0])

        drop = OptionMenu(canvas, self.clicked_device, *options)
        drop.config(bg='black', fg='white')
        drop.pack()

        def show():
            Label(canvas, text=self.clicked_device.get(), fg='white', bg='black').pack()
            print(self.get_selected_device())
        Button(canvas, text="Show Selection", command=show, fg='white', highlightbackground='black').pack()

    def get_selected_device(self):
        selected_device = None
        selected_device_name = self.clicked_device.get()

        for device in self.devices:
            if device[0] == selected_device_name:
                selected_device = device[1]

        return selected_device


    
Control()