import audioop
import pyaudio
import queue
import threading
import time


class Audio(threading.Thread):
    def __init__(self, device, chunk=2 ** 11, samplerate=44100, aScale=100, exponent=1):
        threading.Thread.__init__(self)
        self.stop = False  # set true to end thread

        '''
        INPUTS
        '''
        self.device = device
        self.chunk = chunk
        self.samplerate = samplerate
        self.aScale = aScale
        self.exponent = exponent

        if self.device == 2:
            self.raw_min = 0
            self.raw_max = 8582  # just my observed max and mins for system audio
        else:
            self.raw_min = float('inf')
            self.raw_max = float('-inf')

        self.relativeVolume = True  # if true, factors in raw_baseline when computing volume

        '''
        STUFF TO WORK WITH
        '''
        self.p = pyaudio.PyAudio()
        self.start_stream()

        '''
        OUTPUTS
        '''
        self.volume = 0

    def run(self):
        while not self.stop:
            data = self.stream.read(self.chunk)
            self.calculate_volume(data, self.relativeVolume)

    def change_device(self, new_device):
        if new_device != self.device:
            self.device = new_device
            self.start_stream()

    def calculate_volume(self, data, relativeVol):
        volume = audioop.rms(data, 2)
        print(volume)
        if volume < self.raw_min:
            self.raw_min = volume
        if volume > self.raw_max:
            self.raw_max = volume

        if relativeVol and self.raw_max > self.raw_min:
            rel_volume = volume - self.raw_min
            diff = self.raw_max - self.raw_min
            volume = rel_volume/diff

        self.volume = volume

    def get_volume(self):
        return self.volume

    def start_stream(self):
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.device,
        )


# audio = Audio(2)
# audio.start()
# while True:
#     print(audio.get_volume())
