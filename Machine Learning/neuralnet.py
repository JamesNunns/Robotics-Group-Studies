#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:19:12 2020

@author: louismiranda-smedley
"""

import numpy as np

class NeuralNetwork():
    
    def __init__(self):
        
        np.random.seed(1)
        self.synaptic_weights = 2*np.random.random((3,1)) - 1
        
    def sigmoid(x):
        return 1/1+np.exp(-x)
    
    def sigmoid_derivative(x):
        return x*(1-x)
    
    def train(self, training_inputs, training_outputs, training_iterations):
        """ Using known inputs and outputs for training """
        for iteration in range(training_iterations):
            
            output = self.think(training_inputs)
            error = training_inputs - output
            adjustments = np.dot(training_inputs.T,error * self.sigmoid_derivative(output))
            self.synaptic_weights =+ adjustments
    
    def think(self, inputs):
        """ New situation, with user allowed inputs """
        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs,self.synaptic_weights))
        
        return output
    
    
if __name__ == '__main__':
    
    neural_network = NeuralNetwork()
    
    training_inputs = np.array([[0,0,1],
                        [1,1,1],
                        [1,0,1],
                        [0,1,1]])
    
    training_outputs = np.array([[0,1,1,0]]).T
    

    
        
        