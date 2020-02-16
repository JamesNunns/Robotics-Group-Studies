from encoder_functions import getAngle, calibrate
import time
import pandas as pd

calibrate()
start = time.time()
l = []
while time.time()-start < 600:
	l.append(((time.time()), getAngle()))

times = []
angles = []

for i in l:
	times.append(i[0])
	angles.append(i[1])	

times = [i-start for i in times]

df = pd.DataFrame(list(zip(times, angles)), 
               columns =['Time', 'angle'])

df.to_csv("damping_data") 
