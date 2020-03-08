class Triple():

    def __init__(self,value,all_data,**kwargs):

        self.start_time = values['time']
        self.duration = kwargs.get('duration',10)
        self.wait = 1.8
        self.last_move = 0

    def algo(self,values,all_data):
        print 'Start Algo' , values['time']

        t = values['time']

        if t < 0.1:
            self.last_move = t
            return ['extended', 0.6]

        if t > 0.1:

            if t > self.last_move + self.wait:
                self.last_move = t
                if values['pos'] == 'extended':
                    return ['crunched', 0.6]
                else:
                    return ['extended', 0.6]

        if t -self.start_time > self.duration:
            print 'switch' , t
            return 'switch'


     