'''Start-up algorithm that simply kicks, waits a half period,
    and kicks again.'''
    
import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero

class SmallAngleDamping ():
    def __init__(self, values, all_data, **kwargs):
        print 'Startup script'
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.setting_posture = 'seated' 
        self.duration = kwargs.get('duration', float('inf'))
        self.max_angle = kwargs.get('max_angle', 5)
        #self.wait_time = 1.2735   # defined by the half period of a swing
        self.last_move = 0      # time last kick was performed
        self.first_kick = True  # used to check if it is first kick

    def algo(self, values, all_data):
        # At the end of the loop, set the value of big encoder to the previous value
        print 'SmallAngleDamping', values['time'], values['be']
        if self.setting_posture == 'seated':
            return 'seated'
        else:
            return 'extended'
    

