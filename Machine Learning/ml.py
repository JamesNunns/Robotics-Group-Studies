# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:33:07 2020

@author: User
"""

from keras.models import load_models 
import numpy as np

model = load_models('net.h5')

def get_action(state):
    
    if state is None:
        return np.random.randint(0, high=4)
    action = np.argmax(model.predict(state.reshape(-1, len(state)))[0])
    return action
