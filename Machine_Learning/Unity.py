from pynput.keyboard import Key, Controller
from keras.models import load_model
import numpy as np
import time

class Unity:
    '''
    Machine learning class that uses a neural network to output trained actions based on current states.
    '''
    def __init__(self, timeout: int = 30):
        '''
        Initialise the neural network.
        '''
        for i in range(10):
            print(str(10 - i), end=" ", flush=True)
            time.sleep(1)
        
        print("Go!")
        print("Generating Unity wrapper...", end=" ", flush=True)

        self.keyboard = Controller()

        self.state = self.reset()
        self.timeout = timeout

        print("Done!")
    
    def reset(self):
        '''
        Reset the environment (returns state).
        '''
        self.start_time = time.time()
        self.time = 0
        self.max_angle = 0

        self.keyboard.press('y')
        self.keyboard.release('y')

        return self.get_state()

    def step(self, action: int):
        '''
        Time step the environment.
        '''
        time.sleep(1.0 / 10)

        self.time = time.time() - self.start_time # Determine current time

        penalty = self.perform_action(action) # Perform action

        old_state = self.state # Save old state
        new_state = self.get_state() # Calculate new state

        if abs(self.state[0]) > self.max_angle: self.max_angle = abs(self.state[0]) # Update max angle

        reward = 0
        if ((old_state[1] < 0 and new_state[1] > 0) or (old_state[1] > 0 and new_state[1] < 0)) or ((old_state[0] < 0 and new_state[0] > 0) or (old_state[0] > 0 and new_state[0] < 0)): # Only do rewards at apexes or minimum of swing
            reward = 2 * new_state[0]**3 + new_state[1]**3
        
        done = self.time > self.timeout # Simulation timed out

        self.state = self.get_state() # Update current state

        return (self.state, reward - penalty, done, {})

    def perform_action(self, action: int):
        '''
        Presses the key for that specific action.
        u = legs out
        i = legs in
        o = torso out
        p = torso in
        '''
        penalty = 0
        
        if action == 0:
            self.keyboard.press('u')
            self.keyboard.release('u')
            penalty = 5
        elif action == 1:
            self.keyboard.press('i')
            self.keyboard.release('i')
            penalty = 5
        elif action == 2:
            self.keyboard.press('o')
            self.keyboard.release('o')
            penalty = 5
        elif action == 3:
            self.keyboard.press('p')
            self.keyboard.release('p')
            penalty = 5
        
        return penalty
    
    def get_state(self):
        '''
        Reads the current angle of the swing from a text file.
        '''
        try:
            f = open('state.txt')
            state = f.readlines()[0].split(' ')
            f.close()
            out = [float(state[0]), float(state[1])]
        except:
            out = [0.0, 0.0]

        return out
