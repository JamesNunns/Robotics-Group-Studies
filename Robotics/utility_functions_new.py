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
    
    
    
