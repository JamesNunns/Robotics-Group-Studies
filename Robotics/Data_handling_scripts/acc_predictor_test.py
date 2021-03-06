import numpy as np
from scipy.signal import find_peaks
import time
import pandas as pd
import matplotlib.pyplot as plt
# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]

data = pd.read_csv("Sensor_change_pos.txt")

data.columns =["time", "", "", "","az", "","", "","", "","", "", "","", "","", "", ""]


def filt(fft, freq, tl, th):
    for i in xrange(len(freq)):
        if tl < np.abs(freq[i]) < th:
            fft[i] = fft[i]
        else:
            fft[i] = 0.0
    return fft

def convert(fft, freq):
    fft_conv = np.zeros(fft.size)
    for i in xrange(len(fft)):
        if fft[i] != 0.0:
            where = np.where(freq == min(freq, key=lambda x:abs(x-freq[np.argmax(fft)]/2)))[0][0]
            fft_conv[where] = fft[i]
            fft_conv[len(fft)-where] = np.conj(fft[i])
            break
    return fft_conv 

def acc_predict(all_data, tl=0.77, th=0.82):
    Time = np.array(all_data['time'])[-120:]
    rel_Time = Time - Time[0]
    AccZ = np.array(all_data['az'])[-120:]
    Tlist = []
    for i in xrange(len(rel_Time)-1):
        Tlist.append(rel_Time[i+1] - rel_Time[i])
    ts = sum(Tlist)/len(Tlist)
    fr = (1/ts)/120
    Nz = AccZ.size
    fftz = np.fft.fft(AccZ)
    freqsz = np.fft.fftfreq(Nz, ts)    
    fftz = filt(fftz, freqsz, tl, th)
    fft_conv = convert(fftz, freqsz)
    data = np.real(np.fft.ifft(fft_conv))
    plt.plot(Time, data)
    plt.title("Filtered Accelerometer Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Filtered Amplitude")
    peaks = find_peaks(data)[0]
    tp = []
    for i in xrange(len(rel_Time[peaks])-1):
        tp.append(rel_Time[peaks][i+1]-rel_Time[peaks][i])
    tp = np.mean(tp)
    e = (fr/(1/tp))*tp
    print e
    last_maxima = rel_Time[peaks][-1]+Time[0]
    next_5_maxima = []
    next_5_minima = []
    for i in xrange(5):
        next_5_maxima.append(last_maxima+(i+1)*tp)
        next_5_minima.append(last_maxima+(i+1)*tp - tp/2)
    return next_5_maxima, next_5_minima
acc_predict(data)