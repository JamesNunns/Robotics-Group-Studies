from naoqi import ALProxy
from positions_new import positions
from limb_data_2020 import values
import time

def set_posture(name_posture, max_speed=0.1):
    # Select posture from dictionary
    posture = positions[name_posture]
    # Import joint names
    names = [values[name][0] for name in posture.keys()]
    # Set initial stiffness
    motion.setStiffnesses(
        ["Head", "RArm", "LArm", "RLeg", "LLeg"], 1)
    # Start movement of each part
    for i in range(len(names)):
        motion.setAngles(names[i], list(posture.values())[i], max_speed)

tts = ALProxy("ALTextToSpeech", "192.168.1.3", 9559)
motion = ALProxy("ALMotion", "192.168.1.3", 9559)
motion.setStiffnesses(["Head", "RArm", "LArm", "RLeg", "LLeg"], 1)
# Turn off fall detector in webots
#motion.setMotionConfig( [["ENABLE_DISACTIVATION_OF_FALL_MANAGER", True]] )
#motion.setFallManagerEnabled(False)
tts.say("Connected!")

set_posture("extended", 0.05)

#for i in xrange(20):
    # Switch between crunched and extended
    #set_posture("crunched", 0.3)
    #time.sleep(1)
    #set_posture("extended", 0.3)
    #time.sleep(1)
#print motion.getSummary()
