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

fftx = np.fft.fft(AccX)
Nx = AccX.size
fftx = np.abs(fftx)[:Nx // 2] * 1 / Nx
fftx = fftx/np.max(fftx[1:])
freqsx = np.fft.fftfreq(Nx, 0.03828600826884199)
freqsx = np.array([x for x in freqsx if x >= 0])

fftz = np.fft.fft(AccZ)
Nz = AccZ.size
fftz = np.abs(fftz)[:Nz // 2] * 1 / Nz
fftz = fftz/np.max(fftz[1:])
freqsz = np.fft.fftfreq(Nz, 0.03828600826884199)
freqsz = np.array([x for x in freqsz if x >= 0])

plt.figure()
plt.title("FFT of Accelerometers whilst Nao stays in position")
plt.ylabel("Normalised Amplitude")
plt.xlabel("Frequency (Hz)")
plt.xlim(0, 2)
plt.ylim(0, 1.2)
plt.plot(freqsx[1:], fftx[1:], "g", label = "X axis accelerometer")
plt.plot(freqsz[1:], fftz[1:], "m", label = "Z axis accelerometer")
plt.legend()
plt.show()