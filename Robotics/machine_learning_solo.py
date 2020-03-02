from sys import path
path.insert(0, 'hidlibs')
import top_encoder.encoder_functions as BigEncoder

from robot_interface import Robot
from encoder_interface import Encoders
# from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values

import time

import ML
ml = ML()

# Robot = Robot(values, positions, ALProxy, "192.168.1.3", 9559)
# Encoders = Encoders(BigEncoder, SmallEncoders)


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
def move_torso(angle=1, percent_max_speed=0.4):
    torso = {'RHP': 1.0, 'LHP': 1.0, 'RSP': 0.480417754569, 'LSP': 0.0496083550914, 'RSR': 1.12532637076, 'LSR': -1.10966057441, 'RER': -2.13838120104, 'LER': 2.18263145891, 'REY': -0.258485639687, 'LEY': 0.853785900783, 'RWY': 0.167101827676, 'LWY': -0.180156657963}
    for joint in torso_dict:
        Robot.move_limbs(joint, angle*torso[joint]*0.0174533, percent_max_speed)

def move_legs(angle=1, percent_max_speed=0.4):
    legs = ['RKP', 'LKP']
    for joint in legs:
        Robot.move_limbs(joint, angle*0.0174533, percent_max_speed)

BigEncoder.calibrate()
angle_then = BigEncoder.getAngle()
time_then = time.time()

while time.time() - start_time < 600:
    angle_now, time_now = BigEncoder.getAngle(), time.time()
    ang_vel_now = (angle_now-angle_then)/(time_now-time_then)
    action = self.ml.get_action([ angle_now, ang_vel_now ])
    angle_then, time_then = angle_now, time_now
    if action == 0:
        "legs out -"
        self.move_legs(-1)
    elif action == 1:
        "legs in +"
        self.move_legs(1)
    elif action == 2:
        "torso out +"
        self.move_torso(1)
    elif action == 3:
        "torso in -"
        self.move_torso(-1)
    elif action == 4:
        pass
