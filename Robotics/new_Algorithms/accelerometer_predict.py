from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, 'single_pendulum')
from single_nothing import Nothing
from acc_predict import Acc
class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)

        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=True, gyro_required=False)

        self.order = [
        {
			'algo': Nothing,
			'duration': 40
        },
        {
            'algo': Acc,
            'duration': 600
        }
        ]
