from numpy import sin, cos, pi
import numpy
from os import listdir
from collections import OrderedDict
import datetime
import numpy as np
#import matplotlib.pyplot as plt

def flatten(values):
    """
    Takes a list that can contain a mixture of lists and values, and recursively
    flattens the list until everything is one layer deep
    Args:
        values: list to flatten
    Returns:
        flattened list
    Example:
        > flatten([1, [3, 5, [6, 7]], [[[3]]]])
        [1, 3, 5, 6, 7, 3]
    """
    final_list = []
    for list_value in values:
        if isinstance(list_value, list):
            [final_list.append(value) for value in list_value]
        else:
            final_list.append(list_value)
    return final_list


def read_file(filename):
    """
    Reads data file with rows that have the same structure as current data types
    Args:
        filename: name of file to read
    Returns:
        2d numpy array containing named columns of current_data_types
    """
    data_type = current_data_types()

    # Data will be added to this with time
    all_data = numpy.empty((0, ), dtype=data_type)

    with open(filename, 'r') as f:
        file_data = f.read().split('\n')
        lines = [line.split(',') for line in file_data][:-1]
        for line in lines:
            all_data = numpy.append(all_data, numpy.array(
                [tuple(line)], dtype=data_type), axis=0)
    return all_data

def current_data_types():
    """
    Contains list of tuples that define the data types of self.all_data, type coercion helps with easily accessing
    data with names instead of index number
    Args:
        None
    Returns: 
        list of tuples containing name of column and data type
    """
    return [('time', 'f4'), ('event', 'i4'), ('ax', 'f4'), ('ay', 'f4'), ('az', 'f4'), ('gx', 'f4'), ('gy', 'f4'),
            ('gz', 'f4'), ('se0', 'f4'), ('se1', 'f4'), ('se2',
                                                         'f4'), ('se3', 'f4'), ('be', 'f4'), ('av', 'f4'),
            ('cmx', 'f4'), ('cmy', 'f4'), ('algo', '|S40'), ('pos', '|S10')]


def get_latest_file(current_dir, test=True):
    """
    Get latest data file, if test = True will collect latest tst file, if not then only
    original files will be loaded
    Args:
        current_dir: Code or Analysis
        test: include test files or not
    Returns:
        filename + ' Tst' or filename + ' Org'
    """
    if current_dir == 'Code':
        output_directory = 'Output_data/'
    else:
        output_directory = '../Output_data/'
    if test:
        filetype = 'Tst'
    else:
        filetype = 'Org'
    files = [name[:-4]
             for name in listdir(output_directory) if name[-3:] == filetype]
    if len(files) == 0:
        files = [name[:-4]
                 for name in listdir(output_directory) if name[-3:] == 'Org']
    dates = []
    for date in files:
        try:
            dates.append(datetime.datetime.strptime(
        date, "%d-%m-%Y %H:%M:%S"))
        except ValueError:
            pass
    dates.sort()
    latest = dates[-1]
    latest = datetime.datetime.strftime(latest, "%d-%m-%Y %H:%M:%S")
    if test:
        return latest + ' Tst', output_directory
    else:
        return latest + ' Org', output_directory


def convert_list_dict(current_values):
    """
    Converts list of values into a dictionary with keys of names current_data_types(), this way data
    can be accessed via values['time'] etc
    Args:
        current_values: list of values with same length as current_data_types()
    Returns:
        ordered dictionary with keys of correct data type, and values of corresponding values
    """

    data_types = current_data_types()
    if len(current_values) != len(data_types):
        raise ValueError('Length of values not equal to data types length')
    values = OrderedDict()
    data_names = [key_pair[0] for key_pair in data_types]
    for i, name in enumerate(data_names):
        values[name] = current_values[i]
    return values


