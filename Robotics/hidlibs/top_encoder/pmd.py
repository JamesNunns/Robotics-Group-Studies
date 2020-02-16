"""Module for talking to a USB1208FS data acquisition device

Python Library for talking to a Measurement Computing
USB data acquisition module, model USB1208FS (formerly pmd1208fs)
"""

# This presents roughly the same API as the 1.x version.  The functions
# associated with ainscan have been changed and a few unpopular functions
# have been dropped.

# Copyright 2009 Mark Colclough

from ctypes import *
import array
libpmd = cdll.LoadLibrary("libpmd1208fs.so.2")

pmd_flash = libpmd.pmd_flash
pmd_serial = libpmd.pmd_serial
pmd_serial.restype = c_char_p
pmd_digin = libpmd.pmd_digin
pmd_digin16 = libpmd.pmd_digin16
pmd_digout = libpmd.pmd_digout
pmd_digconf = libpmd.pmd_digconf
pmd_aout = libpmd.pmd_aout
pmd_ain = libpmd.pmd_ain
pmd_ainstop = libpmd.pmd_ainstop
pmd_ainscan = libpmd.pmd_ainscan
pmd_ainawaited = libpmd.pmd_ainawaited
pmd_ainactive = libpmd.pmd_ainactive
pmd_ainkill = libpmd.pmd_ainkill
pmd_crst = libpmd.pmd_crst
pmd_cin = libpmd.pmd_cin
pmd_version = libpmd.pmd_version
pmd_version.restype = c_char_p
usb_get_errmsg = libpmd.usb_get_errmsg
usb_get_errmsg.restype = c_char_p


class pmd1208fs:
    """Represents a usb1208fs or pmd1208fs device

    Create an instance of this class, then use its methods to talk to the device.
    At present, only one device is supported.

    Parameters
    ----------
    arraysize : int
        Size of the array.array that is used to holdainscan data.  An error
        will be raised if an ainscan would overflow.

    Attributes
    ----------
    ranges : (tuple of int)
        Full-scale voltage for each adc range setting. ranges[0] is 20, meaning
        from -20 to 20 V; ranges[7] is 1, meaning -1 to + 1 V.
    """

    def __init__(self, arraysize=10000):
        """Find the device and check that it works"""
        self.pmd = libpmd.pmd_find_first()
        if self.pmd == 0:
            raise IOError("PMD1208FS device not found")
        # print "found pmd handle", self.pmd
        # Discover any communication difficulties right now, in the ctor.
        self.hardware_serial_number = self.hserial()
        # Used by ainscan
        self.data = array.array('h', range(arraysize))
        self.dataloc, self.datasize = self.data.buffer_info()
        self.numsamples = 0

    def __del__(self):
        """Close the device"""
        # print "closing pnd handle", self.pmd
        # not if it was never opened, or if lhe lib wrapper is gone
        if self.pmd != 0 and libpmd is not None:
            libpmd.pmd_close(self.pmd)

    def version(self):
        """Return the version string of the underlying pmd1208fs C library

        Returns
        -------
        string
            Version of libpmd1208fs in use
        """
        return pmd_version()

    def flash(self):
        """Flash the module's LED briefly"""
        pmd_flash(self.pmd)

    def hserial(self):
        """Return the Hardware serial number as a fixed-length string

        Returns
        -------
        string
            Hardware serial number (8 characters)
        """
        return pmd_serial(self.pmd)

    def digin(self, port):
        """Return 8 bits of a digital port as integer

        Parameters
        ----------
        port : int
            0 for port A, 1 for port B

        Returns
        -------
        int
            0 - 255, representing data at port
        """
        return pmd_digin(self.pmd, port)

    def digin16(self):
        """Return all 16 bits of digital input as integer

        Returns
        -------
        int
            0 - 65535, A0 is lowest bit, B7 highest
        """
        return pmd_digin16(self.pmd)

    def digout(self, port, value):
        """Send 8-bit integer to digital output port

        Parameters
        ----------
        port : int
            0 for port A, 1 for port B
        value : int
            0 - 255.  Excess bits get masked off.
        """
        pmd_digout(self.pmd, port, value)

    def digconf(self, port, direction):
        """Configure the direction of a digital port

        All 8 bits of a port have the same direction.

        Parameters
        ----------
        port : int
            0 for port A, 1 for port B
        direction : int
            0 = output, 1 = input (the default)
        """
        pmd_digconf(self.pmd, port, direction)

    def aout(self, channel, value):
        """Send a single value to an analogue output.

        Parameters
        ----------
        channel : int
            0 or 1  for DA0 or DA1
        value : int
            0 - 4095 for 0 to 4.095 volts
        """
        ret = pmd_aout(self.pmd, channel, value)
        if ret < 0:
            raise IOError("%d: %s" % (ret, usb_get_errmsg(ret)))

    # ADC range index to full scale volts translation
    ranges = (20, 10, 5, 4, 2.5, 2, 1.25, 1)

    def ain(self, channel, adcrange):
        """Return single ADC value

        The fastest this command will loop at is 1000 samples per second,
        because of the USB timing.  For faster sampling, use ainscan.

        Parameters
        ----------
        channel : int
            0 to 3 for the three differential analogue inputs
        adcrange : int
            0 - 7 for decreasing full-scale ranges, see `ranges` attribute.

        Returns
        -------
        int
            -2048 ... 2047.  The returned integer value should be multiplied by
            (`ranges`[`adcrange`]/2047.0) to convert to volts.
        """
        ret = pmd_ain(self.pmd, channel, adcrange)
        if ret < -2048:
            usberr = ret + 2049
            raise IOError("%d: %s" % (usberr, usb_get_errmsg(usberr)))
        return ret

    # Use after ainscan, or to kill one. Probably not needed.
    def ainstop(self):
        pmd_ainstop(self.pmd)

    def ainscan(self, lowch=0, highch=0, npts=1000,
                interval=100, trigger=0, block=1):
        """Perform analogue input in burst mode

        If block==1, blocks until all data arrive.
        If block==0, starts transfer and returns immediately; use ainawaited
        to determine when the transfer has finished or failed, and ainkill to
        stop it early.

        In either case, the acquired data is self.data, an array.array of integers
        in the range -2048..+2047.   The first self.numsamples of this array
        are the data requested.

        The full scale ranges of the channels in use must be set previously, by
        a call to ain.

        Parameters
        ----------
        lowch : int
            0 - 4, first channel to scan
        highch : int
            0 - 4, last channel to scan
        npts : int
            number of samples per channel
        interval : int
            Time in us between successive samples of the same channel (>20)
        trigger : int
            0=internal, -1=external, falling edge, +1=external, rising edge
        block : int
            0=non-blocking, 1=blocking

        Returns
        -------
        int
            0 for success, or negative error code
        """
        self.numsamples = (highch - lowch + 1) * npts
        ret = pmd_ainscan(self.pmd, lowch, highch, npts, interval, trigger,
                          self.dataloc, self.datasize, block)
        if ret < 0:
            raise IOError("ainscan error %d" % ret)

    def ainawaited(self):
        """Determine whether the last non-blocking ainscan has finished

        Returns
        -------
        int
            A positive return value is the number of bytes outstanding.
            Zero signifies proper completion.
            Negative is either a detected error (-EIO == -5) or some
            equally erroneous bad counting
        """
        return pmd_ainawaited(self.pmd)

    def ainactive(self):
        """Return the number of active USB transfers

        Returns
        -------
        int
            Number of active USB transfers. If not zero, ainscan will return -EAGAIN.
            It goes to zero a short while after ainawaited.

        """
        return pmd_ainactive(self.pmd)

    def ainkill(self):
        """Force cancellation of the last non-blocking ainscan

        Performs an ainstop, then forces an error.
        May be up to 2s before ainawaited==0.
        """
        pmd_ainkill(self.pmd)

    def crst(self):
        """Reset the event counter"""
        pmd_crst(self.pmd)

    def cin(self):
        """Read the event counter

        Returns
        -------
        int
            Count of events since last crst, up to 32 bits.  Other actions on
            the device seem to disturb the count.
        """
        return pmd_cin(self.pmd)


