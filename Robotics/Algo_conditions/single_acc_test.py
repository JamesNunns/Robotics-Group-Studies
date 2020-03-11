class Acc_testXZ():

	def __init__(self,values,all_data,**kwargs):
		self.period = kwargs.get('period', 0.005)

		self.start_time = values['time']
		self.previous_time = values['time']
		self.previous_be = values['be']

		self.previous_accX = values['ax']
		self.previous_accZ = values['az']

		self.duration = kwargs.get('duration', float('inf'))


	def algo(self, values, all_data):
		print values['time'], values['be'], values['ax'], values['az']
		if values['time'] - self.start_time < self.duration:
			acc_dx = values['ax'] - self.previous_accX
			acc_dz = values['az'] - self.previous_accZ
			self.previous_accX, self.previous_accZ = values['ax'], values['az']
			if acc_dx < 0 and values['ax'] > 0 and acc_dz < 0:
				return 'crunched'
			elif acc_dx < 0 and values['ax'] < 0 and acc_dz < 0:
				return 'extended'
			else:
				return values['position']
		else:
			return 'switch'
