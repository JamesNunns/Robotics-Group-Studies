from sys import path
path.insert(0, "../")
from acc_predictor import acc_predict

class Acc():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.01)
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))

    def algo(self,values,all_data):
        print values['time'], values['be'], values['ax'], values['az']
        if values['time'] - self.start_time < self.duration:
            offset = 0.25
            p = acc_predict(values)
            for i in p[0]:
                if abs(values['time'] - i) < offset:
                    return 'extended'
            for i in p[1]:
                if abs(values['time'] - i) < offset:
                    return 'crunched'
		else:
			return 'switch'
        
