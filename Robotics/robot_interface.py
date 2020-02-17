# python2.7
"""
A modules containing a class with which to access data about the robot and control it.

Contains class:
  Robot
"""

class PositionError(Exception): pass

class Robot():
    """
    Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
    """

    def __init__(self, values, positions, ALProxy,
                 ip="192.168.1.3", port=9559, **kwargs):
        """
        Sets up the connection to the robot and sets initial posture. Also calibrates encoders to zero, if available.
        Requires arguments:

        values: dictionary containing information of robot limb data
        positions: dictionary containing different preset positions
        ip : string, contains the IPv4 address of the robot to connect to.
        port : int, contains the port number through which to access the robot.
        """
        # Store for later
        self.values = values
        self.positions = positions

        # Set up proxies to robot
        self.speech = ALProxy("ALTextToSpeech", ip, port)
        self.motion = ALProxy("ALMotion", ip, port)
        self.memory = ALProxy("ALMemory", ip, port)
        self.masses = kwargs.get('masses', True)
        self.acc_required = kwargs.get('acc_required', False)
        self.gyro_required = kwargs.get('gyro_required', False)

        self.set_posture_initial('crunched', max_speed = 0.1)
        self.motion.setMotionConfig( [["ENABLE_DISACTIVATION_OF_FALL_MANAGER", True]] )
        self.motion.setFallManagerEnabled(False)
        #self.speech.say('Battery level at {:.0f}%'.format(self.get_angle('BC')[0]*100))
        print 'Battery level at {:.0f}%'.format(self.get_angle('BC')[0]*100)
        
    def check_setup(self, position):
        """
        Checks position values received from Nao match the position values it's meant to have
        Args:
            position: name of position to check
        Returns:
            None
        Example:
            > self.check_setup('extended')
        """
        position = self.positions[position]
        values = [self.get_angle(key)[0] for key in position.keys()]
        differences = [(key, value, abs(value - position[key])) for (key, value) in zip(position.keys(), values)]

        incorrect_positions = [i for i in differences if i[2] > 0.5]
        if len(incorrect_positions) != 0:        
            # for values in incorrect_positions:
                # print values[0], 'Actual value: {}'.format(values[1]), 'Difference from expected: {}'.format(values[2])
            
            error_amounts = ['{}, Actual value: {}, Difference from expected: {}'.format(*v) for v in incorrect_positions]
            raise PositionError("Initial check of setup failed\n" + '\n'.join(error_amounts))
            
            
    def get_gyro(self):
        """
        Obtain the current gyroscope data. Returns a tuple containing the (x, y, z) gyroscope data,
        in rad/s.
        Args:
            None
        Returns:
            list containing x, y, and z gyrometer
        Example:
            > self.get_gyro()
            [0.0, 0.5, 0.6]
        """
        if self.gyro_required: # This is slow and limits interface heavily
            # not sure whether the below works on not, worth testing
            # x_data, y_data, z_data = self.memory.getData([self.values['GX'][1], self.values['GY'][1], self.values['GZ'][1]])
            x_data = self.memory.getData(self.values['GX'][1])
            y_data = self.memory.getData(self.values['GY'][1])
            z_data = self.memory.getData(self.values['GZ'][1])
            return [x_data, y_data, z_data]
        else:
            return [0.0, 0.0, 0.0]

    def get_acc(self):
        """
        Obtain the current accelerometer data. Returns a list containing the (x, y, z) acceleromenter data,
        in m/s.
        Args:
            None
        Returns:
            list containing x, y, and z acceleration
        Example:
            > self.get_acc()
            [0.0, 1.1, 0.5]
        """
        if self.acc_required: # This is slow and limits interface heavily
            # same again, not sure if this works but would be good to save time
            # x_data, y_data, z_data = self.memory.getData([self.values['ACX'][1], self.values['ACY'][1], self.values['ACZ'][1]])
            x_data = self.memory.getData(self.values['ACX'][1])
            y_data = self.memory.getData(self.values['ACY'][1])
            z_data = self.memory.getData(self.values['ACZ'][1])
            return [x_data, y_data, z_data]
        else:
            return [0.0, 0.0, 0.0]

    def get_angle(self, part_name):
        """
        Get the current angle of the named part.
        Args:
            part_name : the name of the part as written in the values dictionary.
        Returns:
            angle of joint in radians and shorthand naoqi name
        Example:
            > self.get_angle('HY')
            1.03, HeadYaw
        """
        limb_info = self.values[part_name]
        angle = self.memory.getData(limb_info[1])
        name = limb_info[0]
        return angle, name
        
    def set_posture(self, next_posture, current_posture, max_speed=1.0):
        """
        Changes position from current_posture to next_posture, calculates correct speeds
        for all joints to finish at the correct time
        Args:
            next_posture: name of posture to switch to
            current_posture: name of posture nao is currently in
            max_speed: value between 0 and 1 specifying how fast to change
        Returns:
            None
        Example:
            self.set_posture('extended', self.position)
        """
        # Extract dictionaries corresponding to both positions
        next_posture_dict = self.positions[next_posture]
        current_posture_dict = self.positions[current_posture]
        
        differences_in_angles = []
        for name in next_posture_dict.keys():
            # Calculate difference in angle for each joint
            difference = abs(next_posture_dict[name] - current_posture_dict[name])
            # Can't have a speed of 0 so pretend there is a difference to get a non zero speed
            if difference == 0:
                differences_in_angles.append(0.01)
            else:
                differences_in_angles.append(difference)

        # Normalise speeds to longest time
        max_difference = max(differences_in_angles)
        speeds = [max_speed * difference / max_difference for difference in differences_in_angles]
            
        # Extract name naoqi uses to set positions
        part_name = [self.values[name][0] for name in next_posture_dict.keys()]
        
        # Change position
        for name, value, speed in zip(part_name, next_posture_dict.values(), speeds):
            self.motion.setAngles(name, value, speed)
        # Update self.position with now current position
        self.position = next_posture
        
    def set_posture_initial(self, next_posture='seated', max_speed=0.2):
        """
        Moves nao from whatever position he is currently in to a specified starting position, important
        this is used as otherwise speeds aren't normalised and that will destroy his joints
        Args:
            next_posture: named position to move to
            max_speed: how fast he should move
        Returns:
            None
        Example:
            self.set_posture_initial('seated')
        """
        # This sets the stiffness permanently
        self.motion.setStiffnesses("Body", 1.0)
        
        # Calculate his current position
        startup_dict = {}
        for key in self.positions[next_posture].keys():
            startup_dict[key] = self.get_angle(key)[0]
        # Add his current position to the positions dictionary
        self.positions['startup'] = startup_dict
        
        # Switch from current position just added to next_posture
        self.set_posture(next_posture, 'startup', max_speed=max_speed)
        
        
        
