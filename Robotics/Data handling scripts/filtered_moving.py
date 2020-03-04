import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]

data = np.array(pd.read_csv("Sensor_change_pos.txt"))

Time = np.array([x[0] for x in data])[0:120]
Time = Time - Time[0]
AccX = np.array([x[2] for x in data])[0:120]
AccZ = np.array([x[4] for x in data])[0:120]
Encoder = np.array([x[12] for x in data])[0:120]
fftz = np.fft.fft(AccZ)
Nz = AccZ.size

Tlist = []
for i in xrange(len(Time)-1):
    Tlist.append(Time[i+1] - Time[i])
ts = sum(Tlist)/len(Tlist)

freqsz = np.fft.fftfreq(Nz, ts)

def filt(fft, freq, tl, th):
    for i in xrange(len(freq)):
        if tl < np.abs(freq[i]) < th:
            fft[i] = fft[i]
        else:
            fft[i] = 0.0
    return fft

fftz_2 = np.copy(fftz)

fftz = filt(fftz, freqsz, 0.77, 0.82)
fftz_2 = filt(fftz_2, freqsz, 0.38, 0.41)
fft_conv = np.zeros(fftz.size)

for i in xrange(len(fftz)):
    if fftz[i] != 0.0:
        where = np.where(freqsz == min(freqsz, key=lambda x:abs(x-freqsz[np.argmax(np.abs(fftz))]/2)))[0][0]
        fft_conv[where] = fftz[i]
        fft_conv[len(fftz)-where] = np.conj(fftz[i])
        break

data = np.real(np.fft.ifft(fft_conv))
data_2 = np.real(np.fft.ifft(fftz_2))

A_factor = max(Encoder)/max(data)
A_factor_2 = max(Encoder)/max(data_2)

t_factor = Time[np.argmax(data)] - Time[np.argmax(Encoder)]

plt.figure()
plt.title("FFT Filter of Z Accelerometer whilst Nao changes position")
#plt.plot(Time, Encoder, label ="Encoder Angle")
#plt.figure(1)
#plt.plot(Time, AccZ)
#plt.plot(Time, data_2, label="Filtered Z Accelerometer from 0.4Hz")
plt.plot(Time, data, label="Filtered Z Accelerometer from 0.8Hz halved")
#plt.ylim(-30, 30)
#plt.xlim(5, 13)
#plt.ylabel(r"Swing angle $^{\circ}$")
plt.xlabel("Time (s)")
plt.legend()
plt.show()

