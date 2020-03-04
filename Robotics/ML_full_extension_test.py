from Webots_interface import Robot
from naoqi import ALProxy
from positions_sym import positions
from limb_data_2020 import values


Robot = Robot(values, positions, ALProxy)

crunched_pos = positions['crunched']
extended_pos = positions['extended']
torso_list = {'RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY'}
hips = extended_pos['RHP'] - crunched_pos['RHP']
torso_dict = {}
for joint in torso_list:
    value = (extended_pos[joint] - crunched_pos[joint])/hips
    torso_dict[joint] = value

def move_torso(angle=1, percent_max_speed=0.5):
    for joint in torso_dict:
        Robot.move_limbs(joint, angle*torso_dict[joint]*0.0174533, percent_max_speed)


def move_legs(angle, percent_max_speed=0.5):
    legs = ['RKP', 'LKP']
    for joint in legs:
        Robot.move_limbs(joint, angle*0.0174533, percent_max_speed)

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
