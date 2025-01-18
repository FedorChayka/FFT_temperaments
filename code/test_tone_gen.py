
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write

SAMPLE_RATE = 44100  # Hertz

def gen_time(duration, sample_rate=SAMPLE_RATE):
    return np.linspace(0, duration, sample_rate * duration, endpoint=False)

def gen_sine(freq, duration, sample_rate=SAMPLE_RATE):
    frequencies = freq * gen_time(duration, sample_rate)
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return y

def normalize(tone):
    return np.int16((tone / tone.max()) * 32767)

tone = normalize(gen_sine(400, 5) + gen_sine(440, 5))

write("test_400_440_5sec.wav", SAMPLE_RATE, tone)

#plt.plot(np.linspace(0, 5, SAMPLE_RATE * 5, endpoint=False), tone)
#plt.show()
