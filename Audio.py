import audioop
import math
import numpy as np
import pyaudio as pa
import threading
import settings


class Audio(threading.Thread):
    def __init__(self, device, chunk=2**14, samplerate=44100, aScale=100, exponent=1):
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

        self.raw_min = float('inf')
        self.raw_max = float('-inf')
        self.relativeVolume = True  # if true, factors in raw_baseline when computing volume

        '''
        STUFF TO WORK WITH
        '''
        self.p = pa.PyAudio()
        self.start_stream()

        # fft things
        self.hz_index_constant = samplerate/chunk  # for conversion
        self.min_freq = settings.MIN_FREQ  # in Hz. don't bother with any frequencies below this
        self.max_freq = settings.MAX_FREQ  # in Hz. don't bother with any frequencies above this
        self.fft_start_index = math.floor(self.hz_to_index(self.min_freq))
        self.fft_end_index = math.ceil(self.hz_to_index(self.max_freq))

        '''
        OUTPUTS
        '''
        self.volume = 0

    def run(self):
        while not self.stop:
            self.data = self.stream.read(self.chunk)
            self.fft()

    def change_device(self, new_device):
        if new_device != self.device:
            self.device = new_device
            self.start_stream()
            self.reset_min_max()

    def calculate_volume(self):
        # this method SHOULD return a fraction between 0 and 1.
        # Fluctuating values kinda depend on that
        data = self.data
        relativeVol = self.relativeVolume

        volume = audioop.rms(data, 2)
        if volume < self.raw_min:
            self.raw_min = volume
        if volume > self.raw_max:
            self.raw_max = volume

        if relativeVol and self.raw_max > self.raw_min:
            rel_volume = volume - self.raw_min
            diff = self.raw_max - self.raw_min
            volume = rel_volume/diff

        self.volume = volume
        return volume

    def fft(self):
        arr = np.fromstring(self.data, np.int16)
        fft_out = 10.0 * np.log10(abs(np.fft.rfft(arr)))
        self.fft_out = fft_out[self.fft_start_index:self.fft_end_index]

    def hz_to_index(self, hz):
        return hz/self.hz_index_constant

    def index_to_hz(self, index):
        return index*self.hz_index_constant

    def reset_min_max(self):
        self.raw_min = float('inf')
        self.raw_max = float('-inf')
        # if self.device == 2:
        #     self.raw_min = 0
        #     self.raw_max = 8582  # just my observed max and min for system audio
        # else:
        #     self.raw_min = float('inf')
        #     self.raw_max = float('-inf')

    def start_stream(self):
        self.stream = self.p.open(
            format=pa.paInt16,
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
