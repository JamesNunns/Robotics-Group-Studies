from keras.models import load_model
import numpy as np
import pickle
from neat import nn

class ML:
    '''
    Machine learning class that uses a neural network to output trained actions based on current states.
    '''
    def __init__(self, neural_net):
        '''
        Initialise the neural network.
        '''
        # print("Loading neural network...", end=" ", flush=True)
        try:
            self.model = load_model(neural_net)
        except:
            with open(neural_net, "rb") as f:
                winner = pickle.load(f)
            winner_net = nn.create_feed_forward_phenotype(winner)
        # print("Done!")

    def get_action(self, state = None):
        '''
        Takes the current state, [angle, angular velocity], and returns an integer depending on the calculated optimal move.
        Note that angle has units of degrees and angular velocity has units of degrees/second.

        Actions:
            0 - Legs out
            1 - Legs in
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
        try:
            action = np.argmax(self.model.predict(state.reshape(-1, len(state)))[0])
        except:
            action = np.argmax(self.model.serial_activate(state))
        
        return action