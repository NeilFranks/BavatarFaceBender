from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import pyaudio
import concurrent.futures
from multiprocessing.pool import ThreadPool
from EmbeddedVideo import EmbeddedVideo


class DemoControl(object):
    def __init__(self, frame_rate=25):
        self.frame_rate = frame_rate

        # setup devices
        self.audio_devices = []
        self.clicked_audio_device = None  # will be the name of the device
        self.selected_audio_device = 0  # will be the number of the device

        self.root = Tk()
        self.root.configure(bg='black')
        self.video = EmbeddedVideo()

        # load control panel
        self.load_controls()

        # load initial image
        image = self.get_frame()
        self.panelA = Label(image=image)
        self.panelA.image = image
        self.panelA.pack()

        self.run()

    def run(self):
        self.root.after(1000//self.frame_rate, self.display_frame)
        self.root.mainloop()

    def display_frame(self):
        image = self.get_frame()
        self.panelA.configure(image=image)
        self.panelA.image = image
        self.root.after(1000//self.frame_rate, self.display_frame)

    def get_frame(self):
        image = self.video.get_frame()

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # convert the images to PIL format...
        image = Image.fromarray(image)
        # ...and then to ImageTk format
        return ImageTk.PhotoImage(image)

    def load_controls(self):
        self.devices_dropdown()

    def devices_dropdown(self):

        # list audio input devices
        p = pyaudio.PyAudio()
        i = 0
        n = p.get_device_count()

        while i < n:
            device = p.get_device_info_by_index(i)
            if device['maxInputChannels'] > 0:
                self.audio_devices.append((device['name'], i))
            i += 1

        options = [device[0] for device in self.audio_devices]

        self.clicked_device = StringVar()
        self.clicked_device.set(options[0])

        drop = OptionMenu(
            self.root,
            self.clicked_device,
            *options,
            command=self.change_device
        )
        drop.config(bg='black', fg='white')
        drop.pack()

    def get_selected_audio_device(self):
        selected_audio_device = None
        selected_audio_device_name = self.clicked_device.get()

        for device in self.audio_devices:
            if device[0] == selected_audio_device_name:
                selected_audio_device = device[1]

        return selected_audio_device

    def change_device(self, device_name):
        for device in self.audio_devices:
            if device[0] == device_name:
                selected_audio_device = device[1]
        self.video.audio.change_device(selected_audio_device)


DemoControl()
