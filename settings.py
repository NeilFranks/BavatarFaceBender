MIN_FREQ = 0  # in Hz. don't bother with any frequencies below this
MAX_FREQ = 1500  # in Hz. don't bother with any frequencies above this

# FWIW, I found my system audio had a baseline of about 40, and a max around 85
MIN_LEVEL = 40  # in mystery units on the fft (currently calculated by `10.0 * np.log10(abs(np.fft.rfft(arr)))`), the lowest level necessary to activate some effect
MAX_LEVEL = 85  # in mystery units on the fft (currently calculated by `10.0 * np.log10(abs(np.fft.rfft(arr)))`), the highest level necessary to activate some effect

CHUNK_SIZE = 2**14
SAMPLE_RATE = 44100
HZ_INDEX_CONSTANT = SAMPLE_RATE/CHUNK_SIZE  # for conversion between Hz and index on fft array 