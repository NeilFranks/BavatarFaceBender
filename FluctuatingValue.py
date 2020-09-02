import utils


class FluctuatingValue(object):
    def __init__(self, initial_val, low_val, high_val, min_freq, max_freq, min_level, max_level, function, fluctuate_on):
        self.fluctuate_on = fluctuate_on

        # video
        self.current_val = initial_val
        self.low_val = low_val
        self.high_val = high_val

        # audio
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.min_level = min_level
        self.max_level = max_level

        self.fft_start_index = utils.hz_to_index(self.min_freq)
        self.fft_end_index = utils.hz_to_index(self.max_freq)

        '''
        function should be a lambda, like `lambda frac, whole: frac * whole`
        '''
        self.function = function

    def fluctuate_by_fraction(self, fraction):
        diff = self.high_val - self.low_val
        self.current_val = self.low_val + self.function(fraction, diff)

    def fluctuate(self):
        if self.fluctuate_on:
            self.fluctuate_by_fraction(
                self.get_fraction_from_fft(
                    self.fft_start_index,
                    self.fft_end_index,
                    self.min_level,
                    self.max_level
                )
            )

    def get_fraction_from_fft(self, start_index, end_index, min_level, max_level):
        # fraction should be between 0-1, calculated by where the peak is between min and max level
        sub_fft = utils.fft_out[start_index:end_index]
        peak = max(sub_fft)

        if peak < min_level:
            result = 0
        elif peak > max_level:
            result = 1
        else:
            diff = max_level - min_level
            result = (peak - min_level)/diff

        return result

    def get(self):
        return self.current_val
