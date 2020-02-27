import keras
import random
import math
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam



class Agent:
    '''
    'Agent' class that represents the actions taken by a single neural network.
    '''

    def __init__(self, neural_net, input_size, output_size):
        '''
        Initialise class with the neural network.
        '''
        self.input_size = input_size
        self.output_size = output_size

        self.neural_net = neural_net
        self.memory = []
        self.performance = []

        self.epsilon = 1                # Exploration factor
        self.epsilon_decay =  0.995     # Less exploration with time
        self.epsilon_min =  0.01        # Still non-zero exploration after long time

        self.state = deque(maxlen=2)
        self.state.append(np.reshape([0] * self.input_size, [1, self.input_size]))
        self.action = 0
    
    def perform_action(self, state, reward, done):
        '''
        Takes state as [angle, velocity] and reward representing reward of previous action.
        Returns outputs as [leg_angle, torso_angle].
        '''
        self.state.append(np.reshape(state, [1, self.input_size]))
        self.memory.append((self.state[0], self.action, reward, self.state[1], done))
        self.performance.append(reward)

        self.epsilon = max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((len(self.memory)) * self.epsilon_decay / 10000))) # Decay epsilon to reduce exploration
        if np.random.random() <= self.epsilon:
            self.action = random.randrange(0, (self.output_size * 2) + 1)                     # Explore action space
        else:
            self.action = np.argmax(self.neural_net.predict(self.state[1]))  # Explore rewarding states
        
        output = [0] * self.output_size
        if self.action == 0:
            pass
        elif self.action % 2 == 1:  # Odd number
            output[self.action // 2] = 1
        elif self.action % 2 == 0:  # Even number
            output[(self.action // 2) - 1] = -1
        
        return output

class Controller(list):
    '''
    'Controller' class that manages the updating of neural networks for a list of agents.
    '''

    def __init__(self, input_size, output_size):
        '''
        Initialise the class with learning parameters.
        '''
        self.input_size = input_size
        self.output_size = output_size

        self.alpha =  0.01               # Learning rate
        self.alpha_decay = 0.01          # Using previous actions to predict more with time
        self.gamma = 1                   # Discout factor
    
    def make_agent(self):
        '''
        Create agent using Keras neural network.
        '''
        neural_net = Sequential()
        neural_net.add(Dense(52, input_dim=self.input_size, activation='tanh'))
        neural_net.add(Dense(128, activation='tanh'))
        neural_net.add(Dense((self.output_size * 2) + 1, activation='linear'))
        neural_net.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))
         
        super().append(Agent(neural_net, self.input_size, self.output_size))

    def replay(self, agent, batch_size = 64):
        '''
        Trains the model based on remembered information.
        '''
        x_batch, y_batch = [], []
        mini_batch = random.sample(agent.memory, min(len(agent.memory), batch_size))
    
        for state, action, reward, next_state, done in mini_batch:
            y_target = agent.neural_net.predict(state)
            if done:
                y_target[0][action] = reward
            else:
                y_target[0][action] = reward + self.gamma * np.max(agent.neural_net.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            
        agent.neural_net.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)
    
    def step(self):
        '''
        Run RL algorithms based on memory of each agent.
        '''
        for agent in self:
            self.replay(agent)
        
        return self





# if __name__ == "__main__":
#     '''
#     Testing.
#     '''
#     c = Controller(2, 2)
#     c.make_agent()

#     for i in range(20):
#         print(c[0].perform_action([1,i], i, False))
#         c.step()
    
#     print(c[0].perform_action([1,i], i, True))
#     c.step()
#     print(c[0].performance)
