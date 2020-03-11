import time as tme
import numpy as np
from utility_functions import sign_zero

class Nothing():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_be = values['be']
        
        
    def algo(self, values, all_data):
        print 'Nothing', values['time'], values['be']
        
        if values['time'] - self.start_time > self.duration:
			return 'switch'
        
        
