from sys import path
path.insert(0, "../Interface")
from robot_interface import Robot
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values


Robot = Robot(values, positions, ALProxy, "192.168.1.3", 9559)


def move_torso(angle=1, percent_max_speed=0.4):
    torso = {'RHP': 1.0, 'LHP': 1.0, 'RSP': 0.480417754569, 'LSP': 0.0496083550914, 'RSR': 1.12532637076, 'LSR': -1.10966057441, 'RER': -2.13838120104, 'LER': 2.18263145891, 'REY': -0.258485639687, 'LEY': 0.853785900783, 'RWY': 0.167101827676, 'LWY': -0.180156657963}
    for joint in torso:
        Robot.move_limbs(joint, angle*torso[joint]*0.0174533, percent_max_speed)


def move_legs(angle, percent_max_speed=0.4):
    legs = ['RKP', 'LKP']
    for joint in legs:
        Robot.move_limbs(joint, angle*0.0174533, percent_max_speed)

while True:
    key = raw_input("q = torso out\tw = torso in\to = legs in\tp = legs out\n")
    if key == "q":
        move_torso(5)
        print "Torso Out\n"
    elif key == "w":
        move_torso(-5)
        print "Torso In\n"
    elif key == "o":
        move_legs(5)
        print "Legs In\n"
    elif key == "p":
        move_legs(-5)
        print "Legs Out\n"
    else:
        print "Unrecognised Key"
