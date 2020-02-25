class Acc_testXZ():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.005)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.previous_accX = values['ACX']
        self.previous_accX

        self.duration = kwargs.get('duration', float('inf'))


    def algo(self, values, all_data):
        print values['time'], values['be'], values['ACX']
        if values['time'] < self.duration:
            acc_dx = values['ACX'] - self.previous_accX
            acc_dz = values['ACZ'] - self.previous_accZ
            self.previous_accX, self.previous_accZ = values['ACX'], values['ACZ']
            if acc_dx < 0 and values['ACX'] > 2 and acc_dz < 0:
                return 'crunched'
            elif acc_dx < 0 and values['ACX'] < 0 and acc_dz < 0:
                return 'extended'
            else:
                if values['pos'] == 'crunched':
                    return 'crunched'
                elif values['pos'] == 'extended':
                    return 'extended'
