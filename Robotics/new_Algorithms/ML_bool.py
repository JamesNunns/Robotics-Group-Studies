from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, '../Algo_conditions')
from single_startup_const_period import Start
from single_nothing_ml import Nothng_ML
from interface_machine_learning_bool import Machine_Learning_Bool


class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)

        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [ {'algo': Nothing_ML,'duration': 10}, {'algo': Machine_Learning_Bool,'duration': 600}]
