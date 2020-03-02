class Machine_Learning():
    
    def __init__(self,values,all_data,**kwargs):
        
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_vel = values['av']
        import ML
        self.ml = ML()

    def algo(self,values,all_data):
        print values['time'], values['be']
        if values['time'] - self.start_time < self.duration:
            action = self.ml.get_action([ values['be'], values['av'] ])
            if action == 0:
                return "legs_out"
            elif action == 1:
                return "legs_in"
            elif action == 2:
                return "torso_out"
            elif action == 3:
                return "torso_in"
            elif action == 4:
                pass


           # 0.0174533 "one degree in radians"
