from keras.models import load_model
import numpy as np
from sys import path

class ML:
    '''
    Machine learning class that uses a neural network to output trained actions based on current states.
    '''
    def __init__(self):
        '''
        Initialise the neural network.
        '''
        # print("Loading neural network...", end=" ", flush=True)
        self.model = load_model('/home/demo/Documents/Robotics_2020/Robotics-Group-Studies/Machine_Learning/Genetic_(Simple).h5')
        # print("Done!")

    def get_action(self, state = None):
        '''
        Takes the current state, [angle, angular velocity], and returns an integer depending on the calculated optimal move.
        Note that angle has units of degrees and angular velocity has units of degrees/second.

        Actions:
            0 - Legs in
            1 - Legs out
            2 - Torso out
            3 - Torso in
            4 - Do nothing

        Parameters
        ----------
        state : Array
            the current angle and angular velocity of the rod.

        Returns
        -------
        action : int
            optimal action decided by the trained neural net.
        '''
        state = np.array(state)

        action = np.argmax(self.model.predict(state.reshape(-1, len(state)))[0])
        
        return action
