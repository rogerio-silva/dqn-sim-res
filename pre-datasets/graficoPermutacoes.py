# Criar um gráfico para mostrar as permutações das ações
# "UP", "DOWN", "LEFT", "RIGHT" e "STOPPED" para de 1 a 10 drones

import itertools
import math
import matplotlib.pyplot as plt

acoes = ["UP", "DOWN", "LEFT", "RIGHT", "STOPPED"]
p = len(acoes)
drones = list(range(1, 7))
actions = [p ** d for d in drones]

plt.plot(drones, actions, 'ro-')
plt.xlabel('Number of drones')
plt.ylabel('Number of actions')
plt.title('Number of actions for a set of 5 possible movements')

plt.show()

