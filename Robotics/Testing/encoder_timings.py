from sys import path
path.insert(0, "../Interface")
import time
import numpy as np
import pandas as pd
from encoder_interface import Encoders

Encoders = Encoders(BigEncoder, SmallEncoders, small_encoders_required=True)

print "move the swing slowly"
small_accuracy_values = []
big_accuracy_values = []
for i in range(100):
    small_accuracy_values.append(Encoders.get_small_encoders())
print "small done, big starting"
for i in range(5):
    time.sleep(1)
    print 6-i
for i in range(100):
    big_accuracy_values.append(Encoders.get_big_encoder)

angle_accuracy_df = pd.DataFrame({'small_encoders':small_accuracy_values, 'big_encoders':big_accuracy_values})
angle_accuracy_df.to_csv("encoder_angles_accuracy")


calls = np.linspace(0, 1000, 10)

small_times = []
start_time_small = time.time()
for i in range(10):
    for j in range(100):
        Encoders.get_small_encoders()
    small_times.append(time.time()-start_time_small)

big_times = []
start_time_big = time.time()
for i in range(10):
    for j in range(100):
        Encoders.get_big_encoder()
    big_times.append(time.time()-start_time_big)

readout_timings_df = pd.DataFrame({'calls':calls, 'small_times':small_times, 'big_times':big_times})
readout_timings_df.to_csv("encoder_readout_timings")
