import sys
import time
class Machine_Learning():
    
    def __init__(self,values,all_data,**kwargs):
        
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_vel = values['av']
        sys.path.insert(0, "../")
        from ml import ML
        self.ml = ML()

    def algo(self,values,all_data):
        time.sleep(0.01)
        if values['time'] - self.start_time < self.duration:
            action = self.ml.get_action([ values['be'], values['av'] ])
            print values['time'], values['be'], values['av'], action
            if action == 1:
                return ["legs_retracted", 1.0]
            elif action == 0:
                return ["legs_extended", 1.0]
            elif action == 3:
                return "torso_extended"
            elif action == 2:
                return "torso_retracted"
            elif action == 4:
				pass
        else:
            return 'switch'
           # 0.0174533 "one degree in radians"
