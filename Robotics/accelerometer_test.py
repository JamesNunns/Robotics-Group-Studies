from naoqi import ALProxy
import time
import pandas as pd

IP = "192.168.1.3" # set your Ip address here
PORT = 9559

# ====================
# Create proxy to ALMemory
memoryProxy = ALProxy("ALMemory", IP, PORT)

def AccX():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
def AccY():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
def AccZ():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")

start = time.time()
l = []
while time.time()-start < 30:
	l.append(((time.time()), AccX(), AccY(), AccZ()))
	time.sleep(0.01)
times = []
x = []
y = []
z = []
for i in l:
	times.append(i[0])
	x.append(i[1])	
	y.append(i[2])
	z.append(i[3])
	
times = [i-start for i in times]

df = pd.DataFrame(list(zip(times, x, y, z)), 
               columns =['Time', 'x', 'y', 'z'])

df.to_csv("Accelerometer_test")
