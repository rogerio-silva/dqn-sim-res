# Criar um gráfico para mostrar as combinações de 100 posições para de 1 a 10 drones
import math
import matplotlib.pyplot as plt

p = 100
drones = list(range(1, 6))
states = [math.factorial(p) / (math.factorial(d) * math.factorial(p - d)) for d in drones]

plt.plot(drones, states, 'ro-')
plt.xlabel('Number of drones')
plt.ylabel('Number of states')
plt.title('Number of states for 100 possible positions')

plt.show()
