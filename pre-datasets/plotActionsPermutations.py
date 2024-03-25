# Create the plot for the number of actions for a set of 5 possible movements
# "UP", "DOWN", "LEFT", "RIGHT" e "STOPPED" for 1 to 6 drones

import itertools
import math
import matplotlib.pyplot as plt

actions = ["UP", "DOWN", "LEFT", "RIGHT", "STOPPED"]
p = len(actions)
drones = list(range(1, 7))
n_actions = [p ** d for d in drones]

plt.plot(drones, n_actions, 'ro-')
plt.xlabel('Number of drones')
plt.ylabel('Number of actions')
plt.title('Number of actions for a set of 5 possible movements')

plt.savefig('plots/actions.png')

