from re import search
from os import listdir
import time as tme
from limb_data import values
from positions import positions
from utility_functions import flatten, read_file, current_data_types, get_latest_file, convert_list_dict, centre_of_mass_respect_seat, store
from sys import path, argv
from robot_interface import Robot, PositionError
#from robot_interface_webots import Robot
from encoder_interface import Encoders
import numpy
from collections import OrderedDict


option = raw_input("Using Real Robot (Yes/No)")
if option == 'No':
    ###Training Functons###
    path.insert(0, "Training_functions")
    from naoqi import ALProxy
    import BigEncoder
elif option == 'Yes':
    path.insert(0, "hidlibs")
    from pynaoqi.naoqi import ALProxy
    import top_encoder.encoder_functions as BigEncoder

path.insert(0, 'new_Algorithms')
import jack as Algorithm

class Interface():

    def __init__(self,setup=option,period=0.005):
        
        self.period = period

        self.setup = setup

        Algorithm.__init__(
            self,
            BigEncoder,
            SmallEncoders,
            values,
            positions,
            ALProxy,
            period
        )

        self.motion.setStiffnesses("Body", 1.0)
        tme.sleep(4.0)
        try:
            self.check_setup('seated')
        except PositionError as e:
            # When position doesn't set properly
            self.motion.setStiffnesses("Body", 0.0)
            self.speech.say('Failed, loosening')
            raise e

    def get_ang_vel(self, time, current_angle):
        """
        Function to get the current angular velocity, taking last recorded value and new
        value.
        Args:
            time: time since start of algorithm
            current_angle: current big encoder value
        Returns:
            Angular velocity in rad s^-1 is there is previous data, otherwise 0
        Example:
            > self.get_ang_vel(0.5, 0.6)
            -0.2
        """
        # No angular velocity if no old data
        if len(self.all_data) < 5:
            return 0

        old_values = self.all_data[-5]

        delta_time = time - old_values['time']
        delta_angle = current_angle - old_values['be']

        return delta_angle / delta_time

    def initialize_all_data(self):
        """
        Sets up all_data for storage of data, should be same for all test modes
        Args:
            None
        Returns:
            all_data, 2d numpy array with forced data types
        Example:
            > self.initialize_all_data()
        """
        # For good numpy storage need column names and data types
        self.data_type = current_data_types()
        # Data will be appended to this with time
        all_data = numpy.empty((0, ), dtype=self.data_type)
        return all_data

    def __run_algorithm(self, switch, current_values):
        self.algo_name = Algorithm.__name__

        return_values = self.algorithm(current_values, self.all_data[-200:])

        if isinstance(return_values, list):
            switch, speed = return_values
        else:
            switch, speed = return_values, 1.0

        # If text returned is a possible position switch to it
        if switch in positions.keys():
            self.set_posture(switch, self.position, speed)

        # Add current values to list of all values
        self.all_data = numpy.append(self.all_data, numpy.array(
            [tuple(current_values.values())], dtype=self.data_type), axis=0)
        
        return switch
    
    def run(self, t, period):

        max_runs = t * 1 / period + 1.0

        self.all_data = self.initialize_all_data()
        self.filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())

        self.initial_time = tme.time()

        for event in range(int(max_runs)):
            start_time = tme.time()

            # Collect all relevant values
            time = start_time - self.initial_time
            #ax, ay, az = self.get_acc()
            #gx, gy, gz = self.get_gyro()
            #se0, se1, se2, se3 = self.get_small_encoders()
            be = self.get_big_encoder()
            #cmx, cmy = centre_of_mass_respect_seat(self.position, self.masses)
            av = self.get_ang_vel(time, be)
            algo = self.algo_name
            position = self.position
            current_values = convert_list_dict(
                [time, event, be, av, cmx, cmy, algo, position])

            try:
                out = self.__run_algorithm(current_values)
            except AlgorithmFinished:
                print('\n\033[1mAlgorithm finished, stopping\033[0m\n')
                break