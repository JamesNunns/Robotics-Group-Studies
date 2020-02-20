'''Start-up algorithm that simply kicks, waits a half period,
    and kicks again.'''
    
from utility_functions import last_maxima


class Start():
    def __init__(self, values, all_data, **kwargs):
        print 'Startup script'
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.max_angle = kwargs.get('max_angle', 5)
        self.wait_time = 1.253   # defined by the half period of a swing
        self.last_move = 0      # time last kick was performed
        self.first_kick = True  # used to check if it is first kick

    def algo(self, values, all_data):
        t = values['time'] - self.start_time  # renames current time to t
        print 'Time: {:.2f}'.format(values['time']), 'Big encoder: {:.2f}'.format(values['be'])

        if t < 0.1:
            # sets the first kick from standstill.
            self.last_move = t  # resets time of last kick
            return 'extended'   # kicks

        if t > 0.1:
            if t > self.last_move + self.wait_time/2 and self.first_kick == True:
                # first kick needed after a quarter period, not half
                self.first_kick = False  # go to half period kicks
                self.last_move = t       # reset time of last kick
                if values['pos'] == 'seated':
                    return 'extended'
                else:
                    return 'seated'

            if t > self.last_move + self.wait_time:
                # kicks after first kick use quarter period
                self.last_move = t  # reset time of last kick
                if values['pos'] == 'extended':
                    return 'seated'
                else:
                    return 'extended'

        if 0.15 < t - self.last_move < 0.5:
            if t > self.duration:
                print 'last move', self.last_move
                print 'Switch on duration'
                return 'switch'
            if t > 10:
                if last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period) > self.max_angle:
                    print 'last move', self.last_move
                    print 'Switched on max angle'
                    return 'switch'
