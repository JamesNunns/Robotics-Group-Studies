# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:34:54 2020

@author: Tom & Henry

Need to go into
"""

import numpy as np
import gym
from gnarl_mutate import Gnarl
# import construct_net_new




class GnarlController():
    '''
    Controller class used to make lots of pops and run for some gens 
    '''
    def __init__(self, pop_size, engine
                 , env=None, start_entities=None, input_length=4,
                 output_length=2, max_generation=30):

        self.pop_size = pop_size
        self.entities = [0]*pop_size
        self.fitnesses = np.array(np.zeros((pop_size)))

        if start_entities is None:
            for i in range(pop_size):
                # print(i)
                self.entities[i] = Gnarl(env, engine, input_size=input_length,
                                         output_size=output_length)
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
            print('Generation: ', i)
            # print('fitnesses: ',self.fitnesses)
            print('mean: ', self.fitnesses.mean(), '\n')
            self.next_generation()





    def next_generation(self):
        '''
        Runs a complete generation
        '''
        #get fitnesses
        sorted_args = self.fitnesses.argsort()[::-1]
        parents = [self.entities[p] for p in sorted_args][0:int(self.pop_size/2)]
        children = [e.ret() for e in parents]
        [e.mutate() for e in children]

        self.entities = parents
        self.entities.extend(children)



if __name__ == '__main__':

    print('qhh')
    controller = GnarlController(pop_size=50, env=gym.make('CartPole-v1'), 
                                  engine="cartpole", max_generation=20,
                                  input_length=4, output_length=2)
    print([e for e in controller.entities])
