from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, 'single_pendulum')
from single_startup_const_period import Start
from single_acc_test import Acc_testXZ
from single_nothing import Nothing

class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)

        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=True, gyro_required=False)

        self.order = [ {'algo': Nothing,'duration': 10}, {'algo': Start,'duration': 60}, {'algo': Acc_testXZ,'duration': 30}]
