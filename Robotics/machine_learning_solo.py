from sys import path
path.insert(0, 'hidlibs')
import top_encoder.encoder_functions as BigEncoder
import pandas as pd

from robot_interface import Robot
from encoder_interface import Encoders
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values
import time
path.insert(0, "Training_functions")
import SmallEncoders

from ml import ML
ml = ML()

Robot = Robot(values, positions, ALProxy)
Encoders = Encoders(BigEncoder, SmallEncoders)


#creates dictionary of ratios required to move whole torso relative to hip movements
crunched_pos = positions['crunched']
extended_pos = positions['extended']
torso_list = {'RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY'}
hips = extended_pos['RHP'] - crunched_pos['RHP']
torso_dict = {}
for joint in torso_list:
    value = (extended_pos[joint] - crunched_pos[joint])/hips
    torso_dict[joint] = value



#functions to move either the legs or torso as a whole
def move_torso(angle, percent_max_speed=0.5):
    for joint in torso_dict:
        Robot.move_limbs(joint, angle*torso_dict[joint]*0.0174533, percent_max_speed)

def move_legs(angle, percent_max_speed=0.5):
    legs = ['RKP', 'LKP']
    for joint in legs:
        Robot.move_limbs(joint, angle*0.0174533, percent_max_speed)

BigEncoder.calibrate()
time.sleep(10)
angle_then = BigEncoder.getAngle()
start_time = time.time()
time_then = time.time()
l =[]

while time.time() - start_time < 60:
	if time.time() - start_time < 10:
		angle_now, time_now, ang_vel_now = BigEncoder.getAngle(), time.time() - start_time, 0.0
		k = (time_now, angle_now, ang_vel_now, 0)
		print k
		l.append(k)
	else:
		angle_now, time_now = BigEncoder.getAngle(), time.time() - start_time
		ang_vel_now = (angle_now-l[-5][1])/(time_now-l[-5][0])
		if ang_vel_now == 0.0:
			if l[-15][2] < 0:
				ang_vel_now = -1
			else:
				ang_vel_now = 1
		action = ml.get_action([ angle_now, ang_vel_now ])
		if action == 0:
			move_legs(500)
		elif action == 1:
			move_legs(-500)
		elif action == 2:
			move_torso(500)
		elif action == 3:
			move_torso(-500)
		elif action == 4:
			pass

		k = (time_now, angle_now, ang_vel_now, action)
		l.append(k)
		print k
		time.sleep(0.01)

df = pd.DataFrame(l, columns = ['time' , 'angle', 'ang_vel', 'net action'])
df.to_csv(r'with net 050320')

