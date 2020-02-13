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
def GyrRef():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrRef/Sensor/Value")
def GyrX():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
def GyrY():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
def AngX():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value")
def AngY():
	return memoryProxy.getData("Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value")

start = time.time()
l = []
while time.time()-start < 30:
	l.append(( time.time(), AccX(), AccY(), AccZ(), GyrRef(), GyrX(), GyrY(), AngX(), AngY() ))
	time.sleep(0.01)
times = [i[0] for i in l]
AccX_data = [i[1] for i in l]
AccY_data = [i[2] for i in l]
AccZ_data = [i[3] for i in l]
GyrRef_data = [i[4] for i in l]
GyrX_data = [i[5] for i in l]
GyrY_data = [i[6] for i in l]
AngX_data = [i[7] for i in l]
AngY_data = [i[8] for i in l]

times = [i-start for i in times]

df = pd.DataFrame(list(zip(times, AccX_data, AccY_data, AccZ_data, GyrRef_data, GyrX_data, GyrY_data, AngX_data, AngY_data)),
               columns =['Time', 'AccX', 'AccY', 'AccZ', 'GryRef', 'GyrX', 'GyrY', 'AngX', 'AngY'])

df.to_csv("Accelerometer_test")