def cm_to_cartesian(angle1, angle2, angle3, position):
    """
    Returns cartesian coordinate of centre of mass of nao, with respect to the big encoder
    angles need to be in radians
    position is centre of mass from centre_of_mass_respect_seat
    Args:
        angle1: big encoder angle (radians)
        angle2: encoder after big encoder value (radians)
        angle3: encoder value after other small encoder (radians)
        position: named position defined in positions.py
    Returns:
        cartesian coordinate of centre of mass of nao with respect to big encoder
    """
    cartesian_position_seat = position_seat_cartesian(angle1, angle2, angle3)
    centre_of_mass_nao_seat = position

    # minus because of big encoder angle direction
    angle_seat = - \
        numpy.arctan(cartesian_position_seat[0]/cartesian_position_seat[1])

    # using rotation of axes formula to convert between frames of reference
    converted_coords_x = numpy.cos(
        angle_seat) * centre_of_mass_nao_seat[0] - numpy.sin(angle_seat) * centre_of_mass_nao_seat[1]
    converted_coords_y = numpy.sin(
        angle_seat) * centre_of_mass_nao_seat[0] + numpy.cos(angle_seat) * centre_of_mass_nao_seat[1]
    # adding cartesian positions together
    return [cartesian_position_seat[0] + converted_coords_x, cartesian_position_seat[1] + converted_coords_y]


def position_seat_cartesian(angle1, angle2, angle3):
    """
    Calculates the cartesian coordinate of the seat with respect to the big encoder given all angles in radians
    Args:
        angle1: big encoder
        angle2: small encoder 0
        angle3: small encoder 1
    Returns:
        cartesian coordinate for seat with respect to big encoder
    """
    L1 = 1.5  # length of pendulum 1 in m
    L2 = 0.12  # length of pendulum 2 in m
    L3 = 0.20  # length of pendulum 3 in m
    x_seat = L3 * numpy.sin(angle1 + angle2 + angle3) + L2 * \
        numpy.sin(angle1 + angle2) + L1 * numpy.sin(angle1)
    y_seat = - L3 * numpy.cos(angle1 + angle2 + angle3) - L2 * \
        numpy.cos(angle1 + angle2) - L1 * numpy.cos(angle1)
    return [x_seat, y_seat]


def centre_of_mass_respect_seat(position, masses):
    """
    Returns centre of mass coordinates of nao in different positions, with respect to the SEAT
    Args:
        position: named position defined in positions.py
        masses: boolean as to whether masses are attached or not
    Returns:
        centre of mass of nao with respect to the seat in metres
    """
    if position == "seated" and masses == False:
        x_com = (0.0429973 - 0.03)
        y_com = (0.16 - 0.0165042)
    elif position == "extended" and masses == False:
        x_com = (0.0478673 - 0.03)
        y_com = (0.16 - 0.01934243)
    elif position == 'raised' and masses == False:
        x_com = (0.0496793 - 0.03)
        y_com = (0.16 + 0.00690544)
    elif position == 'lowered' and masses == False:
        x_com = (0.0386997 - 0.03)
        y_com = (0.16 - 0.0238556)
    elif position == 'seated' and masses:
        x_com = 1.000
        y_com = 1.000
    elif position == 'extended' and masses:
        x_com = 1.000
        y_com = 1.000
    elif position == 'raised' and masses:
        x_com = 1.000
        y_com = 1.000
    elif position == 'lowered' and masses:
        x_com = 1.000
        y_com = 1.000
    else:
        raise ValueError("Position not found")
    return [x_com, y_com]


def moving_average(values, window_size):
    """
    Calculates the moving average on a list of values
    Args:
        values: list of values to take moving average on
        window_size: how many values to use to average
    """
    ma = [np.sum(values[i:i+window_size])/window_size for i,
          _ in enumerate(values[:-window_size+1])]
    return ma


def last_zero_crossing(values, previous_time, previous_be):
    """
    Interpolates between two times and big encoder values, should be used when sign
    of encoder changes.
    Args:
        values: dictionary containing all current values being recorded
        previous_time: value of time before crossing
        previous_be: big encoder value at time before crossing
    Returns:
        estimated last zero crossing point, uses linear interpolation
    """
    current_be = values['be']
    dt = values['time'] - previous_time

    interpolate = dt * np.abs(current_be) / \
        np.abs(current_be - previous_be)

    min_time = values['time'] - interpolate
    return min_time


def last_maxima(time_list, values_list, time_values='time', dt=0.005):
    """
    Calculates when the last maxima happened, and returns either the time at which it happened, or the value
    when it happened. Uses a moving average on data first to remove most local maxima
    Args:
        time_list: list of times data was sampled at, or any list that functions as an index
        values_list: list of values corresponding to time_list
        time_values: whether to return the time at maximum or the value at maximum, or both
        dt: rough average of difference between sampling times
    Returns:
        time of latest maxima or value at this maxima
    Example:
        > time_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        > values_list = [1.0, 3.0, 5.0, 7.0, 9.0, 7.0, 5.0]
        > last_maxima(time_list, values_list, 'values', dt=0.5)
        9.0
    """
    return zero_maxima('max', time_list, values_list, time_values=time_values, dt=dt)

