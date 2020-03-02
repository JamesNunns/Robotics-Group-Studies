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

    def move_torso(self, angle=1, percent_max_speed=0.4):
        torso = {'RHP': 1.0, 'LHP': 1.0, 'RSP': 0.480417754569, 'LSP': 0.0496083550914, 'RSR': 1.12532637076, 'LSR': -1.10966057441, 'RER': -2.13838120104, 'LER': 2.18263145891, 'REY': -0.258485639687, 'LEY': 0.853785900783, 'RWY': 0.167101827676, 'LWY': -0.180156657963}
        for joint in torso:
        	Robot.move_limbs(joint, angle*torso[joint]*0.0174533, percent_max_speed)

    def move_legs(self, angle=1, percent_max_speed=0.4):
        legs = ['RKP', 'LKP']
        for joint in legs:
            Robot.move_limbs(joint, angle*0.0174533, percent_max_speed)


    def algo(self,values,all_data):
        print values['time'], values['be']
        if values['time'] - self.start_time < self.duration:
            action = self.ml.get_action([ values['be'], values['av'] ])
            if action == 0:
                "legs out -"
                self.move_legs(-1)
            elif action == 1:
                "legs in +"
                self.move_legs(1)
            elif action == 2:
                "torso out +"
                self.move_torso(1)
            elif action == 3:
                "torso in -"
                self.move_torso(-1)
            elif action == 4:
                pass


           # 0.0174533 "one degree in radians"
