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
        accX_0, accY_0, accZ_0 = 0, 0, 0
        self.calibrate_acc()

        self.set_posture_initial('crunched', max_speed = 0.1)
        #self.motion.setMotionConfig( [["ENABLE_DISACTIVATION_OF_FALL_MANAGER", True]] )
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

    def get_acc(self, plane):
        """
        Obtain the current accelerometer data. Returns a list containing the (x, y, z) acceleromenter data,
        in m/s.
        Args:
            name of the undesired accelerometer
        Returns:
            list containing x, y, and z acceleration (0.0 for undesired accelerometers)
        Example:
            > self.get_acc()
            [0.0, 1.1, 0.5]
        """
        if self.acc_required: # This is slow and limits interface heavily
            # same again, not sure if this works but would be good to save time
            # x_data, y_data, z_data = self.memory.getData([self.values['ACX'][1], self.values['ACY'][1], self.values['ACZ'][1]])
            if plane == 'z':
                x_data = self.memory.getData(self.values['ACX'][1]) - accX_0
                y_data = self.memory.getData(self.values['ACY'][1]) - accY_0
                z_data = 0.0
            elif plane == 'x':
                x_data = 0.0
                y_data = self.memory.getData(self.values['ACY'][1]) - accY_0
                z_data = self.memory.getData(self.values['ACZ'][1]) - accZ_0
            elif plane == 'y':
                x_data = self.memory.getData(self.values['ACX'][1]) - accX_0
                y_data = 0.0
                z_data = self.memory.getData(self.values['ACZ'][1]) - accZ_0
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

    def move_limbs(self, limb_name, angle, percent_max_speed):
        """
        Moves limbs by given angles
        Args:
            limb_name: string
                shorthand key of the desired limb as given in the limb_data dictionary
            angle: float
                the angle to move the desired limb in radians
            percent_max_speed: float
                percentage of max speed given as a decimal between 0 and 1
        Returns:
            None
        """
        current_angle, long_name = self.get_angle(limb_name)
        if current_angle + angle <= self.positions['maxs'][limb_name] and current_angle + angle >= self.positions['mins'][limb_name]:
            self.motion.changeAngles(long_name, angle, percent_max_speed)
        elif current_angle + angle > self.positions['maxs'][limb_name]:
            self.motion.setAngles(long_name, self.positions['maxs'][limb_name], percent_max_speed)
        elif current_angle + angle < self.positions['mins'][limb_name]:
            self.motion.setAngles(long_name, self.positions['mins'][limb_name], percent_max_speed)

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

    def set_posture_initial(self, next_posture='crunched', max_speed=0.2):
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

    def get_posture(self):
        '''
        Temporarily adds the current posture of Nao to the imported 'positions'
        dictionary calling it 'current'

        Args:
            summary: list
                Raw list of current posture generated using "motionProxy.getSummary()"
        Returns:
            None
        Example:
            self.get_posture()
            current_posture = positions['current']
        '''
        current_posture = {}
        summary = self.motion.getSummary()
        summary = summary.split()
        summary = summary[7:-14]
        for i in range(len(summary)/4):
            for keys in self.values:
                if self.values[keys][0] == summary[4*i]:
                    current_posture[keys] = float(summary[4*i + 3])
        self.positions['current'] = current_posture

    def is_moving(self, body_section = 'all'):
        """
        Checks if the robot is moving by comparing commanded and current joint
        angles and assuming if it has not reached the command it is still moving

        Args: body_section ('torso' or 'legs')
            section of body to check movement
        Returns
            None
        """
        current_posture, command_posture = {}, {}
        summary = self.motion.getSummary()
        summary = summary.split()
        summary = summary[7:-14]

        if body_section = 'torso': section_list = ['RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY']
        elif body_section = 'legs': section_list = ['RKP', 'LKP', 'LAP', 'RAP']
        else: section_list = ['RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY', 'RKP', 'LKP', 'LAP', 'RAP']

        current_posture, command_posture = {}, {}
        for i in range(len(summary)/4):
            for keys in section_list:
                if self.values[keys][0] == summary[4*i]:
                    current_posture[keys], command_posture[keys] = float(summary[4*i + 3]), float(summary[4*i + 2])
        differences = [current_posture[keys]-command_posture[keys] for keys in section_list]
        l = [abs(dif) < 0.01 for dif in differences]
        if all(l):
            return False
        else:
            return True

    def calibrate_acc(self):
        '''
        A function that takes no arguments and calibrates the accelerometers to zero
        '''
        global accX_0, accY_0, accZ_0
        if self.acc_required:
            accX_0, accY_0, accZ_0 = self.memory.getData(self.values['ACX'][1]), self.memory.getData(self.values['ACY'][1]), self.memory.getData(self.values['ACZ'][1])
        else:
            accX_0, accY_0, accZ_0 = 0, 0, 0
