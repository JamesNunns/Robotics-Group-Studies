class Cm():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.005)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.duration = kwargs.get('duration', float('inf'))


    def algo(self,values,all_data):
        print values['time'], values['be'] , values['av']
        if values['time'] - self.start_time < self.duration:
            
            if values['be'] <= 0 and values['av'] >= 0:
                return 'low_cm'
            elif values['be'] >= 0 and values['av'] <= 0:
                return 'low_cm'
            elif values['be'] >= 0 and values['av'] >= 0:
                return 'high_cm'
            elif values['be'] <= 0 and values['av'] <= 0:
                return 'high_cm'
        
        else:
            return 'switch'
