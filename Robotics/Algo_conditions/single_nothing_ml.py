import time as tme
import numpy as np
from sys import path
path.insert(0, "../Utility")
from utility_functions import sign_zero

class Nothing_ML():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_be = values['be']
        self.n = 0
        
    def algo(self, values, all_data):
        print 'Nothing', values['time'], values['be']
        
        if self.duration - (values['time'] - self.start_time) < 2 and values['time'] - self.start_time < self.duration:
			
			if self.n == 0:
				self.n += 1
				return "extended"
			else:
				tme.sleep(0.5)
				return "crunched"
				
			
		
        
        if values['time'] - self.start_time > self.duration:
			return 'switch'
        
        
