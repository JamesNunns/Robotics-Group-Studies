"""
Contains class that mocks how naoqi connects to robot etc, then interface
can run away from robot if this is imported as substitute for naoqi.

Contains:
    ALProxy
"""
from sys import path
path.insert(0, '../')
from limb_data import values

position = {}

class ALProxy():
    """
    Mock class to replace naoqi when not in lab
    """
    def __init__(self, name, ip, port):
        pass
        
    def say(self, word):
        """
        Prints in bold whatever Nao would normally say
        """
        print("\033[1mNAO: " + word + "\n \033[0m")

    def getData(self, key):
        if key in position.keys():
            return position[key]
        else:
            return 1

    def setStiffness(self, parts, stiffness):
        pass

    def setStiffnesses(self, parts, speed):
        pass

    def setAngles(self, names, angles, speed):KeyError: 'LHYP'

        """
        Adds angle being set to position dictionary, then can be accessed when it is called
        by ALProxy memory
        """
        for key in values.keys():
            if values[key][0] == names:
                position[values[key][1]] = angles

    def changeAngles(self, long_name, angle, percent_max_speed):
        
        position[long_name] += angle

    def setFallManagerEnabled(self, boolean):
        pass
    
    def getSummary(self):
		
		return '---------------------- Model ---------------------------\n       JointName   Stiffness     Command      Sensor\n         HeadYaw    0.000000    0.024502    0.024502\n       HeadPitch    0.000000    0.510311    0.514872\n  LShoulderPitch    1.000000    0.952572    0.955640\n   LShoulderRoll    1.000000    0.570606    0.552198\n       LElbowYaw    1.000000   -0.369736   -0.369736\n      LElbowRoll    1.000000   -1.092166   -1.055350\n       LWristYaw    1.000000   -1.248718   -1.264058\n           LHand    1.000000    0.000000    0.044000\n    LHipYawPitch    1.000000   -0.035240   -0.035240\n        LHipRoll    1.000000   -0.012230   -0.012230\n       LHipPitch    1.000000   -0.450954   -0.450954\n      LKneePitch    1.000000    1.050748    1.049214\n     LAnklePitch    1.000000    0.168698    0.168698\n      LAnkleRoll    1.000000    0.006178    0.006178\n    RHipYawPitch    0.000000   -0.035240   -0.035240\n        RHipRoll    1.000000    0.024586    0.024586\n       RHipPitch    1.000000   -0.481718   -0.481718\n      RKneePitch    1.000000    1.006346    1.006346\n     RAnklePitch    1.000000    0.293036    0.293036\n      RAnkleRoll    1.000000   -0.127280   -0.127280\n  RShoulderPitch    1.000000    0.869820    0.871354\n   RShoulderRoll    1.000000   -0.478650   -0.469446\n       RElbowYaw    1.000000    0.234660    0.233126\n      RElbowRoll    1.000000    1.004812    0.974132\n       RWristYaw    1.000000    1.457258    1.428112\n           RHand    1.000000    0.000000    0.024000\n---------------------- Tasks  --------------------------\n            Name          ID    BrokerID    Priority\n----------------- Motion Cycle Time --------------------\n              20 ms'
