from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, '../Algo_conditions')
from interface_machine_learning_full_movement import Machine_Learning
from single_nothing_ml import Nothing_ML

class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [{'algo':Nothing_ML, 'duration':10}, {'algo':Machine_Learning, 'duration': 600}]