def last_minima(time_list, values_list, time_values='time', dt=0.005):
    """
    Calculates when the last bottom of the arc happened, and returns either the time at which it happened, or the value
    when it happened. Uses a moving average on data first to remove most local minima
    Args:
        time_list: list of times data was sampled at, or any list that functions as an index
        values_list: list of values corresponding to time_list
        time_values: whether to return the time at minima or the value at minima, or both
        dt: rough average of difference between sampling times
    Returns:
        time of latest minima or value at this minima
    Example:
        > time_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        > values_list = [7.0, 5.0, 3.0, 2.5, 4.5, 7.0,9.0]
        > last_minima(time_list, values_list, 'values', dt=0.5)
        2.5
    """
    return zero_maxima('min', time_list, values_list, time_values=time_values, dt=dt)

def zero_maxima(min_max, time_list, values_list, time_values='time', dt=0.005):
    """
    Generalised function that calculates zero crossing point or maxima value 

    THIS FUNCTION IS AWFUL IF YOU DECIDE TO IMPROVE ON OUR CODE MAKING THIS BETTER WOULD BE A START
    WOULD USE SCIPY BUT CAN'T USE scipy.find_peaks ON THE LAB PC
    """
    n = int(3.0 / dt)
    window_number = int(0.8 / dt)
    if window_number % 2 == 0:
        window_number += 1
    if window_number == 1:
        window_number = 3
    
    avg_values_list = np.abs(moving_average(values_list[-n:], window_number))
    if min_max == 'min':
        max_index = (np.diff(sign_zero(np.diff(np.abs(avg_values_list)))) > 0).nonzero()[0] + 1 + (window_number - 1)/2
    elif min_max == 'max':
        max_index = (np.diff(sign_zero(np.diff(avg_values_list))) < 0).nonzero()[0] + 1 + (window_number - 1)/2
    elif min_max == 'either':
        max_index = (np.abs(np.diff(sign_zero(np.diff(np.abs(avg_values_list))))) > 0).nonzero()[0] + 1 + (window_number - 1)/2
    else:
        raise ValueError('Choice of min or max not provided')
    
    if time_values == 'time':
        return time_list[-n:][max_index[-1]]
    elif time_values == 'values':
        return values_list[-n:][max_index[-1]]
    elif time_values == 'both':
        return time_list[-n:][max_index[-1]], values_list[-n:][max_index[-1]]
    else:
        raise ValueError('Last maxima is not returning anything')

def sign_zero(value_s):
    """
    Returns -1 if the value is less than 0, and 1 if it is greater than or equal to 0. 
    This ensures that when comparing crossing point sign_zero(value_before) != sign_zero(value_after)
    and there is a value of zero then the if statement won't trigger twice.
    Args:
        value: value to check sign of
    Returns:
        -1 or 1, depending on sign
    Example:
        > if sign_zero(0) != sign_zero(-2):
        >    print 'Ran'
        'Ran'
    """
    if isinstance(value_s, list) or isinstance(value_s, numpy.ndarray):
        return [sign_zero(value) for value in value_s]
    else:
        if value_s < 0:
            return -1
        elif value_s >= 0:
            return 1


def store(filename, all_data):
    """
    Saves numpy matrix as txt file while retaining data types such that columns can be accessed
    like a dictionary
    Args:
        filename: name of file to store to in Output_data folder
    Returns:
        None, but stores to filename
    Example:
        > store('file_to_store_to')
    """
    with open('Output_data/' + filename, 'w') as f:
        rows = [[str(i) for i in list(line)[:-1]] + [line[-1]]
                for line in all_data]
        for row in rows:
            f.write(','.join(row) + '\n')
    print '\n\033[1mData saved to {}\033[0m\n'.format(filename)
        

def total_angle(be, se0, se1):
    x, y = position_seat_cartesian(be * np.pi/180, se0 * np.pi/180, se1 * np.pi/180)
    return - np.arctan(x/y) * 180/np.pi
