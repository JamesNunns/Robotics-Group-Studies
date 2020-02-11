'''
python methods for get angle and
calibrate to zero for encoder(16-bit).
All angles are in degrees.
Authors: Will Etheridge and Will Edmundson

'''

from pmd import pmd1208fs

# Initialise the device
my_pmd = pmd1208fs()

# Initialise the cal_factor to zero degrees
calibration_factor = 0.0

'''
function that takes no arguaments and returns the angle
of the encoder
'''


def getAngle():
    global calibration_factor
    raw = my_pmd.digin16()
    raw2 = raw & 2047
    angle = float(raw2) * (360.0 / 2048.0) - calibration_factor
    
    if angle > 180:
        return angle - 360
    else:
        return angle


'''
a void function that takes no arguaments and calibrates
the encoder to zero
'''


def calibrate():
    global calibration_factor
    raw = my_pmd.digin16()
    raw2 = raw & 2047
    calibration_factor = float(raw2) * (360.0 / 2048.0)
    print(calibration_factor)


def filelokation():
    print(pmd1208fs.__file__)


def kill():
    global my_pmd
    del(my_pmd)
