# python2.7
"""
A module containing class that connects to encoders and returns data.

Contains class:
    Encoders
"""


class Encoders():
    """
    Class that connects to encoders to return values, will either be fake encoders that always return 1
    or real encoders depending on the setup used in interface.py.
    """

    def __init__(self, BigEncoder):
        """
        Initialises encoders.
        Args:
            BigEncoder: Class that connects to big encoder, available in hidlibs for real values or training functions for fake
        """
        # BigEncoder, SmallEncoders will either be the real functions or a set of fake functions returning
        # fake values
        # They are imported in interface so storing retains access of them
        self.BigEncoder = BigEncoder
        # Set current angle to zero point
        self.calibrate()

    def calibrate(self):
        """
        Set current angle to 0 degrees.
        Args:
            None
        Returns:
            None
        Example:
            > self.calibrate()
        """
        self.BigEncoder.calibrate()

    def get_big_encoder(self):
        """
        Returns the numerical value read from the large encoder at the top of the swing.
        Args:
            None
        Returns:
            angle of large encoder in degrees
        Example:
            > self.get_big_encoder()
            10.2
        """

        return self.BigEncoder.getAngle()
