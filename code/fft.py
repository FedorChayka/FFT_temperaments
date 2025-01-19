import scipy
import numpy as np
import matplotlib.pyplot as plt
import operator

# CONFIG ##############################################################
FREQ_CUTOFF_LOW = 40 # Hz
FREQ_CUTOFF_HIGH = 4000 # Hz
MIN_PEAK_DIST = 10 # Hz
TOP_PEAK_NUM = 50

DO_PLOTTING = False

# LOAD SOUND FILE #####################################################

SAMPLERATE, data = scipy.io.wavfile.read("../../FFT_data/test_music/397_meantone.wav")
#SAMPLERATE, data = scipy.io.wavfile.read("./test_400_440_5sec.wav")

if data.ndim > 1:
    print("data is not mono")
    exit()

N_SAMPLES = len(data)

print("samplerate = ", SAMPLERATE)
print("n_samples = ", N_SAMPLES)
print("duration = ", N_SAMPLES / SAMPLERATE)
print("max freq = ", SAMPLERATE / 2)
print("bin size = ", SAMPLERATE / N_SAMPLES)

# RUN FOURIER TRANSFORM ###############################################

complex_fourier = scipy.fft.fft(data)
abs_fourier = np.abs(complex_fourier[:N_SAMPLES // 2])

freq = scipy.fft.fftfreq(N_SAMPLES, d=1/SAMPLERATE)
freq = freq[0:N_SAMPLES // 2]

smooth_fourier = scipy.signal.savgol_filter(abs_fourier, 100, 3)

# frequency cutoffs:
abs_fourier = abs_fourier[round(FREQ_CUTOFF_LOW/(SAMPLERATE/N_SAMPLES)):round(FREQ_CUTOFF_HIGH/(SAMPLERATE/N_SAMPLES))]
smooth_fourier = smooth_fourier[round(FREQ_CUTOFF_LOW/(SAMPLERATE/N_SAMPLES)):round(FREQ_CUTOFF_HIGH/(SAMPLERATE/N_SAMPLES))]
freq = freq[round(FREQ_CUTOFF_LOW/(SAMPLERATE/N_SAMPLES)):round(FREQ_CUTOFF_HIGH/(SAMPLERATE/N_SAMPLES))]

# find peaks:
peaks,_ = scipy.signal.find_peaks(smooth_fourier, distance=round(MIN_PEAK_DIST/(SAMPLERATE / N_SAMPLES)))
# compute peak prominences:
peaks_prom = scipy.signal.peak_prominences(smooth_fourier, peaks)[0]
# sort peaks by prominence, write TOP_PEAK_NUM most prominent ones to top_peaks
sorted_peaks,_ = zip(*sorted(zip(peaks, peaks_prom), key=operator.itemgetter(1), reverse=True))
top_peaks = sorted_peaks[1:TOP_PEAK_NUM] # *indices* of top peaks

top_peaks_freq = [round(i*(SAMPLERATE / N_SAMPLES), 2) for i in top_peaks]

# PLOTTING ############################################################

if DO_PLOTTING:
    plt.plot(freq, abs_fourier)
    plt.plot(freq, smooth_fourier)
    for xc in [freq[i] for i in top_peaks]:
        plt.axvline(x=xc, color='red')
    plt.show()

# DATA OUTPUT #########################################################

np.savetxt('top_peaks.csv', (top_peaks, top_peaks_freq), delimiter=',',fmt='%.2f')
