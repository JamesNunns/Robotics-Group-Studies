import sys
import time

class Machine_Learning_bool:

    def __init__(self,values,all_data,**kwargs):

        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.duration = kwargs.get('duration', float('inf'))
        self.previous_vel = values['av']
        sys.path.insert(0, "../../Machine_Learning")
        from ml import ML
        self.ml = ML("../../Machine_Learning/ MACHINE_LEARNING_FILE ")


    def algo(sefl,values,all_data):
        time.sleep(0.01)
        if values['time'] - self.start_time < self.duration:
            torso_bool, legs_bool = values['t_move'], values['l_move']
            action = self.ml.get_action([ values['be'], values['av'], torso_bool, legs_bool ])
            print values['time'], values['be'], values['av'], action

            if (action == 0 and not legs_bool):
                return ["legs_extended", 0.8]
            elif (action == 1 and not legs_bool):
                return ["legs_retracted", 0.8]
            elif (action = 2 and not torso_bool):
                return ["torso_retracted"]
            elif (action == 3 and not torso_bool):
                return ["torso_extended"]
            elif action == 4:
                pass

        else:
            return 'switch'
        # 0.0174533 "one degree in radians"
