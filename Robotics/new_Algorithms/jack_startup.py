from robot_interface import Robot
from encoder_interface import Encoders
from sys import path
path.insert(0, 'single_pendulum')
from single_nothing import Nothing
path.insert(0,'Triple_pendulum')
from triple_startup import Triple
from triple_incrase_period import TripleIncrease
from triple_maintain import Maintain

class Algorithm(Robot, Encoders):

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):

        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [
        {        
            'algo': Nothing,
            'duration': 10
        },{        
            'algo': Triple,
            'duration': 30
        },{
            'algo': TripleIncrease,
            'duration' : 30
        },{
            'algo': Maintain,
            'duration' : 30
        }
        ]