# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:34:54 2020

@author: Tom
"""
from gnarl_mutate import Gnarl
# import construct_net_new
import numpy as np



class gnarl_controller():
    def __init__(self, pop_size, engine, start_entities = None, input_length = 2, output_length = 4, max_generation=30):
        self.pop_size = pop_size
        self.entities = [0]*pop_size
        self.fitnesses = np.array(np.zeros((pop_size)))
        
        if start_entities is None:
            for i in range(pop_size):
                # print(i)
                self.entities[i] = Gnarl(engine, input_size=input_length, output_size=output_length)#.initial_structure()
                # self.entities[i].initial_structure()
                
        elif len(start_entities) < pop_size:
            self.entities[0:len(start_entities)] = start_entities
            for i in range(pop_size - len(start_entities)):
                self.entities[len(start_entities) + i] = Gnarl(engine, input_size=input_length, output_size=output_length).initial_structure()
                
        elif len(start_entities) >= pop_size:
            self.entities = start_entities[0:pop_size]
        
        for i in range(max_generation):
            # print(i,'a')
            [e.run() for e in self.entities]
            self.fitnesses = np.array([e.fitness for e in self.entities])
            print('Generation: ',i)
            # print('fitnesses: ',self.fitnesses)
            print('mean: ',self.fitnesses.mean(),'\n')
            self.nextGeneration()
            
        
                
                
        
    def nextGeneration(self):
        #get fitnesses
        sorted_args = self.fitnesses.argsort()[::-1]
        parents = [self.entities[p] for p in sorted_args][0:int(self.pop_size/2)]
        children = [e.ret() for e in parents]
        [e.mutate() for e in children]
        
        self.entities = parents
        self.entities.extend(children)
        


# if __name__ == '_main_':
print('qhh')
controller = gnarl_controller(50, 'cartpole', max_generation=20)
print([e for e in controller.entities])

