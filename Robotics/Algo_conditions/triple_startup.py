class Triple():

    def __init__(self, values, all_data, **kwargs):

        self.start_time = values['time']
        self.duration = kwargs.get('duration',10)
        self.wait = 1.253 
        self.last_move = 0
        self.first_kick = True

    def algo(self,values,all_data):
        print 'Start Algo' , values['time']

        t = values['time']

        if t < 0.1:
            self.last_move = t
            return ['extended', 0.6]

        if t > 0.1:
			if t > self.last_move + self.wait/2 and self.first_kick == True:
				# first kick needed after a quarter period, not half
				self.first_kick = False  # go to half period kicks
				self.last_move = t       # reset time of last kick
				if values['pos'] == 'seated':
					return 'extended'
				else:
					return 'seated'
			if t > self.last_move + self.wait:
				self.last_move = t
				if values['pos'] == 'extended':
					return ['crunched', 0.8]
				else:
					return ['extended', 0.8]

        if t -self.start_time > self.duration:
            print 'switch' , t
            return 'switch'


     
