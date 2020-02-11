from encoder_functions import getAngle, calibrate
import time
calibrate()
start = time.time()
angles = []
t_values = []
while time.time()-start < 1:
	angles.append(getAngle())
	t_values.append(time.time()-start)
print(angles)
