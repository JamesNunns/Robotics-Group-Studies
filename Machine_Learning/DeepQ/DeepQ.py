import keras
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model
import pandas as pd



class DeepQ:
    '''
    Deep Q-Learning algorithm using Keras to update a neural network episodically.
    '''
    
    def __init__(self, environment):
        '''
        Initialise the environment and neural network.
        '''
        print("\n------------------------------------------")
        print("          DEEP Q-LEARNING USING             ")
        print("                NEURAL NETS                 ")
        print("------------------------------------------\n")

        # Hyperparameters
        self.alpha =  0.01              # Learning rate
        self.alpha_decay = 0.01         # Using previous actions to predict more with time
        self.gamma = 1                  # Discout factor
        self.epsilon = 1                # Exploration factor
        self.epsilon_decay =  0.98      # Less exploration with time
        self.epsilon_min =  0.01        # Still non-zero exploration after long time

        # Memory
        self.memory = []
        self.rewards = deque(maxlen=100)
        self.performance = []
        self.max_angles = []
        self.actions = []
        self.epoch = 0

        # Swing simulation environment
        self.env = environment

        # Neural network
        self.neural_net = self.generate_network()

        print("Ready!\n")
    
    def generate_network(self):
        '''
        Generate the neural network.
        '''
        print("Generating neural network...", end=" ", flush=True)

        neural_net = Sequential()
        neural_net.add(Dense(52, input_dim=2, activation='tanh'))
        neural_net.add(Dense(128, activation='tanh'))
        neural_net.add(Dense(5, activation='linear'))
        neural_net.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))

        print("Done!")
        return neural_net

    def replay(self, batch_size: int = 64):
        '''
        Trains the model based on remembered information.
        '''
        x_batch, y_batch = [], []
        mini_batch = random.sample(self.memory, min(len(self.memory), batch_size))
    
        for state, action, reward, next_state, done in mini_batch:
            y_target = self.neural_net.predict(state)
            if done:
                y_target[0][action] = reward
            else:
                y_target[0][action] = reward + self.gamma * np.max(self.neural_net.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            
        self.neural_net.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def run(self, episodes: int = -1):
        '''
        Run deep Q-learning algorithm.
        '''
        print("Running deep Q-learning algorithm...\n")
    
        print("  |--------------|---------|-------------|-----------------|-------------|")
        print("  |    Epoch     |  Score  |   Epsilon   |     Actions     |  Max Angle  |")
        print("  |--------------|---------|-------------|-----------------|-------------|")

        try:
            for e in range(self.epoch, episodes + self.epoch):
                print("  |  Episode " + str(e + 1) + str(" " * (4 - (len(str(e + 1))))), end="", flush=True)

                state = np.reshape(self.env.reset(), [1, 2])
                done = False
                score = 0
                actions = [0, 0, 0, 0, 0]

                while not done:

                    self.epislon = max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((e + 1) * self.epsilon_decay)))

                    if np.random.random() <= self.epsilon:
                        action = random.randrange(0, 5)
                    else:
                        action = np.argmax(self.neural_net.predict(state))
                    
                    actions[action] += 1

                    next_state, reward, done, _ = self.env.step(action)

                    next_state = np.reshape(next_state, [1, 2])
                    self.memory.append((state, action, reward, next_state, done))
                    state = next_state

                    score += reward
                
                self.actions.append(actions)
                self.rewards.append(score)
                self.performance.append(np.mean(self.rewards))
                self.max_angles.append(self.env.max_angle)
                self.replay()

                print("|" + str(" " * (8 - (len(str(int(np.mean(self.rewards))))))) + str(int(np.mean(self.rewards))) + " ", end="", flush=True)
                print("|" + str(" " * (10 - (len(str(round(self.epsilon, 4)))))) + str(round(self.epsilon, 4)) + "   ", end="", flush=True)
                a = str(int(100 * actions[0] / sum(actions))) + "/" + str(int(100 * actions[1] / sum(actions))) + "/" + str(int(100 * actions[2] / sum(actions))) + "/" + str(int(100 * actions[3] / sum(actions))) + "/" + str(int(100 * actions[4] / sum(actions)))
                print("|" + str(" " * (15 - (len(a)))) + a + "  ", end="", flush=True)
                print("|" + str(" " * (7 - (len(str(int(self.env.max_angle)))))) + str(int(self.env.max_angle)) + "      |")
                
        except KeyboardInterrupt:
            print("\nExited at " + str(e) + " episodes.")
            e -= 1

        self.epoch = e + 1

        print("\nDone!\n")
        return e, self.performance
    
    def render_sim(self, title: str, timeout: int = 60):
        '''
        Render simulation of the current neural network.
        '''
        self.env.render(self.neural_net, title, timeout)
    
    def render_actions(self):
        '''
        Render percentage stacked area chart showing action chosen at each epoch.
        '''
        print("Plotting graph of actions over epochs...", end=" ", flush=True)

        data = pd.DataFrame({'legs_out':[i[0] for i in self.actions], 'legs_in':[i[1] for i in self.actions], 'torso_out':[i[2] for i in self.actions], 'torso_in':[i[3] for i in self.actions], 'nothing':[i[4] for i in self.actions], }, index=range(0, self.epoch))
        data_perc = data.divide(data.sum(axis=1), axis=0)

        plt.stackplot(range(0, self.epoch),  data_perc["legs_out"],  data_perc["legs_in"],  data_perc["torso_out"],  data_perc["torso_in"],  data_perc["nothing"], labels=['Legs out', 'Legs in', 'Torso out', 'Torso in', 'Nothing'])
        plt.plot(range(0, self.epoch), (np.array(self.performance) - np.min(self.performance)) / np.max(np.array(self.performance) - np.min(self.performance)), 'black', label='Performance')
        plt.plot(range(0, self.epoch), (np.array(self.max_angles) - np.min(self.max_angles)) / np.max(np.array(self.max_angles) - np.min(self.max_angles)), 'w', label='Max Angle')
        plt.legend(loc='upper left')
        plt.margins(0, 0)
        plt.title("Choice of action at increasing epoch")
        plt.xlabel("Epoch")
        plt.ylabel("Probability")
        plt.show()

        print("Done!\n")
    
    def save(self, name: str = "DeepQ"):
        '''
        Save the current neural network model.
        '''
        self.neural_net.save(name + ".h5")
        print("Saved to " + str(name) + ".h5\n")
    
    def load(self, name: str = "DeepQ"):
        '''
        Load a saved neural network model.
        '''
        self.neural_net = load_model(name + ".h5")
        print("Loaded " + name + '.h5\n')


def main():
    environment = input("Environment (gym / pymunk / unity): ")

    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    load = input("Load net? ([name] / no) ")
    if load == '': load = 'DeepQ'
    if not load == 'no': epsilon = float(input("Epsilon: "))

    if environment == 'gym': # Run Gym sim
        import gym
        q = DeepQ(gym.make('CartPole-v0')) # TODO Make gym work
    elif environment == 'pymunk': # Run Pymunk sim
        from Pymunk import Swing
        q = DeepQ(Swing())
    elif environment == 'unity': # Run Unity sim
        from Unity import Unity
        q = DeepQ(Unity())
    
    if not load == 'no':
        q.load(load)
        q.epsilon = epsilon
    
    q.run(1000)
    q.save()
    q.render_actions()
    q.render_sim("Simulation")
