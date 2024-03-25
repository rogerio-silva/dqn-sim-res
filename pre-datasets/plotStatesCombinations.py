# Description: This script plots the number of states for 100 possible positions and 1 to 5 drones.

import math
import matplotlib.pyplot as plt

p = 100
drones = list(range(1, 6))
states = [math.factorial(p) / (math.factorial(d) * math.factorial(p - d)) for d in drones]

plt.plot(drones, states, 'ro-')
plt.xlabel('Number of drones')
plt.ylabel('Number of states')
plt.title('Number of states for 100 possible positions')

# Save the plot in a file
plt.savefig('plots/states.png')

