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

    def __init__(self, BigEncoder, SmallEncoders, **kwargs):
        """
        Initialises encoders.
        Args:
            BigEncoder: Class that connects to big encoder, available in hidlibs for real values or training functions for fake
            SmallEncoders: Class that connects to small encoders, available in hidlbis for real values or training functions for fake
            small_encoders_required (optional): whether you want to return zero or not as small encoders are slow
        Returns:
            None
        """
        # BigEncoder, SmallEncoders will either be the real functions or a set of fake functions returning
        # fake values
        # They are imported in interface so storing retains access of them
        self.SmallEncoders = SmallEncoders
        self.BigEncoder = BigEncoder
        self.small_encoders_required = kwargs.get('small_encoders_required', False)
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
        print '\033[1mCalibrating encoders\033[0m'
        self.SmallEncoders.calibrate()
        self.BigEncoder.calibrate()

    def get_small_encoders(self):
        """
        Return the angles recorded by the small hinge encoders, at the base of the swing, at the time of calling.
        Args:
            None
        Returns:
            list containing angle of each small encoder in degrees
        Example:
            > self.get_small_encoders()
            [10.0, 0.5, 5.0, 3.0]
        """
        encoder0 = self.SmallEncoders.getAngle0()
        encoder1 = self.SmallEncoders.getAngle1()
        encoder2 = self.SmallEncoders.getAngle2()
        encoder3 = self.SmallEncoders.getAngle3()
        return [encoder0, encoder1, encoder2, encoder3]

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
