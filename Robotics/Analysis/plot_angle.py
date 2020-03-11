import numpy as np 
import os
import matplotlib.pyplot as plt 
from graph_functions import *
from sys import path, argv
path.insert(0, "../Utility")
from utility_functions import read_file, get_latest_file, total_angle

print 'Saving plot'
#Collects the latest file name and the directory of the file  
filename, output_data_directory = get_latest_file('Analysis', test=False)
#Reads the file and collects the output data
angles = read_file(output_data_directory + filename)

t = angles['time'] #Collects the times of the data collection
be = angles['be'] #Collects the Big encoder data
position = angles['pos'] #Collects the postions of the Robot
algorithm = angles['algo'] #Collects the name of the Alogrithm

fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

plt.sca(ax) #Selects the plot
shade_background_based_on_algorithm(t, algorithm) #Changes the background dependant on the algo


plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")

plt.plot(t, be-be[0], label='Big Encoder', color='b')
#Sets x limit to the max time from the file
plt.xlim([0, max(t)])

plt.savefig('graphs/{}.png'.format(filename)) #Saves the graph to graph directory