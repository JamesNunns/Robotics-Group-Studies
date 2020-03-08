from Webots_interface import Robot
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values
from torso_and_legs import torso_dict, legs_dict, torso_speed, legs_speed


Robot = Robot(values, positions, ALProxy)

def move_torso(angle=1, percent_max_speed=0.5):
    for joint in torso_dict:
        Robot.move_limbs(joint, angle*torso_dict[joint]*0.0174533, torso_speed[joint]*percent_max_speed)


def move_legs(angle, percent_max_speed=0.5):
    for joint in legs_dict:
        Robot.move_limbs(joint, legs_dict[joint]*angle*0.0174533, legs_speed[joint]*percent_max_speed)

while True:
    key = raw_input("q = torso out\tw = torso in\to = legs in\tp = legs out\n")
    if key == "q":
        move_torso(500)
        print "Torso Out\n"
    elif key == "w":
        move_torso(-500)
        print "Torso In\n"
    elif key == "o":
        move_legs(500)
        print "Legs In\n"
    elif key == "p":
        move_legs(-500)
        print "Legs Out\n"
    else:
        print "Unrecognised Key"
