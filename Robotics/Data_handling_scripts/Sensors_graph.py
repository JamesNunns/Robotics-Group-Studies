import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, lfilter, find_peaks, fftconvolve





#functions defined from scipy cookbook to smooth functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def test_filter(time, values):
    # Filter requirements
    order = 6#strictness of filter
    fs = 1.0/np.mean(np.diff(time[-200:]))#sampling frequency
    lowcut = 0.5 # desired cutoff frequencies of the filter, Hz
    highcut = 1.50
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    smoothed_signal = lfilter(b, a, values)
    return smoothed_signal

def smooth(y, box_pts, edge):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode=edge)
    return y_smooth
    


##################################
#Read data from csv file
##################################
    
data = pd.read_csv("Sensor_test.csv")

Time = data['Time']

AccX = data['AccX']
AccY = data['AccY']
AccZ = data['AccZ']

GyrX = data['GyrX']
GyrY = data['GyrY']

AngX = data['AngX']
AngY = data['AngY']

Encoder = data['Encoder']


test = test_filter(Time, AngY)

Time_array = np.asarray(Time)
peaks = find_peaks(test)[0]
test_array = np.asarray(test)

args = [i for i in range(len(test)) if abs(test[i]) <= 0.007]




##################################
#Encoders
##################################

fig1, ax1 = plt.subplots()
#ax1.set_xlim(10, 60)

ax1.set_title('Unfiltered X Accelerometer')
ax1.set_xlabel('Time(s)')
ax1.set_ylabel('Encoder Reading(degrees)', color='cornflowerblue')
ax1.set_ylim( -50, 50)
ax1.plot(Time, Encoder, label = 'Swing Angle', color='cornflowerblue')
#ax1.plot(Time, AccX, color='cornflowerblue', linewidth=8)
ax1.axhline(y=0)
#ax1.plot(Time[args], Encoder[args], 'k.')


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
ylim = 0.3
ax2 = ax1.twinx()
ax2.set_ylabel('Sensor Values', color='orange')
#ax2.set_ylim(-ylim, ylim)
#ax2.plot(Time, smooth(AccZ, 20, 'same'), color='orange', linewidth=2)
ax2.plot(Time, AccX, color='orange', linewidth=2)
#ax2.plot(Time[peaks], test[peaks], 'k.')
#ax2.plot(Time[AngX_peaks], AngX[Ang_peaks], 'k.',label = 'Peaks')





