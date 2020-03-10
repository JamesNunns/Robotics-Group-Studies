import pandas as pd
import time

from robot_interface import Robot
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values
from torso_and_legs import torso_dict, torso_speed, legs_dict, legs_speed


Robot = Robot(values, positions, ALProxy)

calls = np.linspace(100, 1000, 10)

##########
#Joint movement timing test
##########
times_JM = []
start_time_JM = time.time()
for i in range(10):
    for j in range(100):
        Robot.move_limbs('LKP', 0.0, 0.5)
    times.append(time.time()-start_time_JM)

##########
#Get Posture timing test
##########
times_GP = []
start_time_GP = time.time()
for i in range(10):
    for j in range(100):
        Robot.get_posture()
    times_GP.append(time.time()-start_time_GP)

##########
#Set Posture timing test
##########
times_SP = []
start_time_SP = time.time()
for i in range(10):
    for j in range(100):
        Robot.set_posture('current')
    times_SP.append(time.time()-start_time_SP)

##########
#Accelerometer timing test
##########
times_AC = []
start_time_AC = time.time()
for i in range(10):
    for j in range(100):
        Robot.get_acc(y):
    times.AC.append(time.time()-start_time_AC)


df = pd.DataFrame((calls, times_JM, times_GP, times_SP, times_AC), columns = ['calls', 'joints', 'get_p', 'set_p', 'set_a'])
df.to_csv("Nao_readout_timings")
