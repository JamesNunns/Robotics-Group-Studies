# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:10:27 2020

@author: samwh


Section 1: Class to construct and manipulate Tensorflow models
Section 2: Classes and functions required for NEAT algorithm
Section 3: Functions required for OpenAI cartpole gym environment

Note:
    - Currently the algorithm is deliberately bottlenecked by starting each model
    without prior training (all weights start with random values) and only using a 
    small population size - this is so it doesn't just solve the cartpole instantly.
    - Mutations occur probabilistically so the number of generations required to 
    find a solution varies quite a lot

Plans for changes:
    - Experiment with different initial populations and mutation parameters
    - Maybe add a progress bar for each generation
    - Add swinging sims to use instead of cartpole
    - Seperate mutation function into multiple subfunctions for easier editing
    - Add ability to retain certain weights when a new layer is added rather than
    just randomising them
    - Maybe experiment with splitting the evolutionary process into an initial
    segment for finding the best architecture, then a secondary one to refine weights
"""


import random
import numpy as np
import matplotlib.pyplot as plt

# import tensorflow as tf
import keras
from keras.models     import Sequential
from keras.layers     import Dense
from keras.optimizers import Adam
from keras.models     import load_model

# gym.logger.set_level(40)

###############################################################################


'''
Class to define Neural Net object, capable of loading an existing network from a .h5 file 
e.g.     network_name = NeuralNet(file="Neural_Network.h5") 
OR training a new network from a 'training_data' array with specified 'architecture' (layer structure)
e.g.     network_name = NeuralNet(training_data=array_name, architecture=[10,10,10]) 
OR creating an untrained neural net with specified 'input_size', 'output_size' and 'architecture'
e.g.     network_name = NeuralNet(input_size=4, output_size=2, architecture=[10,10,10])

To train a model, call 'fit(training_data)' where training_data is a list of inputs and outputs 
Network can be saved to a .h5 file by calling the 'save(file_name)' method
To make a prediction, call 'predict(input_data)' method where input_data is an array of observations
Stored network architecture can be updated (e.g. after mutation) by calling 'get_architecture()' method
Return lists containing network weights and biases by calling 'get_weights()' (also updates internal variables)
Set network weights by calling 'set_weights(weights, biases)', input same data format as get_weights() output
'''

class NeuralNet():
    
    def __init__(self, 
                 file=None, 
                 architecture=None, 
                 input_size=None, 
                 output_size=None, 
                 training_data=None,
                 training_epochs=1):
        
        def build_model(input_size, output_size, architecture):
            
            model = Sequential()
            model.add(Dense(architecture[0], input_dim=input_size, activation='relu'))
            for i in range(1, len(architecture)):
                model.add(Dense(architecture[i], activation='relu'))
            model.add(Dense(output_size, activation='linear'))
            model.compile(loss='mse', optimizer=Adam())
           
            return model

        if training_data: input_size, output_size = len(training_data[0][0]), len(training_data[0][1])
        
        if file:
            
            self.model = load_model(file)
            print('Loaded ' + file, '\n')
            
        else: self.model = build_model(input_size, output_size, architecture)
        
        if training_data: self.fit(training_data, training_epochs)
        
        self.get_architecture()
        self.get_weights()
        
    
    #fits model to given training data    
    def fit(self, training_data, epochs=10):
            
        inputs = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
        outputs = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
        self.model.fit(inputs, outputs, epochs=epochs)
            
    
    #saves network inc. weights to a .h5py file with a given name
    def save(self, name='Neural_Network'):
        
        self.model.save(name + '.h5')
        print('Saved to {}'.format(name + '.h5'), '\n')
    
     
    #use the model to generate an output from a given input
    def predict(self, input_data):
        
        return self.model.predict(np.array(input_data).reshape(-1, len(input_data)))[0]
    
    
    #returns architecture (hidden layer structure) of network, also updates internal variables
    def get_architecture(self):
        
        architecture = []
        for layer in self.model.layers: architecture.append(layer.output_shape[1])
        
        self.output_size = architecture[-1]
        architecture.pop()
        self.architecture = architecture
        
        return architecture
    
    
    #outputs weights and biases of network, also updates internal variables
    def get_weights(self, _print=False):    
    
        weights, biases = [], []
        for layer in self.model.layers:
            weights.append(layer.get_weights()[0])
            biases.append(layer.get_weights()[1])
        
        if _print: print('Weights:', weights, '\n\nBiases:', biases, '\n')
        
        self.weights, self.biases = weights, biases
        self.input_size = len(weights[0])
        
        return weights, biases
    
    
    #accepts lists containing weights and biases and uses these to replace existing network weights
    def set_weights(self, weights, biases):
        
        count = 0
        for layer in self.model.layers:
            layer.set_weights([weights[count], biases[count]])
            count += 1
            
        self.get_weights()
    

###############################################################################
        

'''
Classes and functions for evolutionary algorithm. The main function 'NEAT()' runs the algorithm.
ALter the 'run_sim()' function to use a different simulation environment - currently using the
OpenAI cartpole env; this function must accept a Tensorflow model and return a 'fitness' value.

Current process for each generation:
    - Generate new population by randomly mutating best models of previous generation
    - Include 'parent' models from previous generation in new population
    - Sequentially test the fitness of each network by using the 'run_sim()' method
    - 
'''

#simple class to store a model and calculated fitness value
class Chromosome():
    
    def __init__(self, model, fitness):
        
        self.model, self.fitness = model, fitness
        

#function to run simulation with optional rendering and return a fitness value  
#currently this simply calls the 'play_cart' function which runs the cartpole gym env
def run_sim(model, env, goal_steps=500, render=False, games=100, _print=False):
    
    fitness = play_cart(model, env, goal_steps, render, games, _print)
    
    return fitness
    

#generate an initial population of random networks
def generate_population(population_size,
                        max_layer_size,
                        max_nodes,
                        input_size,
                        output_size):
    
    population = [NeuralNet(None, 
                            [random.randint(1,max_nodes) for i in range(random.randint(1,max_layer_size))], 
                            input_size, 
                            output_size, 
                            None, 
                            1)
                  for i in range(population_size)]
    
    return population
    

#mutate a given neural net
def mutate(neural_net, 
           add_layer_prob=0.1,              #probability to add a new layer          
           max_layers=10,                   #max number of hidden layers
           add_node_prob=0.1,               #probability to add a new node to a layer
           max_nodes=512,                   #max number of nodes in each hidden layer
           alt_weight_prob=0.1,             #probability to alter a weight
           alt_bias_prob=0.1,               #probability to alter a bias         
           allow_del=True,                  #allow nodes to be deleted
           gaussian=True,                   #randomise weights/biases by gaussian noise rather than simple random()
           gauss_std=None):                 #standard deviation of gaussian noise
    
    #get existing weights, biases and architecture from neural net
    weights, biases = neural_net.get_weights()
    architecture = neural_net.get_architecture()
    
    #default gauss_std is currently just a random number (may change)
    if gaussian and not gauss_std: gauss_std = random.random() - 0.5
              
    #duplicate layer
    if random.random() < add_layer_prob and len(architecture) < max_layers:
        
        #choose random layer to duplicate and random new position
        index = random.randint(0, len(architecture))
        architecture.insert(index, architecture[random.randint(0, len(architecture)-1)])
        
        #generate random weights and biases and insert them into weights/biases arrays
        #(currently this does not take into account previous weights - may change)
        new_layer_weights = [[[2*random.random() - 1 for j in range(architecture[index])] for i in range(len(weights[index]))], 
                             [[2*random.random() - 1 for j in range(len(weights[index][0]))] for i in range(architecture[index])]]
        
        del weights[index]
        for i in range(2): weights.insert(index+i, np.array(new_layer_weights[i]))
        biases.insert(index, np.array([0 for i in range(architecture[index])]))        
            
    #add or delete nodes        
    for layer in range(len(architecture)):
        
        if random.random() > add_node_prob or architecture[layer] == max_nodes: continue
        
        #generate a random number of nodes to add, positive or negative
        #currently this is always produced in a gaussian dist.
        diff = int(random.gauss(0, architecture[layer]**0.5))  
        
        #if deletion is not allowed or layer size is too small, use modulus of diff
        if not allow_del or architecture[layer] + diff < 1: diff = abs(diff)
        
        #alter architecture - if new node count exceeds the maximum, use the maximum value
        if architecture[layer] + diff > max_nodes: architecture[layer] = max_nodes
        else: architecture[layer] += diff
        
        #subroutine to handle deletion of nodes
        if diff < 0: 
            
            weights[layer] = np.delete(weights[layer], [len(weights[layer][0]) - 1 - i for i in range(abs(diff))], 1)
            weights[layer+1] = np.delete(weights[layer+1], [len(weights[layer+1]) - 1 - i for i in range(abs(diff))], 0)
            
            biases[layer] = np.delete(biases[layer], [len(biases[layer]) - 1 - i for i in range(abs(diff))])
            
        #subroutine to handle addition of new nodes
        elif diff > 0:
            
            new_layer = []
            for i in range(len(weights[layer])):
                l = [elem for elem in weights[layer][i]]
                for j in range(diff): l.append(2*random.random() - 1)
                new_layer.append(np.array(l))
            
            weights[layer] = np.array(new_layer)
            
            new_layer = []
            for i in range(len(weights[layer+1])): new_layer.append(np.array([elem for elem in weights[layer+1][i]]))
            for i in range(diff): new_layer.append(np.array([2*random.random() - 1 for j in range(len(weights[layer+1][0]))]))
            
            weights[layer+1] = np.array(new_layer)
            
            biases[layer] = np.append(biases[layer], [0 for i in range(diff)])  
        
    #change weight values
    for layer in range(len(weights)):
        for node in range(len(weights[layer])):
            for connection in range(len(weights[layer][node])):
                
                if random.random() > alt_weight_prob: continue
                val = weights[layer][node][connection]
                
                #for gaussian mutation, alter value by gaussian with previous value as mean
                if gaussian: weights[layer][node][connection] = random.gauss(val, gauss_std)
                 
                #prevents weights > 1 or < -1
                if weights[layer][node][connection] < -1: weights[layer][node][connection] = -1
                elif weights[layer][node][connection] > 1: weights[layer][node][connection] = 1
                  
                #for non gaussian mutation, choose a random value between -1 and 1
                else: weights[layer][node][connection] = 2*random.random() - 1

    #change bias values
    for layer in range(len(biases)):
        for node in range(len(biases[layer])):
            
            if random.random() > alt_bias_prob: continue
            val = biases[layer][node]
            
            #for gaussian mutation, alter value by gaussian with previous value as mean
            if gaussian: biases[layer][node] = random.gauss(val, gauss_std)
                
            #prevents biases > 1 or < -1
            if biases[layer][node] < -1: biases[layer][node] = -1
            elif biases[layer][node] > 1: biases[layer][node] = 1
            
            #for non gaussian mutation, choose a random value between -1 and 1
            else: biases[layer][node] = 2*random.random() - 1
    
    new_network = NeuralNet(None, architecture, neural_net.input_size, neural_net.output_size, None, 1)
    new_network.set_weights(weights, biases)
    
    return new_network


#generate new generation of networks by mutating randomly selected parent networks
def evolve_population(parents,                          #list of parent networks
                      population_size,
                      
                      #mutation variables:
                      add_layer_prob=0.1,
                      max_layers=10,
                      add_node_prob=0.1,
                      max_nodes=512,
                      alt_weight_prob=0.1,
                      alt_bias_prob=0.1,
                      allow_del=True,
                      gaussian=True,
                      gauss_std=None):
    
    #generate a list of mutated networks
    population = [mutate(parents[random.randint(0, len(parents) - 1)],
                         add_layer_prob,          
                         max_layers,
                         add_node_prob,
                         max_nodes,
                         alt_weight_prob,
                         alt_bias_prob,
                         allow_del,
                         gaussian,
                         gauss_std) 
                  for i in range(population_size - len(parents))]
     
    #add best of previous generation to new list       
    population.extend(parents)
    
    return population


#function to run the main evolutionary algorithm
def NEAT(init_population=None,              #allows for input of an initial list of models
         input_size=None,                   #model input size
         output_size=None,                  #model output size
         training_data=None,                #training data for initial model (optional)
         training_epochs=1,                 #number of epochs through which to train initial model
         max_generations=20,                #number of generations to iterate through
         population_size=50,                #population size for each generation
         breed_ratio=0.1,                   #ratio of previous population carried over to the next
         
         _print=True,                       #print details of each generation
         render=True,                       #render best model of generation
         render_runs=5,                     #number of simulation runs for best model
         env=None,
         
         #mutation variables:
         add_layer_prob=0.1,        
         max_layers=10,             
         add_node_prob=0.1,         
         max_nodes=512,             
         alt_weight_prob=0.1,
         alt_bias_prob=0.1,
         allow_del=True,
         gaussian=True,
         gauss_std=None):
    
    #if no init_population is provided, generate random 
    if not init_population: init_population = [NeuralNet(None, [1], input_size, output_size, training_data, training_epochs)]
    elif type(init_population) == str: init_population = [NeuralNet(init_population, [2], input_size, output_size, training_data, training_epochs)]
     
    #main evolutionary algorithm loop           
    for gen in range(max_generations):
        
        #generate new population
        new_population = evolve_population(init_population, population_size)
        init_population, chromosomes, fitness_dist = [], [], []
        
        #iteratre through new population
        for model in new_population:
            
            #find and record fitness value for each model
            fitness = run_sim(model, env, goal_steps=500000000, render=False, games=1, _print=False)
            
            chromosomes.append(Chromosome(model, fitness))
            fitness_dist.append(fitness)
        
        #find the 'threshold' fitness based on the percentage of models allowed to survive
        fitness_dist.sort(reverse=True)
        fitness_threshold = fitness_dist[int(population_size*breed_ratio)]
        
        #find the best fitness of the generation
        best_fitness = fitness_dist[0]
        
        #use the above to find the best models in the generation
        for chromosome in chromosomes:
            
            if chromosome.fitness >= fitness_threshold: 
                
                init_population.append(chromosome.model)
                if chromosome.fitness == best_fitness: best_model = chromosome.model
        
        if _print:
            
            print('Best score for gen {}:'.format(gen), best_fitness)
            print('Best model architecture:', best_model.architecture, '\n')
        
        run_sim(model=best_model, env=env, goal_steps=500, render=render, games=render_runs, _print=False)
        
    return best_model, init_population


###############################################################################


'''
Functions taken from online example for running the OpenAI cartpole gym environment: 
https://blog.tanka.la/2018/10/19/build-your-first-ai-game-bot-using-openai-gym-keras-tensorflow-in-python/
'''

#Function to trial neural model over specified number of games, using OpenAI gym
def play_cart(model, env, goal_steps=500, render=False, games=100, _print=True):
    
    scores = []
    choices = []
    
    for each_game in range(games):
        score = 0
        prev_obs = []
        for step_index in range(goal_steps):
            # if render: env.render(model)
            if len(prev_obs)==0:
                action = random.randrange(0, 5)
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
    

#Data preparation for initial network training, using OpenAI gym 'Cartpole'
def model_data_preparation(env, goal_steps=500, score_requirement=60, initial_games=10000):
            
    training_data = []
    accepted_scores = []
    
    for game_index in range(initial_games):
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(goal_steps):
            action = random.randrange(0, 5)
            observation, reward, done, info = env.step(action)
            
            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])
                
            previous_observation = observation
            score += reward
            if done:
                break
            
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]
                training_data.append([data[0], output])
        
        env.reset()

    #print(accepted_scores)
    
    return training_data


###############################################################################  
   

'''    
#a few demonstrations of using the NeuralNet class
goal_steps=500
score_requirement=10
initial_games=1000
        
training_data = model_data_preparation(goal_steps, score_requirement, initial_games)

NN = NeuralNet(architecture=[128,52,20], training_data=training_data)
print(NN.weights)
NN.save()

NN_opened = NeuralNet(file='Network_Weights.h5')
print('Layer architecture: ', NN_opened.get_architecture())
play_cart(NN_opened, goal_steps, render=True, games=100)

'''    





def main():
    environment = input("Environment (gym / pymunk / unity): ")

    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    #optional generation of initial population
    init_population = generate_population(population_size=20,
                                            max_layer_size=5,
                                            max_nodes=32,
                                            input_size=2,
                                            output_size=5)

    if environment == 'gym': # Run Gym sim
        import gym
        env = gym.make('CartPole-v0')
    elif environment == 'pymunk': # Run Pymunk sim
        from Pymunk import Swing
        env = Swing()
    elif environment == 'unity': # Run Unity sim
        from Unity import Unity
        env = Unity()

    env.reset()
    best_model, init_population = NEAT(init_population=init_population,
                                        input_size=2, 
                                        output_size=5, 
                                        max_generations=20, 
                                        population_size=50,
                                        render_runs=1,
                                        breed_ratio=0.5,
                                        env=env)
    
    best_model.save()
    env.render(best_model, timeout=500)




# net = NeuralNet(file='Genetic (Simple).h5')
# env.render(net.model, timeout=500)

# best_model.save()
# env.render(best_model, timeout=5000)