from keras.models import load_model
import numpy as np

class ML:
    '''
    Machine learning class that uses a neural network to output trained actions based on current states.
    '''
    def __init__(self, neural_net) -> None:
        '''
        Initialise the neural network.
        '''
        print("Loading neural network...", end=" ", flush=True)
        self.model = load_model('net.h5')
        print("Done!")

    def get_action(self, state: list) -> int:
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

        if state == None: # If there is no current state (i.e. at the start) makes a random move
            action = np.random.randint(0, 4)
        else: # the optimal move given the state
            action = np.argmax(self.model.predict(state.reshape(-1, len(state)))[0])
        
        return action