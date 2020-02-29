import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]

data = np.array(pd.read_csv("Sensor_change_pos.txt"))

Time = np.array([x[0] for x in data])
Time = Time - Time[0]
AccX = np.array([x[2] for x in data])
AccZ = np.array([x[4] for x in data])
Encoder = np.array([x[12] for x in data])
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

q = filt(fftz, freqsz, 0.77, 0.82)

data = np.real(np.fft.ifft(fftz))

plt.figure()
plt.title("FFT Filter of Z Accelerometer whilst Nao changes position")
plt.plot(Time, Encoder, label ="Encoder Angle")
#plt.figure(1)
#plt.plot(Time, AccZ)
plt.plot(2*Time+0.15, -data*25.5, label="Filtered Z Accelerometer")
plt.xlim(5, 20)
plt.ylim(-30, 30)
plt.ylabel(r"Swing angle $^{\circ}$")
plt.xlabel("Time (s)")
plt.legend()
plt.show()

