#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:17:49 2020

@author: louismiranda-smedley
"""

import numpy as np


""" Normalising function """

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return x*(1-x)



""" Inputs are a 4x3 matrix """

training_inputs = np.array([[0,0,1],
                            [1,1,1],
                            [1,0,1],
                            [0,1,1]])


""" Outputs are a 4x1 matrix """

training_outputs = np.array([[0,1,1,0]]).T



""" Generate random initial weights """

np.random.seed(1)

synaptic_weights = 2 * np.random.random((3,1)) - 1

#print(f'synamptic weights are \n{synaptic_weights}')



""" Model training """

for iteration in range(20000):
    
    input_layer = training_inputs
    
    #np.dot() is essentially matrix multiplication
    outputs = sigmoid(np.dot(input_layer,synaptic_weights)) 
    
    error = training_outputs - outputs
    
    adjustments = error * sigmoid_derivative(outputs)
    
    synaptic_weights += np.dot(input_layer.T,adjustments)

""" new situation """

new_situations = np.array([[1,0,0]])

new_outputs = sigmoid(np.dot(new_situations,synaptic_weights))

print(new_outputs)
    
#print(f'outputs are \n{outputs}')
