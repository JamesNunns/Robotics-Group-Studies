# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:10:29 2020

@author: golda
"""
import numpy as np
import matplotlib.pyplot as plt

#opening the file and reading in the data
Angle_list = []
Angle_changes = []
Time_changes = []
textfile = open(r"C:\Users\golda\Robotics-Group-Studies\Simulation\SwingAmplitude.txt")
lines = textfile.readlines()
lines[0].split()
for i in range(0, len(lines[0].split())):
    Angle_list.append(float(lines[0].split()[i]))
    
#Finding the peak amplitude values
#for i in range(0, len(Angle_list)):
#    if Angle_list[i] >= 0:
#        
#        if abs(Angle_list[i]) == abs(Angle_list[i-1]):
#            if abs(Angle_list[i]) > abs(Angle_list[i-2]) and abs(Angle_list[i]) > abs(Angle_list[i+1]):
#                Angle_changes.append(abs(Angle_list[i]))
#                Time_changes.append(i/30)
#                
#        else:
#            if abs(Angle_list[i]) > abs(Angle_list[i-1]) and abs(Angle_list[i]) > abs(Angle_list[i+1]):
#                Angle_changes.append(abs(Angle_list[i]))
#                Time_changes.append(i/7.5)
        
for i in range(0, len(Angle_list)):
    Time_changes.append(i/30)

#plotting the data
plt.plot(Time_changes, Angle_list)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (degrees)")
plt.title("How the amplitude of the swing decays over time with no stimulation")


plt.savefig("Swing amplitude damping")
textfile.close()


#string anglevalue = (rod.angle + 25).ToString() + " ";
#
#		File.AppendAllText(@"C:\Users\golda\Robotics-Group-Studies\Simulation\SwingAmplitude.txt", anglevalue);
#
#		Time.timeScale = 4;




