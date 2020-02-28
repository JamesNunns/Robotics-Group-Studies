import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]

data = np.array(pd.read_csv("Sensor_change_pos.txt"))

Time = np.array([x[0] for x in data])
AccX = np.array([x[2] for x in data])
AccZ = np.array([x[4] for x in data])
Encoder = np.array([x[12] for x in data])
Time = Time - Time[0]

fftx = np.fft.fft(AccX)
Nx = AccX.size
fftx = np.abs(fftx)[:Nx // 2] * 1 / Nx
fftx = fftx/np.max(fftx[1:])

Tlistx = []
for i in xrange(len(Time)-1):
    Tlistx.append(Time[i+1] - Time[i])
ts = sum(Tlistx)/len(Tlistx)

freqsx = np.fft.fftfreq(Nx, ts)
freqsx = np.array([x for x in freqsx if x >= 0])

fftz = np.fft.fft(AccZ)
Nz = AccZ.size
fftz = np.abs(fftz)[:Nz // 2] * 1 / Nz
fftz = fftz/np.max(fftz[1:])

Tlistz = []
for i in xrange(len(Time)-1):
    Tlistz.append(Time[i+1] - Time[i])
ts = sum(Tlistz)/len(Tlistz)

freqsz = np.fft.fftfreq(Nz, ts)
freqsz = np.array([x for x in freqsz if x >= 0])



plt.figure()
plt.title("FFT of Accelerometers whilst Nao changes position")
plt.plot(freqsx[1:], fftx[1:], label = "X axis accelerometer", color = "g")
plt.ylabel("Normalised Amplitude")
plt.xlabel("Frequency (Hz)")
plt.plot(freqsz[1:], fftz[1:], label = "Z axis accelerometer", color = "m")
plt.xlim(0, 2)
plt.ylim(0, 1.2)
plt.legend()
plt.show()