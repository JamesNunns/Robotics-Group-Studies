import matplotlib.pyplot as plt
import numpy as np

def shade_background_based_on_algorithm(time, algorithm, plot=True):
    """
    Shades axis darker and darker grey whenever algorithm changes
    ax: singular matplotlib axis to be shaded
    time: list of recorded times
    algorithm: list of corresponding algorithm at each 
    """
    # where algorithm changes and difference in indexes between current and next algorithm
    algorithm_change_indexes = np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))
    algorithm_change_diff = np.diff(algorithm_change_indexes)

    if plot:
        # for each change in algorithm shade background slightly darker
        for i, index in enumerate(algorithm_change_indexes[:-1]):
            plt.axvspan(time[index], time[index + algorithm_change_diff[i]], alpha = (i+1) * 0.10, color='grey', label='{}'.format(algorithm[index+1]))
    return algorithm_change_indexes