# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:07:02 2020

@author: samwh
"""

import random
import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.models     import Sequential
from keras.layers     import Dense
from keras.models     import load_model

import gym
gym.logger.set_level(40)
env = gym.make('CartPole-v1')
env.reset()


# lists containing model activations and optimizers to allow for randomisation
hidden_layer_activations = ['tanh', 'relu', 'sigmoid', 'linear', 'softmax']
model_optimizers = ['adam', 'rmsprop']

            
###############################################################################


# object class for storing instance of a global innovation number
class GIN():
    
    def __init__(self, val=0):
        
        self.val = val
        
    
    # increments the innovation value and returns the new value, improving code efficiency
    def i(self):
        
        self.val += 1
              
        return self.val
    
    
    # resets innovation value to 0
    def reset(self):
        
        self.val = 0


def gen_init_population(input_size, 
                        output_size, 
                        population_size,
                        gin = GIN(), 
                        activations = ['sigmoid'], 
                        optimizers = ['adam'], 
                        rand = True
                        ):
    
    # subfunction returns zero unless rand=True, in which case returns a random number from -1 to 1
    def new_val():
        
        if rand: return 2*random.random() - 1
        else: return 0
    
    # generate lists of input and output nodes
    input_nodes, output_nodes = [], []
    
    for i in range(input_size + output_size):
        
        if i < input_size: input_nodes.append(NodeGene(num=i+1, layer=0))
        else: output_nodes.append(NodeGene(num=i+1, layer=1))
    
    # generate initial population of chromosomes with densely connected outer layers
    init_population = []    
    
    for i in range(population_size):
        
        # generate connections between layers after resetting the innovation number to zero
        new_connections = []       
        gin.reset()
        
        for input_node in input_nodes:
            new_connections += [input_node.add_connection(output_node, new_val(), innovation=gin.i()) 
                                for output_node in output_nodes]
         
        # generate the chromosome object with node/connection gene information, and add it to the population
        init_chromosome = Chromosome(connection_genes = new_connections,           
                                     node_genes = input_nodes + output_nodes,                 
                                     input_size = input_size, 
                                     output_size = output_size,
                                     activation = random.choice(activations),              
                                     optimizer = random.choice(optimizers)
                                     )
        
        init_population.append(init_chromosome)
    
    return init_population


#function to run simulation with optional rendering and return a fitness value  
#currently this simply calls the 'play_cart' function which runs the cartpole gym env
def run_sim(model, goal_steps=500, render=False, games=10, _print=False):
    
    fitness = play_cart(model, goal_steps, render, games, _print)
    
    return fitness


def gen_child(parent1, parent2):
    
    
    

###############################################################################


'''
Functions taken from online example for running the OpenAI cartpole gym environment: 
https://blog.tanka.la/2018/10/19/build-your-first-ai-game-bot-using-openai-gym-keras-tensorflow-in-python/
'''

# function to trial neural model over specified number of games, using OpenAI gym
def play_cart(model, goal_steps=500, render=False, games=100, _print=True):
    
    scores = []
    choices = []
    
    for each_game in range(games):
        score = 0
        prev_obs = []
        for step_index in range(goal_steps):
            if render: env.render()
            if len(prev_obs)==0:
                action = random.randrange(0,2)
            else:
                action = np.argmax(model.predict(prev_obs))
                
            choices.append(action)
            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            score+=reward
            if done:
                break
        if _print: print('Score: ' + str(score))
        
        env.reset()
        scores.append(score)
        
    return sum(scores)/len(scores)


###############################################################################


input1 = NodeGene(bias=0, num=1, layer=0)
input2 = NodeGene(bias=0, num=2, layer=0)
input3 = NodeGene(bias=0, num=3, layer=0)
input4 = NodeGene(bias=0, num=4, layer=0)
hidden5 = NodeGene(bias=0, num=5, layer=0.5)
output6 = NodeGene(bias=0, num=6, layer=1)
output7 = NodeGene(bias=0, num=7, layer=1)

con1 = input1.add_connection(hidden5, weight=0.1)
con2 = input2.add_connection(hidden5, weight=0.2)
con3 = input3.add_connection(hidden5, weight=0.3)
con4 = input4.add_connection(output7, weight=0.4)
con5 = hidden5.add_connection(output7, weight=0.5)

activation=hidden_layer_activations[random.randint(0,len(hidden_layer_activations)-1)]
optimizer=model_optimizers[random.randint(0,len(model_optimizers)-1)]

chromosome = Chromosome(connection_genes=[con1, con2, con3, con4, con5],
                        node_genes=[input1, input2, input3, input4,
                                    hidden5,
                                    output6, output7],
                        activation=activation,
                        optimizer=optimizer
                        )

NN = chromosome.compile_network()
NN.get_weights(_print=True) 
