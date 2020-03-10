from sys import path
path.insert(0, "../")
from acc_predictor import acc_predict
from utility_functions_new import last_key_point, next_points

class Acc():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.01)
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.offset = 0.25

    def algo(self,values,all_data):
        print values['time'], values['be'], values['ax'], values['az']
        if values['time'] - self.start_time < self.duration:
            p = acc_predict(all_data)
            l = [last_key_point("max", p), last_key_point("min", p), last_key_point("zero", p)]
            next_max, next_min = next_points(values, l)
            if next_max - values['time'] < self.offset:
                if next_max - values['time'] > 0:
                    return "extended"
            if next_min - values['time'] < self.offset:
                if next_min - values['time'] > 0:
                    return "crunched"
        else:
            print "done"
            return 'switch'
        
