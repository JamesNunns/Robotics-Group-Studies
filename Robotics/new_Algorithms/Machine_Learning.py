from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, 'single_pendulum')
from single_machine_learning import Machine_Learning
from single_nothing import Nothing

class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [{'algo':Nothing, 'duration':10}, {'algo':Machine_Learning, 'duration': 600}]
        