# Useful little data plotter
gp = None  # keep the gnuplot window around until overwritten


def plot():
    global gp
    print("writing to tdat and running gnuplot\n")
    fil = open("tdat", "w")
    for x in mydev.data[:mydev.numsamples]:
        fil.write("%d\n" % x)
    fil.close()
    gp = os.popen("gnuplot", "w")
    gp.write("plot 'tdat' with linespoints\n")
    gp.flush()


if __name__ == "__main__":
    import time
    import os

    for i in range(5):
        try:
            mydev = pmd1208fs()
            break
        except BaseException:
            raw_input("failed to find! CR to try again")

    print "using libpmd1208fs version:", mydev.version()
    print "serial is", mydev.hserial()
    print "flashing now"
    mydev.flash()

    print "doing a blocking ainscan"
    mydev.ainscan()
    plot()

    print "running counter for three seconds"
    mydev.crst()
    time.sleep(3)
    print "count in 3 seconds:", mydev.cin()

    print "a fast one"
    mydev.ainscan(block=0)
    while mydev.ainawaited() > 0:
        pass
    while mydev.ainactive() > 0:
        pass

    print "a fast two"
    mydev.ainscan(block=0)
    while mydev.ainawaited() > 0:
        pass
    while mydev.ainactive() > 0:
        pass

    print "a fast three"
    mydev.ainscan(block=0)
    while mydev.ainawaited() > 0:
        pass
    while mydev.ainactive() > 0:
        pass

    print "a fast four"
    mydev.ainscan(block=0)
    while mydev.ainawaited() > 0:
        pass
    while mydev.ainactive() > 0:
        pass

    print "doing a (too) slow ainscan"
    mydev.ainscan(0, 1, 1000, 40000, 0, 0)
    for i in range(6):
        bytesleft = mydev.ainawaited()
        print "%d bytes to go" % bytesleft,
        print "sleeping%d... " % i
        time.sleep(1)
        bytesleft = mydev.ainawaited()
        if bytesleft <= 0:
            break
    if bytesleft > 0:
        print "got bored waiting, killing transfer"
        mydev.ainkill()
    plot()

    print "doing a less boring ainscan, as soon as it will work"
    while True:
        try:
            mydev.ainscan(block=0)
            break
        except IOError:
            time.sleep(1)

    for i in range(6):
        bytesleft = mydev.ainawaited()
        print "%d bytes to go" % bytesleft,
        print "sleeping%d... " % i
        time.sleep(1)
        bytesleft = mydev.ainawaited()
        if bytesleft <= 0:
            break
    if bytesleft > 0:
        print "got bored waiting, killing transfer"
        mydev.ainkill()
    plot()

    print "now a a less boring ainscan"
    #mydev.ainscan(0, 1, 1000, 400, 0, 0)
    mydev.ainscan(block=0)
    for i in range(6):
        bytesleft = mydev.ainawaited()
        print "%d bytes to go" % bytesleft,
        print "sleeping%d... " % i
        time.sleep(1)
        bytesleft = mydev.ainawaited()
        if bytesleft <= 0:
            break
    if bytesleft > 0:
        print "got bored waiting, killing transfer"
        mydev.ainkill()
    plot()
