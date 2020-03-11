class Test_swapped():

    def __init__(self,values,all_data,**kwargs):
        self.period = kwargs.get('period', 0.005)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.duration = kwargs.get('duration', float('inf'))

    
    def algo(self,values,all_data):
        
        #if values['time'] > 30:#self.duration:
        print values['time'], values['be']
        if values['be'] < 0:
            return 'extended'
        elif values['be'] > 0:
            return 'crunched'
