from sys import path
path.insert(0, "../Interface")
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values
from Webots_interface import Robot
R = Robot(values, positions, ALProxy)

