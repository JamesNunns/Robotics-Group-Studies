from re import search
from os import listdir
import time as tme
from limb_data import values
from positions_sym import positions
from utility_functions import flatten, read_file, current_data_types, get_latest_file, convert_list_dict, centre_of_mass_respect_seat, store
from sys import path, argv
from robot_interface import Robot, PositionError
#from robot_interface_webots import Robot
from encoder_interface import Encoders
import numpy
from collections import OrderedDict
from torso_and_legs import torso_dict, legs

option = raw_input("Using Real Robot (Yes/No)")
if option.upper() == 'NO':
    ###Training Functons###
    setup = 'Testing'
    path.insert(0, "Training_functions")
    from naoqi import ALProxy #Import Fake SDK
    import BigEncoder #Import fake bigencoder
     #Import fake smallencoder
elif option.upper() == 'YES':
    setup = 'Real'
    path.insert(0, "hidlibs")
    from pynaoqi.naoqi import ALProxy #Import robot's SDK
    import top_encoder.encoder_functions as BigEncoder #Import bigencoder
    #import bottom_encoder.hingeencoder as SmallEncoders
    path.insert(0, "Training_functions")
    import SmallEncoders #Import fake smallencoder as algo does not need them
path.insert(0, 'new_Algorithms')

class AlgorithmFinished(Exception): pass

# Allows user to select the algorithm file in Algorithms that they want to run
files = listdir('new_Algorithms')
# Search for files that are .py files and begin with algorithm_
list_algorithms = [x for x in files if search(
    r"(?=\.py$)", x)]
algo_dict = {}
for i, algo in enumerate(list_algorithms):
    algo_dict[i] = algo[:-3]
# Create dictionary with number key and name of algorithm for value
text = ["{} {}".format(key, algo_dict[key]) for key in algo_dict]

# By running this script with the final command line argument '@n' will run the nth algorithm that would
# otherwise appear in the list.
if argv[-1][0] is not "@":
    algorithm = str(
        input(
            '\033[1mWhich algorithm would you like to run? Pick number corresponding to algorithm\033[0m: \n{}\n'.format(
                "\n".join(text))))
else:
    algorithm = argv[-1][1:]

# Imports correct Algorithm class that interface inherits from
algorithm_import = algo_dict[int(algorithm)]
print("\033[1mRunning " + algorithm_import + "\n\033[0m")
path.insert(0, 'new_Algorithms')
Algorithm = __import__(algorithm_import).Algorithm

