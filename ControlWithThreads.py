from tkinter import Tk, StringVar, OptionMenu
import pyaudio

from Video import Video
import PolygonControl


class Control(object):
    def __init__(self, frame_rate=25):
        self.frame_rate = frame_rate

        # setup devices
        self.audio_devices = []
        self.clicked_audio_device = None  # will be the name of the device
        self.selected_audio_device = 2  # will be the number of the device

        self.root = Tk()
        self.root.configure(bg='black')
        self.video = Video(self.selected_audio_device)
        self.video.start()

        # load control panel
        self.load_controls()

        self.root.mainloop()

    def load_controls(self):
        self.devices_dropdown().pack()
        PolygonControl.effect(self).pack()

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
        return drop

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
        print(selected_audio_device)
        self.video.audio.change_device(selected_audio_device)


Control()
