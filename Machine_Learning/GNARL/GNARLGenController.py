# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:34:54 2020

@author: Tom
"""
from gnarl import Gnarl;
import construct_net
import numpy as np


class gnarl_controller():
    def __init__(self, pop_size, engine, start_entities = None, input_length = 2, output_length = 2, max_generation=30):
        self.pop_size = pop_size
        self.entities = [0]*pop_size
        self.fitnesses = np.array(np.zeros((pop_size)))
        
        if start_entities is None:
            for i in range(pop_size):
                self.entities[i] = Gnarl(engine, input_size=input_length, output_size=output_length).initial_structure()
                
        elif len(start_entities) < pop_size:
            self.entities[0:len(start_entities)] = start_entities
            for i in range(pop_size - len(start_entities)):
                self.entities[len(start_entities) + i] = Gnarl(engine, input_size=input_length, output_size=output_length).initial_structure()
                
        elif len(start_entities) >= pop_size:
            self.entities = start_entities[0:pop_size]
        
        for i in range(max_generation):
            [e.run() for e in self.entities]
            self.fitnesses = np.array([e.fitness for e in self.entities])
            self.nextGeneration()
            
        
                
                
        
    def nextGeneration(self):
        #get fitnesses
        sorted_args = self.fitnesses.argsort()
        sorted_fitnesses = self.fitnesses[sorted_args[::-1]]
        parents = sorted_fitnesses[0:self.pop_size]
        children = np.array([e.copy().mutate() for e in parents])
        self.entities = np.append(parents, children)
        


if __name__ == '_main_':
    controller = gnarl_controller(2, None, max_generation=1)
    print([e for e in controller.entities])