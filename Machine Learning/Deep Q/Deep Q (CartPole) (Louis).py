#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: louismiranda-smedley

Comments:
--------
Making a DeepQNetwork, in an object-oriented way to mimic how we might
implement a similar structure in the swinging simulation.
"""


import gym
import keras
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam




class DeepQNetwork():
    def __init__(self, gamma, epsilon, epsilon_decay, epsilon_min, alpha, alpha_decay, batch_size, max_env_steps, n_episodes, n_win_ticks):
        
        #Hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        
        #Training parameters
        self.batch_size = batch_size
        self.memory = deque(maxlen=100000)
        
        #Gym environment parameters
        self.env = gym.make('CartPole-v0')
        self.max_env_steps = max_env_steps
        if self.max_env_steps is not None: self.env.max_episode_steps = self.max_env_steps
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks
        
        #Neural Net
        self.model = Sequential()
        self.model.add(Dense(24, input_dim=4, activation='tanh'))
        self.model.add(Dense(48, activation='tanh'))
        self.model.add(Dense(2, activation='linear'))
        
        self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))
        
        
    def remember(self, state, action, reward, next_state, done):
        ''' store previous states, actions, rewards, next_state and done statuses '''
        self.memory.append((state, action, reward, next_state, done))
    
    def choose_action(self, state, epsilon):
        ''' deciding whether to use model to predict or to take random action'''
        if np.random.random() <= epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.model.predict(state))

    def get_epsilon(self, t):
        ''' exploration factor changed with time'''
        return max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((t+1)*self.epsilon_decay)))

    def preprocess_state(self, state):
        ''' correct input shape for storing in memory '''
        return np.reshape(state, [1, 4])

    def replay(self, batch_size, epsilon):
        ''' trains the model based on remembered information '''
        x_batch, y_batch = [], []
        mini_batch = random.sample(self.memory, min(len(self.memory), batch_size))
    
        for state, action, reward, next_state, done in mini_batch:
            y_target = self.model.predict(state)
            if done:
                y_target[0][action] = reward
            else:
                y_target[0][action] = reward + self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            
        self.model.fit(np.array(x_batch), np.array(y_batch), batch_size = len(x_batch), verbose=0)
        
        if epsilon > self.epsilon_min:
            epsilon *= self.epsilon_decay
          
    def run(self):
        ''' runs the environment time step and chooses action and remembers outcome
            also feeds back into replay function to fit the model  '''
        
        mean_survival_time = 0
        survival_time = deque(maxlen=100)
        performance = []
        
        for e in range(self.n_episodes):
            state = self.preprocess_state(self.env.reset())
            done = False
            ticks = 0
            while not done:
                action = self.choose_action(state, self.get_epsilon(e))
                next_state, reward, done, _ = self.env.step(action)
                if mean_survival_time > 190: #<---only want to show when its close to solving
                    self.env.render()
                next_state = self.preprocess_state(next_state)
                self.remember(state, action, reward, next_state, done)
                state = next_state
                ticks += 1
                
            survival_time.append(ticks)
            mean_survival_time = np.mean(survival_time)
            
          
            if e % 100 == 0:
                performance.append(mean_survival_time)
                print(f'episodes {e}, mean score {mean_survival_time}')
            self.replay(self.batch_size, self.get_epsilon(e))

        return e, performance
    
    
if __name__ == '__main__':
    
    n_episodes = 4000 
    n_win_ticks = 195
    max_env_steps = None
    
    
    gamma = 1        #Discout Factor
    epsilon = 1      #Exploration Factor
    epsilon_decay =  0.995     #Less Explorative with time
    epsilon_min =  0.01        #Still non-zero after long times
    alpha =  0.01           #Learning Rate
    alpha_decay = 0.01      #Using previous actions to predict more with time
    
    batch_size = 64
    
    agent = DeepQNetwork(gamma, epsilon, epsilon_decay, epsilon_min, alpha, alpha_decay, batch_size, max_env_steps, n_episodes, n_win_ticks)
    agent.run()
    #performance = agent.run()[1]
    
    #Plotting how well the test did
    #plt.plot(np.arange(0,2000,100),performance,'r',label='fit')
    #plt.scatter(np.arange(0,2000,100),performance, label='average scores')
    #plt.hlines(y=195,xmin=0,xmax=2000, color='g', label='win score')
    #plt.ylabel('mean score for last 100 episodes')
    #plt.xlabel('number of episodes')
    #plt.title('Quality check of run')
    #plt.legend(loc=4)