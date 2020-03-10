from scipy.signal import find_peaks
import numpy as np

def last_key_point(what, all_data):
    
    times = np.array(all_data["time"])
    encoder_values = np.array(all_data["be"])
    lt = times[-10:]
    t = []
    for i in xrange(len(lt)-1):
        t.append(lt[i+1]-lt[i])
    ts = sum(t)/len(t)
    distance = int(1.5/(ts))
    if what == "max":
        peaks = find_peaks(encoder_values, distance=distance)[0]
        last_peak = peaks[-1]
        return times[last_peak]
    if what == "min":
        peaks = find_peaks(-encoder_values, distance=distance)[0]
        last_peak = peaks[-1]
        return times[last_peak]
    
    if what == "zero":
        ev = encoder_values[-int(3/ts):]
        tv = times[-int(3/ts):]
        min_time = []
        for i in xrange(len(ev)-1):
            if np.sign(ev[i+1]) != np.sign(ev[i]):
                dt = abs(tv[i] - tv[i+1])
                interpolate = dt * np.abs(ev[i]) / \
                    abs(ev[i] - ev[i+1])
                min_time.append(tv[i] - interpolate)
        return min_time[-1]
    
def next_points(values, last_key_points):
    l = last_key_points
    if values['time'] - l[1] < values['time'] - l[2] and values['time'] - l[0]:
        quarter_period = abs(l[1] - l[2])
        next_max = l[1] + 2*quarter_period
        next_min = l[1] + 4*quarter_period
    if values['time'] - l[2] < values['time'] - l[1] and values['time'] - l[0]:
        if values['time'] - l[1] < values['time'] - l[0]: 
            quarter_period = abs(l[2] - l[1])
            next_max = l[2] + quarter_period
            next_min = l[2] + 3*quarter_period
        if values['time'] - l[0] < values['time'] - l[1]: 
            quarter_period = abs(l[2] - l[0])
            next_max = l[2] + 3*quarter_period
            next_min = l[2] + quarter_period
    if values['time'] - l[0] < values['time'] - l[1] and values['time'] - l[2]:
        quarter_period = abs(l[0] - l[2])
        next_max = l[0] + 4*quarter_period
        next_min = l[0] + 2*quarter_period
        
    return next_max, next_min
    
