from limb_data_2020 import values
#from naoqi import ALProxy
#motionProxy = ALProxy("ALMotion", "192.168.1.3", 9559)

neutral = '---------------------- Model ---------------------------\n       JointName   Stiffness     Command      Sensor\n         HeadYaw    0.000000    0.024502    0.024502\n       HeadPitch    0.000000    0.510311    0.514872\n  LShoulderPitch    1.000000    0.952572    0.955640\n   LShoulderRoll    1.000000    0.570606    0.552198\n       LElbowYaw    1.000000   -0.369736   -0.369736\n      LElbowRoll    1.000000   -1.092166   -1.055350\n       LWristYaw    1.000000   -1.248718   -1.264058\n           LHand    1.000000    0.000000    0.044000\n    LHipYawPitch    1.000000   -0.035240   -0.035240\n        LHipRoll    1.000000   -0.012230   -0.012230\n       LHipPitch    1.000000   -0.450954   -0.450954\n      LKneePitch    1.000000    1.050748    1.049214\n     LAnklePitch    1.000000    0.168698    0.168698\n      LAnkleRoll    1.000000    0.006178    0.006178\n    RHipYawPitch    0.000000   -0.035240   -0.035240\n        RHipRoll    1.000000    0.024586    0.024586\n       RHipPitch    1.000000   -0.481718   -0.481718\n      RKneePitch    1.000000    1.006346    1.006346\n     RAnklePitch    1.000000    0.293036    0.293036\n      RAnkleRoll    1.000000   -0.127280   -0.127280\n  RShoulderPitch    1.000000    0.869820    0.871354\n   RShoulderRoll    1.000000   -0.478650   -0.469446\n       RElbowYaw    1.000000    0.234660    0.233126\n      RElbowRoll    1.000000    1.004812    0.974132\n       RWristYaw    1.000000    1.457258    1.428112\n           RHand    1.000000    0.000000    0.024000\n---------------------- Tasks  --------------------------\n            Name          ID    BrokerID    Priority\n----------------- Motion Cycle Time --------------------\n              20 ms'


new_name = raw_input("What would you like the posture to be called?\n{}".format('>'))

def GetPosture(summary):
    '''
    Returns the posture of NAO as a dictionary in the same format as the positions dictionary
    ------
    Parameters
    ------
    summary: list
        raw list using motionProxy.getSummary
    '''
    current_posture = {}
    summary = summary.split()
    summary = summary[7:-14]
    for i in range(len(summary)/4):
        for keys in values:
            if values[keys][0] == summary[4*i]:
                current_posture[keys] = summary[4*i + 3]
    return current_posture

#motionProxy.getSummary()
posture_now = neutral
posture_dict = GetPosture(posture_now)

with open("positions_new_COPY.py", "r") as read_file:
    lines = read_file.readlines()
with open("positions_new_COPY.py", "w") as vfile:
    vfile.writelines([item for item in lines[:-1]])
    vfile.write("\t'%s': {" % (new_name))
    for key, value in posture_dict.items():
		if key != 'LHYP' and key != 'LHR' and key != 'RHYP' and key != 'RHR':
			vfile.write("\n\t\t\'{}\':{},".format(key, value))
    vfile.write('}\n\n\t\t}')
