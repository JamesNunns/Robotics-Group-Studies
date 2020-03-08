import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero

class Maintain():
    """ Last Years code will have to 
    produce a new version """
    def __init__(self, values, all_data, **kwargs):
        self.period = kwargs.get('period', 0.005)
        # offset is time from maximum to swing
        self.time_switch_ext = float('inf')
        self.time_switch_sea = float('inf')

        self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)

        # setting up times
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.maintain_angle = kwargs.get('maintain_angle', 10.0)

        # alternative switch condition
        self.duration = kwargs.get('duration', float('inf'))

        self.offsets = {
            'good': -0.25,
            'poor': 0.1,
            'standard': -0.1
        }

    def algo():

        if sign_zero(values['be']) != sign_zero(self.previous_be) and values['be'] < 0:
            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time, self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='both', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # do two standard, poor, or good kicks, dependent on how far from maintain amplitude it is
            if -0.1 <= abs(self.last_maximum) - abs(self.maintain_angle) <= 0.1:
            self.offset = self.offsets['standard']
            elif abs(self.last_maximum) - abs(self.maintain_angle) > 0.1:
            self.offset = self.offsets['poor']
            elif abs(self.last_maximum) - abs(self.maintain_angle) < -0.1:
            self.offset = self.offsets['good']
            else:
            print 'Offset condition not found\nLast maximum: {}, Maintain angle: {}, \
                Difference between{}'.format(self.last_maximum, self.maintain_angle, abs(self.last_maximum) - abs(self.maintain_angle))

        # set time for position to switch
        self.time_switch_sea = self.min_time + self.quart_period + self.offset
        self.time_switch_ext = self.time_switch_sea + 2 * self.quart_period
        print 'Current time: {:.3f}'.format(values['time']), \
        'Last maximum: {:.3f} degrees'.format(self.last_maximum)
        # 'Next seated switching time: {:.3f}'.format(self.time_switch_sea), \
        # 'Next extended switching time: {:.3f}'.format(self.time_switch_ext), \


        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']

        # position changes, move slower to hopefully control amplitude better
        if values['time'] >= self.time_switch_sea:
            self.time_switch_sea = float('inf')
            return ['crunched', 1.0]
        if values['time'] >= self.time_switch_ext:
            self.time_switch_ext = float('inf')
            return ['extended', 1.0]

        # duration over
        if values['time'] - self.start_time > self.duration:
            print 'Switching from maintaining, duration ended'
            return 'switch'