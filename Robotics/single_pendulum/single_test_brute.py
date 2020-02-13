class Test():

    def __init__(self,values,all_data,**kwags):
        self.period = kwargs.get('period', 0.005)

        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        self.duration = kwargs.get('duration', float('inf'))

    
    def algo(self,values,all_data):
        
        if values['time'] > self.duration:
            
            if values['be'] < 0:
                return 'crunched'
            elif values['be'] > 0:
                return 'extended'
