import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt, savgol_filter





#functions defined from scipy cookbook to smooth functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def final_filter(time, values):
    # Filter requirements.
    order = 6
    fs = 1.0/np.mean(np.diff(time[-200:]))
    lowcut = 0.5 # desired cutoff frequency of the filter, Hz
    highcut = 1.50
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    padded_signal = filtfilt(b, a, values)
    return padded_signal





data = pd.read_csv("Sensor_test.csv")

Time = data['Time']

AccX = data['AccX']
AccX_peaks = find_peaks(AccX, width=10)[0]

AccY = data['AccY']
AccZ = data['AccZ']


GyrX = data['GyrX']
GyrY = data['GyrY']


AngX = data['AngX']
AngY = data['AngY']

Encoder = data['Encoder']
Enc_peaks = find_peaks(Encoder)[0]



##################################
#Encoders
##################################
fig1, ax1 = plt.subplots()
ax1.set_xlim(10, 60)

ax1.set_xlabel('Time(s)')
ax1.set_ylabel('Encoder Reading(degrees)', color='cornflowerblue')
#ax1.set_ylim( ymin, ymax)
ax1.plot(Time, Encoder, label = 'Swing Angle', color='cornflowerblue')
#ax1.plot(Time[Enc_peaks], Encoder[Enc_peaks], 'k.',label = 'Peaks')


##################################
#Accelerometer
##################################
#ax2 = ax1.twinx()
#ax2.set_ylabel('Raw Accelerometer Values')
##ax2.set_ylim(-35, -25)
#ax2.plot(Time, AccX, 'r')
##ax2.plot(Time[AccX_peaks], AccX[AccX_peaks], 'k.',label = 'Peaks')


##################################
#Gyroscope
##################################
#ax2 = ax1.twinx()
#ax2.set_ylabel('Raw Gyroscope Values')
##ax2.set_ylim(-35, -25)
#ax2.plot(Time, GyrX, 'r')
##ax2.plot(Time[GyrX_peaks], GyrX[Gyr_peaks], 'k.',label = 'Peaks')


##################################
#Angles
##################################
ax2 = ax1.twinx()
ax2.set_ylabel('Raw Angle Values', color='orange')
#ax2.set_ylim(-35, -25)
ax2.plot(Time, final_filter(Time, AngY), color='orange')
#ax2.plot(Time[AngX_peaks], AngX[Ang_peaks], 'k.',label = 'Peaks')


