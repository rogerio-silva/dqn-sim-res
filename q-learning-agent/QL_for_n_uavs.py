import argparse
import itertools
import random
from itertools import combinations

import numpy as np
from ns3gym import ns3env

"""
Created on Sun Apr 1 15:00:00 2023
Modified on Sun Apr 1 15:00:00 2023
Authors: Rogério S. Silva, Renan R. Oliveira, and Lucas, and Xavier Sebastião, and Cleyber
Email: {rogerio.sousa, renan.oliveira}@ifg.edu.br, 
"""

__author__ = ("Rogério S. Silva, Renan R. Oliveira, Lucas Tadeu, Xavier Sebastião, "
              "Cleyber Bezerra, Antonio Oliveira-JR, and Kleber V. Cardoso")
__copyright__ = ("Copyright (c) 2024, "
                 "Instituto de Informática - Universidade Federal de Goiás - UFG, and"
                 "Instituto Federal de Goiás - IFG")
__version__ = "0.1.0"
__email__ = ("{rogerio.sousa, renan.oliveira}@ifg.edu.br, lucastsc@gmail.com"
             "{cleyber.bezerra, xavierpaulino, antonio, kleber}@inf.ufg.br")


class Map:
    def __init__(self,
                 dim_grid=10,  # means the grid is 10x10
                 actions_per_agent=5,  # each agent is capable of up,right,down,left and stopped movements
                 agents=2,  # total number of agents (UAVs) in the grid
                 state=0,  # initial state, starts at state 0 (means there is a first position for all agents)
                 alpha=0.2,  # Q-learning algorithm learning rate
                 gamma=0.9,
                 # gamma is the discount factor. It is multiplied by the estimation of the optimal future value.
                 epsilon=1,
                 # epsilon handles the exploration/exploitation trade-off (e.g. epsilon < 0.4 means 40% exploration and 60% exploitation)
                 epsilon_min=0.5,
                 # minimum allowed epsilon. Epsilon will change (reduce) with decay_epsilon function. At begginings, it means more exploration than exploitation.
                 epsilon_decay=0.999
                 # epsilon will decay at each step. For 1000 steps and decay 0.999, for example, epsilon will decay a factor by 0.367 of it initial value.
                 ):
        self.dim_grid = dim_grid
        self.actions_per_agent = actions_per_agent
        self.agents = agents
        self.state = state
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_max = epsilon
        self.epsilon_decay = epsilon_decay
        self.initQTable()

    def initQTable(self):
        # for a grid 10x10 and 2 agents, for example, total stated are C(10x10,2) = 4950 states
        # for 2 agents with 5 movements each, we have 5^2 = 25 possible actions
        self.states = len(list(combinations([i for i in range(self.dim_grid * self.dim_grid)], self.agents)))

        self.qtable = np.zeros(
            (self.states, self.actions_per_agent ** self.agents))  # for grid 10 and 2 agents -> Q(4950,25)

    # gives the next state given the current state for a given action
    def next_state(self, current_state, action):
        return d.loc[current_state, action][0]

    # gives the current qos for a current state
    def current_qos(self, current_state):
        return d.loc[current_state, 'qos']

    # gives the qos of the next state, given the current state and a given action
    def next_qos(self, current_state, action):
        return d.loc[current_state, action][1]

    # epsilon will return to it's initial value for each episode
    def resetEpsilon(self):
        self.epsilon = self.epsilon_max

    # attribute a new value to epsilon after a decay
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    # if current qos is less than the next qos, we have a reward. Otherwise, we have a penalty.
    def reward(self, current_state, action):
        if self.current_qos(current_state) < self.next_qos(current_state, action):
            # rwd = 1
            rwd = self.next_qos(current_state, action)
        else:
            # rwd = -1
            rwd = self.current_qos(current_state)
        return rwd

    # given a state, we search over all possible actions that gives the maximum of qtable[state]. Returns the maximum q-value.
    def getMaxQ(self, state):
        return max(self.qtable[state])

    # returns a random choice over all possible actions (0,1,2,...,24) for 2 agents and 5 possible movements, for example.
    def randomAction(self):
        actions = [i for i in range(self.actions_per_agent ** self.agents)]
        return random.choice(actions)

    # given the qtable, gets the action that better results in the biggest q-value.
    def bestAction(self, state):
        movement = np.argmax(self.qtable[state])
        return movement

    # given a state, times it'll be a random action, times it'll be the best action. It depends on epsilon value.
    def getAction(self, state):
        self.decay_epsilon()
        if random.random() < self.epsilon:
            return self.randomAction()
        else:
            return self.bestAction(state)

    # given a state and a given action, it updates the qtable and returns the new state and the reward for the given movement in that state.
    def update(self, state, action):
        newstate = self.next_state(state, action)
        reward = self.reward(state, action)
        self.qtable[state][action] = (1 - self.alpha) * self.qtable[state][action] + self.alpha * (
                reward + self.gamma * self.getMaxQ(newstate))
        return newstate, reward

    def find_target_state_qos(self, iq, ia):
        target_state = 0
        actual_state = states[iq]
        target_position = [-1 for _ in range(self.agents)]
        actual_positions = positions[iq]
        acts = actions[ia]

        for ai, ac in enumerate(acts):
            if ac == 'Up':
                if actual_positions[ai] + self.dim_grid >= self.dim_grid * self.dim_grid:
                    target_state = -1
                    break
                target_position[ai] = actual_positions[ai] + self.dim_grid
            elif ac == 'Down':
                if actual_positions[ai] - self.dim_grid < 0:
                    target_state = -1
                    break
                target_position[ai] = actual_positions[ai] - self.dim_grid
            elif ac == 'Left':
                if actual_positions[ai] % self.dim_grid == 0:
                    target_state = -1
                    break
                target_position[ai] = actual_positions[ai] - 1
            elif ac == 'Right':
                if actual_positions[ai] % self.dim_grid == self.dim_grid - 1:
                    target_state = -1
                    break
                target_position[ai] = actual_positions[ai] + 1
            else:  # stopped
                target_position[ai] = actual_positions[ai]

        # Invalid movement
        if target_state == -1:
            return [iq, -1]

        # Collisions
        target_position = tuple(sorted(target_position))
        if len(set(target_position)) < self.agents:
            return [iq, -2]

        target_state = states[positions.index(tuple(target_position))]
        qos_target_state = self.next_qos(target_state, ia)
        ret = [target_state, qos_target_state]
        return ret


