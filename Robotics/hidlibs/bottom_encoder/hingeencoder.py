# angletest.py
#
# Authors: Mark Colclough & Max Elliott
#
# Test for MCP2210 USB-to-SPI bridge chip, here used to read out
# Avago/Broadcom AEAT-6012 magnetic angle encoder.
#                                              Mark Colclough, Feb 2108

# PYTHONPATH=/home/markc/mycode/mcp2210/sp python -i tst.py

# Necessary software
# ------------------
# The MCP2210 shows up as a USB HID (1 report, 64 bytes both ways). Hence:
# * udev rule to give user access to hidrawX device
# * The standard hidapi shared library  http://www.signal11.us/oss/hidapi/
# * Python ctypes binding for hidapi  https://github.com/apmorton/pyhidapi
#   (included here in hidlibs)
# * Python MCP2201 device driver https://github.com/ondra/mcp2210 with my
#   mods to make it work with the pyhidapi above (included here in hidlibs)
# * This code, which knows how to extract data from the angle encoder.

# Multiple chip selects on MCP2210
# --------------------------------
# Data sheet is not clear how you multiplex between chip selects. It appears that
# an SPI transaction takes all pins designated as CS from their idle_cs state to their
# active_cs state for the duration of the transaction. Hence disable CS lines by
# making their active_cs state the same as their idle_cs.

# Data format when reading AEAT-6012 using this SPI bridge
# --------------------------------------------------------
# We transfer out 2 bytes (any values, since the sensor does not use data input),
# and get 2 bytes back. Data arrive most significant bit first. The first bit is
# garbage because the sensor doesn't prepare data for the first clock pulse.
# The last 3 bits of the second byte are garbage because the sensor only sends 12 bits.
# Thus we interpret the 2 byte input as a 16-bit number, mask off the garbage bits
# with 0x7ff8, and shift right 3 places so the least significant bit of the reading
# has value 1.

# Error when restarting after interruption
# ----------------------------------------
# 0xf8 is USB transfer in progress.   bridge.cancel_transfer()  should clean things up
# Making a new device is more reliable though.

from device import MCP2210

# active_cs values for enabling different CS lines (a zero in the bit position
# takes the CS to zero when SPI is active)
CS0_ENABLE = 0xfffe
CS1_ENABLE = 0xfffd
# FailureToUnderstand
#CS2_ENABLE = 0xfffc
#CS3_ENABLE = 0xfffb

CS2_ENABLE = 0xfffb
CS3_ENABLE = 0xfff7

bridge = MCP2210(0x04d8, 0x00de)
print bridge.product_name

# Read the present bridge chip configuration and set things we care about
settings = bridge.chip_settings
settings.pin_designations[0] = 0x01  # 0x01 makes the pin a CS pin
settings.pin_designations[1] = 0x01
settings.pin_designations[2] = 0x01
settings.pin_designations[3] = 0x01
bridge.chip_settings = settings

# Read the present bridge chip SPI settings and set things we care about
transfer = bridge.transfer_settings
transfer.bit_rate = 20000  # could slow some more if problems with long wires.
# Clock idles high, data sampled on first edge (change on second)
transfer.spi_mode = 2
transfer.spi_tx_size = 2  # bytes per transfer
transfer.cs_data_delay = 0  # from CS to data (n * 100 us)
transfer.lb_cs_delay = 0   # last byte to CS de-assert
transfer.interbyte_delay = 0
transfer.idle_cs = 0xffff  # All CS lines idle in the high state
# Disable all CS lines by making their active state high also.
transfer.active_cs = 0xffff
bridge.transfer_settings = transfer

# Initialise the cal_factor to zero degrees
cal_factor0 = 0.0
cal_factor1 = 0.0
cal_factor2 = 0.0
cal_factor3 = 0.0

# Conversion of angle from the encoder data to degrees


def toDegrees(angle):
    degreeAngle = angle / 4095 * 360
    if degreeAngle > 180:
        return degreeAngle - 360
    if degreeAngle < -180:
        return degreeAngle + 360
    else:
        return degreeAngle

# Functions to get the raw data from the mcp2210. 0 to 3 represent the different encoders.
# This takes about 8ms per call, mostly in software layers rather than SPI transactions.
# Could be improved with a custom library, as there is a lot of nonsense in the mcp2210 lib.
# Return: encoder value in bytes


def getBytes0():
    transfer.active_cs = CS0_ENABLE
    bridge.transfer_settings = transfer
    ret = bridge.transfer('aa')
    return ((256 * ord(ret[0]) + ord(ret[1])) & 0x7ff8) >> 3


def getBytes1():
    transfer.active_cs = CS1_ENABLE
    bridge.transfer_settings = transfer
    ret = bridge.transfer('aa')
    return ((256 * ord(ret[0]) + ord(ret[1])) & 0x7ff8) >> 3


def getBytes2():
    transfer.active_cs = CS2_ENABLE
    bridge.transfer_settings = transfer
    ret = bridge.transfer('aa')
    return ((256 * ord(ret[0]) + ord(ret[1])) & 0x7ff8) >> 3


def getBytes3():
    transfer.active_cs = CS3_ENABLE
    bridge.transfer_settings = transfer
    ret = bridge.transfer('aa')
    return ((256 * ord(ret[0]) + ord(ret[1])) & 0x7ff8) >> 3

# Functions to get angles from encoders in degrees. It can only read from -180 to +180
# and will go from -180 to +180 if the angle gets that high. 0 to 3 represent the different encoders.
# Return: encoder value in degrees


def getAngle0():
    angleBytes = getBytes0()
    return toDegrees(float(angleBytes - cal_factor0))


def getAngle1():
    angleBytes = getBytes1()
    return toDegrees(float(angleBytes - cal_factor1))


def getAngle2():
    angleBytes = getBytes2()
    return toDegrees(float(angleBytes - cal_factor2))


def getAngle3():
    angleBytes = getBytes3()
    return toDegrees(float(angleBytes - cal_factor3))

# Function to get all encoder angles in degrees.
# Return: all encoder angles in degrees in a 4x1 array


def getAngles():
    ang0 = getAngle0()
    ang1 = getAngle1()
    ang2 = getAngle2()
    ang3 = getAngle3()
    return [ang0, ang1, ang2, ang3]

# Combines the two angles on one side of the swing to produce the full hinge value
# Return: Full angle of hinge in degrees


def getAngleRight():
    ang1 = getAngle0()
    ang2 = getAngle1()
    return ang1 - ang2


def getAngleLeft():
    ang2 = getAngle2()
    ang3 = getAngle3()
    return ang2 - ang3

# Calibrate function: sets the current position of the encoder to 0.


def calibrate():
    global cal_factor0
    global cal_factor1
    global cal_factor2
    global cal_factor3
    cal_factor0 = getBytes0()
    cal_factor1 = getBytes1()
    cal_factor2 = getBytes2()
    cal_factor3 = getBytes3()
