import matplotlib.pyplot as plt
import numpy as np

f = open('NEAT/Data.txt', 'r')
neat = f.readlines()
f.close()

neat_t = eval(neat[0])
neat_p = eval(neat[1])
neat_a = eval(neat[2])

neat_p_mean = [np.mean(i) for i in neat_p]
neat_p_max = [np.max(i) for i in neat_p]
neat_p_min = [np.min(i) for i in neat_p]

neat_a_mean = [np.mean(i) for i in neat_a]
neat_a_max = [np.max(i) for i in neat_a]
neat_a_min = [np.min(i) for i in neat_a]

print(neat_p_mean)
print(neat_p_min)
print(neat_p_max)

plt.errorbar(neat_t, neat_p_mean, yerr=[np.array(neat_p_min) + np.array(neat_p_mean), np.array(neat_p_max) + np.array(neat_p_mean)], label='Performance')
plt.legend(loc='upper left')
plt.margins(0, 0)
plt.title("Performance of NEAT")
plt.xlabel("Genome")
plt.ylabel("Performance")
plt.show()