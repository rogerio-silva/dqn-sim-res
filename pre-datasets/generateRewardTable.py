import pandas as pd
import itertools
import os
import argparse
import time
from tqdm import tqdm

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
def find_target_state_qos(iq, ia):
    target_state = 0
    actual_state = states[iq]
    target_position = [-1 for _ in range(n_drones)]
    actual_positions = positions[iq]
    acts = actions[ia]

    for ai, ac in enumerate(acts):
        if ac == 'Up':
            if actual_positions[ai] + matrix_size >= matrix_size * matrix_size:
                target_state = -1
                break
            target_position[ai] = actual_positions[ai] + matrix_size
        elif ac == 'Down':
            if actual_positions[ai] - matrix_size < 0:
                target_state = -1
                break
            target_position[ai] = actual_positions[ai] - matrix_size
        elif ac == 'Left':
            if actual_positions[ai] % matrix_size == 0:
                target_state = -1
                break
            target_position[ai] = actual_positions[ai] - 1
        elif ac == 'Right':
            if actual_positions[ai] % matrix_size == matrix_size - 1:
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
    if len(set(target_position)) < n_drones:
        return [iq, -2]

    target_state = states[positions.index(tuple(target_position))]
    qos_target_state = qosDF.at[target_state, 'qos']
    ret = [target_state, qos_target_state]
    return ret


start_time = time.time()

# Read the QoS values from the file to a dataframe
qosDF = pd.read_csv(f"{resFolder}/qos_{n_drones}.dat",
                    sep=" ", index_col="state")

print("Processing rewards...")
string_line = ""
file = open(f"{resFolder}/reward_{n_drones}.dat", 'w')
string_line = "state qos " + " ".join([f"{ia}" for ia in range(len(actions))])

with open(f"{resFolder}/reward_{n_drones}.dat", 'a') as file:
    file.write(string_line + "\n")

for iq in tqdm(states, desc="Progress: ", unit=" states"):
    string_line = f"{iq} {qosDF.at[iq, 'qos']} "
    for ia, action in enumerate(actions):
        target_state, target_qos = find_target_state_qos(iq, ia)
        string_line += f'"[{target_state}, {target_qos}]" '
    # Save the string_line to a file
    with open(f"{resFolder}/reward_{n_drones}.dat", 'a') as file:
        file.write(string_line.rstrip() + "\n")

print("Reward table generated successfully")
file.close()
