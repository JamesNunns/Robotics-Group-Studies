# angletest.py    python 2.7 or 3 version
# 
# Test for MCP2210 USB-to-SPI bridge chip, here used to read out
# Avago/Broadcom AEAT-6012 magnetic angle encoder.
#                                              Mark Colclough, Feb 2018-2020

# Necessary software
# ------------------
# Support for this device is an utter mess. There are multiple incompatible
# python hid libraries with clashing names, and multiple botched forks of
# mcp2210, for various Python versions, all mutually incompatible.
# The instructions below  work on Ubuntu 18, 2020, but it would be better
# to redo the whole thing and bypass the hid handling.
# Upstreams are:
#       https://github.com/trezor/cython-hidapi
#       https://github.com/arachnidlabs/mcp2210/  for the py2 version
#       https://github.com/rdpoor/mcp2210  for the py3 version
# Note that neither python-hid nor python-hidapi from Ubuntu repos is helpful.

# For Python 2.7
# * udev rule to give user access to device: 80-microchip.rules
# * pip install --user mcp2210   Build requires libudev-dev, maybe more, e.g. python-dev libusb-1.0-0-dev libudev-dev
#     This should get mcp2210-0.1.4  and  hidapi-0.9.0.post2.

# For Python 3.6
# * udev rule to give user access to device: 80-microchip.rules
# * pip3 install --user hidapi     gets hidapi-0.9.0.post2  as above
# * pip3 install --user rdpoor-mcp2210-master/  (get zip from github and unzip locally because mcp2210 from pypi is py2 only)
#      this gets mcp2210 0.1.5 (commit 2015992, Nov 18, 2018)


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

from __future__ import print_function
import sys, time
from mcp2210 import MCP2210

# active_cs values for enabling different CS lines (a zero in the bit position
# takes the CS to zero when SPI is active)
CS0_ENABLE = 0xfffe
CS1_ENABLE = 0xfffd
CS2_ENABLE = 0xfffb
CS3_ENABLE = 0xfff7
chip_select = [CS0_ENABLE, CS1_ENABLE, CS2_ENABLE, CS3_ENABLE]

bridge = MCP2210(0x04d8, 0x00de)
print(bridge.product_name)

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
transfer.spi_mode = 2 # Clock idles high, data sampled on first edge (change on second)
transfer.spi_tx_size = 2 # bytes per transfer
transfer.cs_data_delay = 0 # from CS to data (n * 100 us)
transfer.lb_cs_delay = 0   # last byte to CS de-assert
transfer.interbyte_delay = 0
transfer.idle_cs = 0xffff  # All CS lines idle in the high state
transfer.active_cs = 0xffff # Disable all CS lines by making their active state high also.
bridge.transfer_settings = transfer

def encoder(channel):
    transfer.active_cs = chip_select[channel]
    bridge.transfer_settings = transfer
    ret = bridge.transfer(b'aa') 
    ret = bytearray(ret) # keep py2 happy; redundant in py3 where it is already a bytes
    return ((256 * ret[0] + ret[1]) & 0x7ff8) >> 3 

# Demo to take and tabulate 4 angle transducers

cal_factor0 = 0.0
cal_factor1 = 0.0
cal_factor2 = 0.0
cal_factor3 = 0.0

def calibrate():
    global cal_factor0
    global cal_factor1
    global cal_factor2
    global cal_factor3
    cal_factor0 = encoder(0)
    cal_factor1 = encoder(1)
    cal_factor2 = encoder(2)
    cal_factor3 = encoder(3)

def toDegrees(angle):
    degreeAngle = angle / 4095 * 360
    if degreeAngle > 180:
        return degreeAngle - 360
    if degreeAngle < -180:
        return degreeAngle + 360
    else:
        return degreeAngle

def getAngle0():
    angleBytes = encoder(0)
    return toDegrees(float(angleBytes - cal_factor0))


def getAngle1():
    angleBytes = encoder(1)
    return toDegrees(float(angleBytes - cal_factor1))


def getAngle2():
    angleBytes = encoder(2)
    return toDegrees(float(angleBytes - cal_factor2))


def getAngle3():
    angleBytes = encoder(3)
    return toDegrees(float(angleBytes - cal_factor3))
    
def getAngles():
    ang0 = getAngle0()
    ang1 = getAngle1()
    ang2 = getAngle2()
    ang3 = getAngle3()
    return [ang0, ang1, ang2, ang3]
    
def getAngleRight():
    ang1 = getAngle0()
    ang2 = getAngle1()
    return ang1 - ang2


def getAngleLeft():
    ang2 = getAngle2()
    ang3 = getAngle3()
    return ang2 - ang3
