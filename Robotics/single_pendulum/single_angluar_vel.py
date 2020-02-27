class Velocity():

    def __init__(self,values,all_data,**kwargs):

		self.period = kwargs.get('period', 0.005)

		self.start_time = values['time']
		self.previous_time = values['time']
		self.previous_be = values['be']

		self.duration = kwargs.get('duration', float('inf'))

		self.previous_vel = values['av']

    def algo(self,values,all_data):
		print values['time'], values['be']
		if values['time'] - self.start_time < self.duration:
			if values['av'] < 0:
				return 'crunched'
			elif values['av'] > 0:
				return 'extended'
		else:
			return 'switch'
