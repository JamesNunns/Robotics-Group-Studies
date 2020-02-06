import numpy as np
import random
import matplotlib.pyplot as plt
import pyglet
import Simulator

# Q-Learning parameters
alpha = 0.3
gamma = 0.9
epsilon = 0.1

# class Algorithm:
#     def __init__(self):
#         print("Init algorithm")
    
#     def reward(self, state, action):
#         print("Env step")
    
#     def action(self):




class Q_Learning:
    def __init__(self, q_table: np.array = np.zeros((21,5))):
        '''
        Initialise Q-table with pre-existing or new Q-table.
        '''
        np.savetxt('q_table.csv', q_table, delimiter=',') # Save q_table
        self.q_table = q_table

        self.episode = 1
        self.state = 0
    
    def env_step(self, env: Simulator):
        '''
        The action to take.
        '''
        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 4)  # Explore action space
        else:
            action = np.argmax(self.q_table[self.state])  # Exploit learned values
        
        env.action(action)  # Make action in the simulation

        next_state, reward = self.calc_reward(env, action, env.velocity)  # Determine new state

        old_value = self.q_table[self.state, action]  # Get old q_table value
        next_max = np.max(self.q_table[next_state])  # Find next max q_table values
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)  # Use Q-learning formula to calculateh how to change old values
        self.q_table[self.state, action] = new_value  # Append new value to q_table

        self.state = next_state  # Update current stat
    
    def calc_reward(self, env: Simulator, state: float, action: int):
        '''
        The reward function for the algorithm.
        '''
        # Calculate the reward of the previous action
        try: angle = int(env.swing.rod1._get_angle() * (180 / math.pi) - env._theta) # Calculate current rod angle
        except: angle = -90 # If angle is outside of bounds

        if angle > 90: angle = 90 # If above 90, set to 90
        if angle < -90: angle = -90 # If below 90, set to -90

        if action == 4: # If action is to do nothing...
            penalty = 0 # ...no penalty
        else:
            penalty = 50 # ...give penalty

        velocity = (env.angle_history[-2] - env.angle_history[-1]) * 60

        if (env.velocity < 0 and velocity > 0) or (env.velocity > 0 and velocity < 0): # If velocity has changed sign (aka at apex), determine reward
            reward = angle**2
        else:
            reward = 0
        
        # Calculate the new state
        state = int((round(env.velocity, -1) / 10) + 10)
        if state > 20: state = 20  # Put cap on
        if state < 0: state = 0  # velocities

        return state, reward - penalty  # Return (state, reward)
    
    def final(self, env):
        '''
        The final reward of the episode.
        '''
        print("Episode " + str(self.episode) + " complete! Saving Q-table...")

        self.episode += 1
        self.state = 0
        np.savetxt('q_table.csv', self.q_table, delimiter=',') # Save q_table

        # Save Q-table and angle history plot images
        fig = plt.figure()
        plt.matshow(self.q_table)
        plt.savefig('image1.png', bbox_inches='tight', dpi=56)
        plt.clf()

        fig = plt.figure()
        plt.plot(np.linspace(0, env.time, len(env.angle_history)), env.angle_history)
        plt.savefig('image2.png', bbox_inches='tight', dpi=56)
        plt.clf()

        plt.close('all')

        env.title = "Episode " + str(self.episode)

        print("Done!")


#####################
#### MAIN
#####################

if __name__ == "__main__":
    algorithm = Q_Learning(q_table=np.loadtxt('q_table.csv', delimiter=','))
    window = Simulator.Window(algorithm, timeout=60, title="Episode 1")  # Initialise window
    
    pyglet.clock.schedule_interval(window.update, 1.0/60)  # Schedule update method to run 60 times a second (FPS of window)
    pyglet.app.run()  # Run Pyglet windows