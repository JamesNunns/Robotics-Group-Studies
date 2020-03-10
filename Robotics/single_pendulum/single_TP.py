from utility_functions_new import last_key_point

class TP_Predict():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.005)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.duration = kwargs.get('duration', float('inf'))


    def algo(self,values,all_data):
        offset = 0.1
        print values['time'], values['be'], len(all_data)
        if values['time'] - self.start_time < self.duration:
            l = [last_key_point("max", all_data), last_key_point("min", all_data), last_key_point("zero", all_data)]
            if values['time'] - l[1] < values['time'] - l[2] and values['time'] - l[0]:
                quarter_period = abs(l[1] - l[2])
                next_max = l[1] + 2*quarter_period
                next_min = l[1] + 4*quarter_period
            if values['time'] - l[2] < values['time'] - l[1] and values['time'] - l[0]:
                if values['time'] - l[1] < values['time'] - l[0]: 
                    quarter_period = abs(l[2] - l[1])
                    next_max = l[2] + quarter_period
                    next_min = l[2] + 3*quarter_period
                if values['time'] - l[0] < values['time'] - l[1]: 
                    quarter_period = abs(l[2] - l[0])
                    next_max = l[2] + 3*quarter_period
                    next_min = l[2] + quarter_period
            if values['time'] - l[0] < values['time'] - l[1] and values['time'] - l[2]:
                quarter_period = abs(l[0] - l[2])
                next_max = l[0] + 4*quarter_period
                next_min = l[0] + 2*quarter_period
            print next_max, next_min   
            if next_max - values['time'] < offset:
                if next_max - values['time'] > 0:
                    return "extended"
            if next_min - values['time'] < offset:
                if next_min - values['time'] > 0:
                    return "crunched"
            
            
        else:
            return 'switch'


