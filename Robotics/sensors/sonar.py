from naoqi import ALProxy

IP = "192.168.1.3" # set your Ip address here
PORT = 9559

# Connect to ALSonar module.
sonarProxy = ALProxy("ALSonar", IP, PORT)

# Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
sonarProxy.subscribe("myApplication")

#Now you can retrieve sonar data from ALMemory.
memoryProxy = ALProxy("ALMemory", IP, PORT)

# Get sonar left first echo (distance in meters to the first obstacle).
lsonar = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
print(lsonar)

# Same thing for right.
rsonar = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
print(rsonar)
# Please read Sonar ALMemory keys section if you want to know the other values you can get.
