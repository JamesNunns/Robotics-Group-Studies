from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero
import numpy as np

class TripleIncrease():

    def __init__(self, values, all_data, **kwargs):

        self.start_time = values['time']
        self.previous_time = values['time']
        self.switch_time = 100
        self.offet = -0.21
        self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_be =  values['be']


    def algo(self,values,all_data):

        if sign_zero(vales['be']) != sign_zero(self.previous_be):
            
            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time, self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='both', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)
            # set time for position to switch
            self.switch_time = self.min_time + self.quart_period + self.offset

        self.previous_be = values['be']
        self.previous_time = values['time']

        if values['time'] > self.switch_time:
            self.switch_time += 100
            if values['be'] < 0:
                return 'crunched'
            elif values['be'] > 0:
                return 'extended'
        
        if values['time'] - self.start_time > self.duration:
            print 'Switch' , values['time']
            return 'switch'
        


