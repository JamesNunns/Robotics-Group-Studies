#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:46:59 2020

@author: robgc
"""
import numpy as np

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
    if isinstance(value_s, list) or isinstance(value_s, np.ndarray):
        return [sign_zero(value) for value in value_s]
    else:
        if value_s < 0:
            return -1
        elif value_s >= 0:
            return 1

