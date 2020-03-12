from sys import path
path.insert(0, "../Utility")
import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero
from utility_functions_new import last_key_point_angle


class Maintain():

	def __init__(self, values, all_data, **kwargs):
		
		self.start_be = values['be']
		self.duration = kwargs.get('duration', float('inf'))
		self.start_time = values['time']
		self.angle_maintain = last_key_point_angle('max',all_data)
		


	def algo(self,values,all_data):
		print 'Maintain' , values['be'] 
		
		if values['time'] - self.start_time < self.duration:
			self.last_angle = last_key_point_angle('max',all_data)
			if self.last_angle < self.angle_maintain:
				
				if values['be'] < 0:
					return 'crunched'
				elif values['be'] > 0:
					return 'extended'
				else:
					return 'current'
			
		else:
			return 'switch'