# Create a parser
parser = argparse.ArgumentParser(description='QL for n UAVs')
# Add arguments to the parser
parser.add_argument('--dim_grid', type=int, help='Grid dimension (dim_grid x dim_grid)')
parser.add_argument('--seed', type=int, help='Seed for random number generator')
parser.add_argument('--ndevices', type=int, help='Number of Devices')
parser.add_argument('--ngateways', type=int, help='Number of Gateways')
# Parse the arguments
args = parser.parse_args()

# ns-3 environment
port = 5555
seed = args.seed
nDevices = args.ndevices
nGateways = args.ngateways
simTime = 600  # seconds
stepTime = 600  # seconds
simArgs = {"--nDevices": nDevices,
           "--nGateways": nGateways}
startSim = 1
debug = 0
dim_grid = args.dim_grid
movements = ['up', 'right', 'down', 'left', 'stay']
actions_per_agent = len(movements)
actions = list(itertools.product(movements, repeat=nGateways))

# Q-learning settings
episodes = 300
steps = 1000
improvements = []
rewards = [0]
k = 0


# ToDo: Change Map to ns-3 environment
m = Map(dim_grid=dim_grid,
        agents=nGateways,
        actions_per_agent=actions_per_agent,
        state=0,
        epsilon=1,
        epsilon_min=0.1,
        epsilon_decay=0.999,
        alpha=0.2,
        gamma=0.9)

env = ns3env.Ns3Env(port=port, startSim=startSim, simSeed=seed, simArgs=simArgs, debug=debug)
ob_space = env.observation_space
ac_space = env.action_space
print("Observation space: ", ob_space, ob_space.dtype)
print("Action space: ", ac_space, ac_space.dtype)

for ep in range(episodes):
    state = env.reset()
    obs, reward, done, info = env.get_state()
    start_qos_episode = reward
    print(f'Qos start state (episode {ep}): {start_qos_episode}')
    m.resetEpsilon()
    for step in range(steps):
        action = m.getAction(state)
        newstate, reward = m.update(state, action)
        state = newstate

        mean_reward = ((k + 1) * rewards[-1] + reward) / (k + 2)
        k = k + 1
    final_qos_episode = m.current_qos(state)
    print(f'Qos final state (episode {ep}): {final_qos_episode}')
    if final_qos_episode > start_qos_episode:
        print(True)
        improvements.append(1)
    else:
        print(False)
        improvements.append(0)

    print('---------' * 5)

    # Média móvel da recompensa no término de cada episodio
    rewards.append(mean_reward)
    #     clear_output(wait=True)
    print(f"episode: {ep:0{5}}/{episodes} - R: {mean_reward:.{8}f}")
print(
    f'For {episodes} episodes, there was {sum(improvements)} improvements ({round(sum(improvements) * 100 / episodes, 2)}%) and {episodes - sum(improvements)} worse results ({round((episodes - sum(improvements)) * 100 / episodes, 2)}%)')