class Interface(Algorithm):

    def __init__(self,setup='Testing',period=0.1):
        """
        Initialising the interface coresponding to the desired setup
        
        Args:
            setup: Either 'Testing' or 'Real' 
            period: Sampling Period of the interface
        """
        self.period = period #Setting period const

        self.setup = setup #Setting setup string

        ##Initialising the selected Algorithm##
        Algorithm.__init__(self,BigEncoder,SmallEncoders,values,positions,ALProxy,period)

        self.motion.setStiffnesses("Body", 1.0) #Stiffening the Robot
        tme.sleep(4.0)
        try:
            self.check_setup('crunched')
        except PositionError as e:
            # When position doesn't set properly
            self.motion.setStiffnesses("Body", 0.0)
            self.speech.say('Failed, loosening')
            raise e

        self.algo_name = 'None'

    def get_ang_vel(self, time, current_angle):
        """
        Function to calculate the current angular velocity, taking last recorded value and new
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
  		ang_vel = delta_angle / delta_time
  		if ang_vel == 0.0:
  			old_old_values = self.all_data[-15]
  			if old_old_values['av'] < 0:
  				ang_vel = -1
  			else:
  				ang_vel = 1
        return ang_vel

    def select_algo(self, values, all_data):
        """
        Function to initialise a new Algorithm from the dictionary
        
        Args
            values: Dictionary containing the data for the locations of the Robot limbs
            all_data: Dictionary containing the values collected about the swing/Robot
        Returns
            algo_class_initialized.algo : Calling the algo function of the Algorithm 

        """
        try:
            # Remove first dictionary element from algorithm and store it
            info = self.order.pop(0)
        except IndexError:
            # Interface handles exception to break out of loop and stops and save
            raise AlgorithmFinished

        self.algo_class = info.pop('algo')
        # Rest of dictionary left are kwargs
        kwargs = info

        self.algo_name = self.algo_class.__name__ #Colecting the name of the algorithm
        algo_class_initialized = self.algo_class(values, all_data, **kwargs)

        return algo_class_initialized.algo

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
        """
        Function to run the selected algorithm.

        Args:
            switch: previous Output of Algorithm, either; 'switch', 'torso+', 'torso-', 'legs+', 'legs-''
            current_values: current values of the Robot
        Returns:
            switch: new Output of Algorithm, either; 'switch', 'crunched' or 'extended'
        """

        self.algo_name = Algorithm.__name__ #Collects the algorithm name

        if switch == 'switch': #If the output of the algo is 'switch' it will call select_algo
            self.algorithm = self.select_algo(current_values, self.all_data)#To change algorithm

        #Collects the retuned values from the algorithm        
        return_values = self.algorithm(current_values, self.all_data[-200:])

        if isinstance(return_values, list):
            switch, speed = return_values #If algo defines a speed the interface will use it
        else:
            switch, speed = return_values, 0.4 #Sets a defult speed

        # If text returned is a possible position switch to it
        if switch in positions.keys():
            self.set_posture(switch, self.position, speed)

        if switch == "torso_out":
            for joint in torso_dict:
                self.move_limbs(joint, torso_dict[joint]*5*0.0174533, speed)
        
        if switch == "torso_in":
            for joint in torso_dict:
                self.move_limbs(joint, torso_dict[joint]*5*-0.0174533, speed)

        if switch == "legs_out":
            for joint in legs:
                self.move_limbs(joint, -5*0.0174533, speed)

        if switch == "legs_in":
            for joint in legs:
                self.move_limbs(joint, 5*0.0174533, speed)
        
        if switch == "legs_retracted":
            for joint in legs:
                self.move_limbs(joint, 500*0.0174533, speed) 
        
        if switch == "legs_extended":
            for joint in legs:
                self.move_limbs(joint, -500*0.0174533, speed) 
        
        if switch == "torso_extended":
            for joint in torso_dict:
                self.move_limbs(joint, torso_dict[joint]*500*0.0174533, speed)


        if switch == "torso_retracted":
            for joint in torso_dict:
                self.move_limbs(joint, torso_dict[joint]*-500*0.0174533, speed)
                
        # Add current values to list of all values
        self.all_data = numpy.append(self.all_data, numpy.array(
            [tuple(current_values.values())], dtype=self.data_type), axis=0)

        return switch

    def __run_real(self, t, period):
        """
        Function to run the interface with the real Robot

        Args:
            t: Time period for the algo to elapse over
            period: The sample period of the git 
        """
        max_runs = t * 1 / period + 1.0 #Calculated the max runs for the time duration

        self.all_data = self.initialize_all_data() #Initializes all the data

        self.fname = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime()) #Creates an output file
        
        self.filename = self.fname + '.txt'
        
        self.initial_time = tme.time() #Collects the initial time
        switch = 'switch' #Sets the initial output as switch to select the first algo

        for event in range(int(max_runs)): 
            start_time = tme.time()

            # Collect all relevant values
            time = start_time - self.initial_time
            ax, ay, az = self.get_acc('y')
            gx, gy, gz = self.get_gyro()
            se0, se1, se2, se3 = 0, 0, 0, 0
            be = self.get_big_encoder()
            cmx, cmy = 0, 0
            av = self.get_ang_vel(time, be)
            algo = self.algo_name
            position = self.position
            current_values = convert_list_dict([time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position])
            
            #Tries to run the algo if the file allows
            try:
                switch = self.__run_algorithm(switch, current_values) 
            #If not it will pass the AlgorithmFinished exception
            except AlgorithmFinished:
                print('\n\033[1mAlgorithm finished, stopping\033[0m\n')
                break
        self.finish_script() #Calls the finish script function

    def __run_test(self, filename, output_directory):
        """
        Function to run the interface with a fake robot and fake encoders

        Args:
            filename: The name of the file containing prvious data to run the interface off
            output_directory: name of the Directory containg the data file
        
        """

        # Read old data
        print('\n\033[1mUsing test mode, will apply algorithm to data from file {}\033[0m\n'.format(filename))
        data = read_file(output_directory + filename)


        self.all_data = self.initialize_all_data()

        # some functions depend on sampling period, therefore extract correct
        # period and place into algorithm data so that it can be passed through
        average_cycle_time = numpy.mean(numpy.diff(data['time']))
        for algorithm in self.order:
            algorithm['period'] = average_cycle_time

        switch = 'switch'
        for i in xrange(len(data)):

            algo = self.algo_name

            # Make current row out of real values from data minus the position and algorithm
            # as those are the things we are running testing to watch
            row_no_pos_algo = list(data[i])[:-2]
            current_values = convert_list_dict(
                row_no_pos_algo + [algo, self.position])

            try:
                switch = self.__run_algorithm(switch, current_values)
            except AlgorithmFinished:
                print '\n\033[1mAlgorithm finished, stopping now\033[0m\n'
                break

        # Data loaded in will have ' Org' file so remove that and replace with ' Tst'
        store(filename[:-4] + ' Tst.txt', self.all_data)

    def finish_script(self):
        """
        Prints running time, cycle time, and stores current data to file
        Note that the file produced does NOT work on windows so cant be shared through git
        with the main repository
        Args:
            None
        Returns:
            None, but stores to file
        """
        # Check whether everything is running on schedule or not
        time_taken = tme.time() - self.initial_time
        print('\033[1mFinished in {:.2f}s\033[0m'.format(time_taken))
        # Check how fast code is running
        average_cycle_time = numpy.mean(numpy.diff(self.all_data['time']))
        print('\033[1mExpected sampling period: {:.3f}s\nActual sampling period: {:.3f}s\033[0m'.format(self.period, average_cycle_time))

        # store data in txt file, all original data has ' Org' added to name
        store(self.filename + ' Org', self.all_data)

    def run(self, **kwargs):
        """
        Function to run the entire interface.
        Checks the desired setup and runs the correct function for the Fake/Real Robot
        """

        if self.setup == 'Testing':
            latest, output_directory = get_latest_file('Code', test=False)
            filename = kwargs.get('filename', latest)
            self.__run_test(filename, output_directory)
        else:
            t = kwargs.get('t', 1000.0)
            self.__run_real(t, self.period)

if __name__ == '__main__':
    #If the Script fails the robot will loosen
    interface = Interface(setup, period=0.1)
    try:
        interface.run(filename='27-02-2020 15:59:56 Org')
    except KeyboardInterrupt:
        interface.finish_script()
        interface.speech.say('Tightening')
    finally:
        interface.motion.setStiffnesses("Body", 1.0)
