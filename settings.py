MIN_FREQ = 0  # in Hz. don't bother with any frequencies below this
MAX_FREQ = 1500  # in Hz. don't bother with any frequencies above this
MIN_LEVEL = 0  # in mystery units on the fft (currently calculated by `10.0 * np.log10(abs(np.fft.rfft(arr)))`), the lowest level necessary to activate some effect
MAX_LEVEL = 50  # in mystery units on the fft (currently calculated by `10.0 * np.log10(abs(np.fft.rfft(arr)))`), the highest level necessary to activate some effect
