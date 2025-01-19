
import scipy
import numpy as np
import operator

# LOAD SOUND FILE #####################################################

def load_file(dir):
    SAMPLERATE, data = scipy.io.wavfile.read(dir)

    if data.ndim > 1:
        print("data is not mono")
        exit()

    N_SAMPLES = len(data)

    print("samplerate = ", SAMPLERATE)
    print("n_samples = ", N_SAMPLES)
    print("duration = ", N_SAMPLES / SAMPLERATE)
    print("max freq = ", SAMPLERATE / 2)
    print("bin size = ", SAMPLERATE / N_SAMPLES)

    return data, SAMPLERATE

# RUN FOURIER TRANSFORM ###############################################

def run_fourier(data, sample_rate, smoothing=True, freq_cutoff=False, frq_low=0, frq_high=1):
    complex_fourier = scipy.fft.fft(data)
    abs_fourier = np.abs(complex_fourier[:len(data) // 2])

    freq = scipy.fft.fftfreq(len(data), d=1/sample_rate)
    freq = freq[0:len(data) // 2]

    if freq_cutoff:
        freq = freq[round(frq_low/(sample_rate/len(data))):round(frq_high/(sample_rate/len(data)))]
        abs_fourier = abs_fourier[round(frq_low/(sample_rate/len(data))):round(frq_high/(sample_rate/len(data)))]
    
    if smoothing:
        smooth_fourier = scipy.signal.savgol_filter(abs_fourier, 100, 3)
        return freq, smooth_fourier
    else:
        return freq, abs_fourier
    

def find_top_peaks(data, sample_rate, peak_num, peak_dist): # peak dist in Hz
    # find peaks:
    peaks,_ = scipy.signal.find_peaks(data, distance=round(peak_dist/(sample_rate / len(data))))
    # compute peak prominences:
    peaks_prom = scipy.signal.peak_prominences(data, peaks)[0]
    # sort peaks by prominence, write most prominent ones to top_peaks
    sorted_peaks,_ = zip(*sorted(zip(peaks, peaks_prom), key=operator.itemgetter(1), reverse=True))
    top_peaks = sorted_peaks[1:peak_num] # *indices* of top peaks

    top_peaks_freq = [round(i*(sample_rate / len(data)), 2) for i in top_peaks]

    return top_peaks, top_peaks_freq



data, sample_rate = load_file("../../FFT_data/test_music/397_meantone.wav", )
freq, fourier = run_fourier(data, sample_rate, smoothing=False, freq_cutoff=True, frq_low=40, frq_high=4000)
_, smooth_fourier = run_fourier(data, sample_rate, smoothing=True, freq_cutoff=True, frq_low=40, frq_high=4000)

peaks, peaks_freq = find_top_peaks(smooth_fourier, sample_rate, peak_num=50, peak_dist=10)
np.savetxt('top_peaks.csv', (peaks, peaks_freq), delimiter=',',fmt='%.2f')

import matplotlib.pyplot as plt

plt.plot(freq, fourier)
plt.plot(freq, smooth_fourier)
for xc in [freq[i] for i in peaks]:
    plt.axvline(x=xc, color='red')
plt.show()
