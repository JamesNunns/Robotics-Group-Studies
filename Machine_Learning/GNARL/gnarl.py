# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:34:54 2020

@author: Tom & Henry

Need to go into
"""

import numpy as np
from tqdm import tqdm
from gnarl_mutate import Gnarl
# import construct_net_new




class GnarlController():
    '''
    Controller class used to make lots of pops and run for some gens 
    '''
    def __init__(self, pop_size, engine
                 , env=None, start_entities=None, input_length=4,
                 output_length=2, max_generation=30, max_fitness=0):

        print('''
  _______ .__   __.      ___      .______       __      
 /  _____||  \ |  |     /   \     |   _  \     |  |     
|  |  __  |   \|  |    /  ^  \    |  |_)  |    |  |     
|  | |_ | |  . `  |   /  /_\  \   |      /     |  |     
|  |__| | |  |\   |  /  _____  \  |  |\  \----.|  `----.
 \______| |__| \__| /__/     \__\ | _| `._____||_______|''')

        self.pop_size = pop_size
        self.entities = [0]*pop_size
        self.fitnesses = np.array(np.zeros((pop_size)))
        self.max_generation = max_generation
        self.max_fitness = max_fitness

        if start_entities is None:
            # for i in range(50):
            for i in range(pop_size):
                # print(i)
                self.entities[i] = Gnarl(env, engine, input_size=input_length,
                                         output_size=output_length, 
                                         max_fitness = self.max_fitness)
                    # self.entities[i].initial_structure()

        elif len(start_entities) < pop_size:
            self.entities[0:len(start_entities)] = start_entities
            for i in range(pop_size - len(start_entities)):
                self.entities[len(start_entities) + i] = Gnarl(engine, input_size=input_length, output_size=output_length).initial_structure()

        elif len(start_entities) >= pop_size:
            self.entities = start_entities[0:pop_size]


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


    
    def main(self):
        '''
        After initialising a net, call this function which will return the bst
        net
        '''
        for i in range(self.max_generation):
            print("\nGeneration " + str(i + 1))
            # print(i,'a')
            for e in tqdm(range(len(self.entities))): self.entities[e].run()
            self.fitnesses = np.array([e.fitness for e in self.entities])
            # print('Generation: ', i)
        
            print('Fitnesses: ',self.fitnesses)
            print('Mean: ', self.fitnesses.mean(), '\n')
            self.next_generation()
            
        sorted_chromosomes = sorted(self.entities, key=lambda x: x.fitness, reverse=True)
        print('Best net fitness: {}'.format(sorted_chromosomes[0].fitness))
        return sorted_chromosomes[0].chromosome.model             





# MAIN

def main():
    print("\nPlease select environment:")
    print(" [1] OpenAI Gym CartPole-v0")
    print(" [2] Pymunk")
    print(" [3] 3D Unity")

    environment = input("--> ")

    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    inp = 2
    out  = 5
    fitness = 1000000
    if environment == '1': # Run Gym sim
        print("Running GNARL with the OpenAI Gym CartPole-v0 environment...\n")
        import gym
        env = gym.make('CartPole-v0')
        inp = 4
        out = 2
        fitness = 500
    elif environment == '2': # Run Pymunk sim
        print("Running GNARL with the Pymunk environment...\n")
        from Pymunk import Swing
        env = Swing()
    elif environment == '3': # Run Unity sim
        print("Running GNARL with the 3D Unity environment...\n")
        from Unity import Unity
        env = Unity()
    
    env.reset()

    # initialise NEAT object (increase best_model_runs to show each winning genome perform)
    controller = GnarlController(pop_size=20, env=env, 
                                  engine="cartpole", max_generation=20,
                                  input_length=inp, output_length=out, 
                                  max_fitness=fitness)
    
    net = controller.main()

    # name = input("Net name: ")\
    # neat.best_model.save(name)
    # print("Net saved as " + name + ".h5")
    # try:
    #     env.render()
    # except:
    #     env.render(best_model, timeout=500)

# if __name__ == '__main__':

#     print('qhh')
#     controller = GnarlController(pop_size=50, env=gym.make('CartPole-v1'), 
#                                   engine="cartpole", max_generation=20,
#                                   input_length=4, output_length=2, 
#                                   max_fitness = 500)
#     net = controller.main()
#     print(net)
#     # controller.next_generation()
#     # print([e for e in controller.entities])
