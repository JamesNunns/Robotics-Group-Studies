import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]

data = pd.read_csv("Sensor_test.txt")

Time = data['Time']

AccX = data['AccX']
AccY = data['AccY']
AccZ = data['AccZ']

GyrX = data['GyrX']
GyrY = data['GyrY']

AngX = data['AngX']
AngY = data['AngY']

Encoder = data['Encoder']

plt.figure()
plt.plot(Time, AccZ)

fftz = np.fft.fft(AccZ)
Nz = AccZ.size
freqsz = np.fft.fftfreq(Nz, 0.038)

def filt(fft, freq, tl, th):
    for i in xrange(len(freq)):
        if tl < np.abs(freq[i]) < th:
            fft[i] = fft[i]
        else:
            fft[i] = 0.0
    return fft

q = filt(fftz, freqsz, 0.78, 0.8)

data = np.real(np.fft.ifft(q))
plt.figure()
plt.title("FFT Filter of Z Accelerometer whilst Nao stays in position")
plt.plot(Time, Encoder, label = "Encoder Angle")
plt.plot(2*Time+0.31, data*8.1, label="Filtered Z Accelerometer")
plt.xlim(5, 20)
plt.ylim(-30, 30)
plt.ylabel(r"Swing angle $^{\circ}$")
plt.xlabel("Time (s)")
plt.legend()
plt.show()