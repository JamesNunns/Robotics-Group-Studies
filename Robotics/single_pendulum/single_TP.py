from utility_functions_new import last_key_point, next_points_qp, next_points_hp


class TP_Predict():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.01)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.offset = 0.21
        self.duration = kwargs.get('duration', float('inf'))


    def algo(self,values,all_data):
        print values['time'], values['be']
        if values['time'] - self.start_time < self.duration:
            l = [last_key_point("max", all_data), last_key_point("min", all_data), last_key_point("zero", all_data)]
            print(l)
            next_max, next_min = next_points_hp(values, l)
            if next_max - values['time'] < self.offset:
                if next_max - values['time'] > 0:
                    return "extended"
            if next_min - values['time'] < self.offset:
                if next_min - values['time'] > 0:
                    return "crunched"
            if values['time'] - l[0] < self.offset:
                if l[0] - values['time'] < 0:
                    return "extended"
            if values['time'] - l[1] < self.offset:
                if l[1] - values['time'] < 0:
                    return "crunched"
            
        else:
            return 'switch'


