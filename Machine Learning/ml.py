# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:33:07 2020

@author: Henry S
"""

from keras.models import load_models
import numpy as np

MODEL = load_models('net.h5')

def get_action(state):
    '''
    Takes the current state (angle and angular velocity deg/sec) and returns
    an integer depending on the calculated optimal move.

    0 - leg out
    1 - leg in
    2 - torso out
    3 - torso in
    4 - nothing

    Parameters
    ----------
    state : Array
        the current angle and angular velocity of the rod

    Returns
    -------
    action : int
        optimal move
    '''

    if state is None:
    # If there is no current state (i.e. at the start) makes a random move
        return np.random.randint(0, high=4)

    # the optimal move given the state
    action = np.argmax(MODEL.predict(state.reshape(-1, len(state)))[0])
    return action
