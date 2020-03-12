from pynput.keyboard import Key, Controller
from keras.models import load_model
import numpy as np
import time

class Unity:
    '''
    Machine learning class that uses a neural network to output trained actions based on current states.
    '''
    def __init__(self, timeout: int = 60):
        '''
        Initialise the neural network.
        '''
        print("Please start the Unity simulation and click on the environment window.")

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

        return self.get_state()[0:2]

    def step(self, action: int):
        '''
        Time step the environment.
        '''
        if ((action == 0 or action == 1) and not self.get_state()[4]) or ((action == 2 or action == 3) and not self.get_state()[3]):
            self.perform_action(action) # Perform action
        self.time = time.time() - self.start_time # Determine current time

        old_state = self.state # Save old state
        new_state = self.get_state()[0:2] # Calculate new state
        penalty = self.get_state()[2] / 100

        time.sleep(1.0 / 50)
        # if action == 0 or action == 1: # Action involves legs
        #     while self.get_state()[4]: time.sleep(1.0 / 50) # Wait until not moving
        # if action == 2 or action == 3: # Action involves torso
        #     while self.get_state()[3]: time.sleep(1.0 / 50) # Wait until not moving

        if abs(new_state[0]) > self.max_angle: self.max_angle = abs(new_state[0]) # Update max angle

        reward = 0
        if ((old_state[1] < 0 and new_state[1] > 0) or (old_state[1] > 0 and new_state[1] < 0)) or ((old_state[0] < 0 and new_state[0] > 0) or (old_state[0] > 0 and new_state[0] < 0)): # Only do rewards at apexes or minimum of swing
            reward = 2 * new_state[0]**2 + new_state[1]**2
        
        done = self.time > self.timeout # Simulation timed out

        self.state = new_state # Update current state

        return (self.state, reward - penalty, done, {})

    def perform_action(self, action: int):
        '''
        Presses the key for that specific action.
        u = legs out
        i = legs in
        o = torso out
        p = torso in
        '''
        if (action == 0 and not self.get_state()[4]):
            self.keyboard.press('u')
            self.keyboard.release('u')
        elif (action == 1 and not self.get_state()[4]):
            self.keyboard.press('i')
            self.keyboard.release('i')
        elif (action == 2 and not self.get_state()[3]):
            self.keyboard.press('o')
            self.keyboard.release('o')
        elif (action == 3 and not self.get_state()[3]):
            self.keyboard.press('p')
            self.keyboard.release('p')
    
    def get_state(self):
        '''
        Reads the current angle of the swing from a text file.
        '''
        try:
            f = open('state.txt')
            state = f.readlines()[0].split(' ')
            f.close()
            out = [float(state[0]), float(state[1]), float(state[2]), eval(state[3]), eval(state[4])]
        except:
            out = [0.0, 0.0, 0.0, False, False]

        return out
    
def render(neural_net: str):
    '''
    Render a neural network model.
    '''
    try:
        model = load_model(neural_net)
    except:
        with open(neural_net, "rb") as f:
            winner = pickle.load(f)
        winner_net = nn.create_feed_forward_phenotype(winner)
    unity = Unity()

    while True:
        state = np.array(unity.get_state()[0:2])
        try:
            action = np.argmax(model.predict(state.reshape(-1, len(state)))[0])
        except:
            action = np.argmax(model.serial_activate(state))
        unity.perform_action(action)
        time.sleep(1.0 / 10)
