import scipy
import numpy as np
import matplotlib.pyplot as plt

SAMPLERATE, data = scipy.io.wavfile.read("./test_400_440_5sec.wav")

if data.ndim > 1:
    print("data is not mono")
    exit()

N_SAMPLES = len(data)

print("samplerate = ", SAMPLERATE)
print("n_samples = ", N_SAMPLES)
print("duration = ", N_SAMPLES / SAMPLERATE)
print("max freq = ", SAMPLERATE / 2)
print("bin size = ", SAMPLERATE / N_SAMPLES)

complex_fourier = scipy.fft.fft(data)
abs_fourier = np.abs(complex_fourier[:N_SAMPLES // 2])


freq = scipy.fft.fftfreq(N_SAMPLES, d=1/SAMPLERATE)
freq = freq[0:N_SAMPLES // 2]

plt.plot(freq, abs_fourier)
plt.show()

