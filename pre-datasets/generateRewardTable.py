import pandas as pd
import itertools
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("matrix_size")
parser.add_argument("drones")
parser.add_argument("path")

args = parser.parse_args()
cwd = os.getcwd()
resFolder = "{}/".format(cwd) + args.path

matrix_size = int(args.matrix_size)
n_drones = int(args.drones)

# Generate all possible positions for the drones
positions = list(itertools.combinations_with_replacement(range(matrix_size * matrix_size), n_drones))
positions = [position for position in positions if len(set(position)) == n_drones]
states = [i for i, pos in enumerate(positions)]
movements = ['Up', 'Right', 'Down', 'Left', 'Stopped']
actions = list(itertools.product(movements, repeat=n_drones))


# Function to find the QoS value for a given action
def find_newstate_qos(qos, iq, ia, actions, qosDF):
    qosValue = 0
    xy_positions = [(pos // matrix_size, pos % matrix_size) for pos in positions[iq]]
    xy_temp_positions = xy_positions.copy()
    for ind, pos in enumerate(xy_positions):
        if actions[xy_positions.index(pos)] == 'Up':
            if pos[0] + 1 >= matrix_size:
                qosValue = -1
                break
            pos = (pos[0] + 1, pos[1])
        elif actions[xy_positions.index(pos)] == 'Down':
            if pos[0] - 1 < 0:
                qosValue = -1
                break
            pos = (pos[0] - 1, pos[1])
        elif actions[xy_positions.index(pos)] == 'Left':
            if pos[1] - 1 < 0:
                qosValue = -1
                break
            pos = (pos[0], pos[1] - 1)
        elif actions[xy_positions.index(pos)] == 'Right':
            if pos[1] + 1 >= matrix_size:
                qosValue = -1
                break
            pos = (pos[0], pos[1] + 1)
        else:  # stopped
            pass
        xy_temp_positions[ind] = pos

    if qosValue == -1:
        ret = iq, -1
    else:
        # Compute the new position index
        new_position = tuple([pos[0] * matrix_size + pos[1] for pos in xy_temp_positions])
        # Sort tuple to find the new state
        new_position = tuple(sorted(new_position))
        # Discard collisions with penalty
        if len(set(new_position)) < n_drones:
            ret = iq, -2
        else:
            # Get the new state
            new_state = positions.index(new_position)
            # Set new state and QoS value from the dataframe
            ret = new_state, qosDF.at[new_state, 'qos']
    return ret


# Read the QoS values from the file to a dataframe
qosDF = pd.read_csv(f"{resFolder}/qos_{n_drones}.dat", sep=" ", index_col="state")
# Add new actions columns to the dataframe
for ia, action in enumerate(actions):
    qosDF[ia] = [[0, 0] for _ in range(len(states))]

for iq, qos in qosDF.iterrows():
    for ia, action in enumerate(actions):
        newstate, qos_newstate = find_newstate_qos(qos, iq, ia, action, qosDF)
        qosDF.at[iq, ia] = [newstate, qos_newstate]

# Save the dataframe to a file
qosDF.to_csv(f"{resFolder}/reward_{n_drones}.dat", sep=" ")

