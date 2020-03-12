import pandas as pd
import time
import numpy as np
from sys import path
path.insert(0, "../Interface")
from robot_interface import Robot
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values
from torso_and_legs import torso_dict, torso_speed, legs_dict, legs_speed


Robot = Robot(values, positions, ALProxy)

calls = np.linspace(100, 1000, 10)
joint_calls = np.linspace(10, 100, 10)

##########
#Joint movement timing test
##########
times_JM = []
start_time_JM = time.time()
for i in range(10):
    for j in range(10):
        Robot.move_limbs('LKP', 0.0, 0.5)
    times_JM.append(time.time()-start_time_JM)
print "joint movements done"
##########
#Get Posture timing test
##########
times_GP = []
start_time_GP = time.time()
for i in range(10):
    for j in range(100):
        Robot.get_posture()
    times_GP.append(time.time()-start_time_GP)
print "get posture done"
##########
#Set Posture timing test
##########
times_SP = []
start_time_SP = time.time()
for i in range(10):
    for j in range(10):
        Robot.set_posture('crunched', 'crunched')
    times_SP.append(time.time()-start_time_SP)
print "set posture done"
##########
#Accelerometer timing test
##########
times_AC = []
start_time_AC = time.time()
for i in range(10):
    for j in range(100):
        Robot.get_acc('y')
    times_AC.append(time.time()-start_time_AC)
print "accelerometer done"

pandas_data = {'calls':calls, 'joint_calls': joint_calls, 'joints':times_JM, 'get_p':times_GP, 'set_p':times_SP, 'set_a':times_AC}
df = pd.DataFrame(pandas_data)
df.to_csv("Nao_readout_timings")
