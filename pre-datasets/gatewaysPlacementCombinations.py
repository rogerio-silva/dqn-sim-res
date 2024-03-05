import itertools
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("nGat")
parser.add_argument("path")

args = parser.parse_args()
cwd = os.getcwd()
resFolder = "{}/".format(cwd) + args.path

matrix_size = 10
objects_to_place = int(args.nGat)

# Generate all possible positions for the objects
positions = list(itertools.combinations_with_replacement(range(matrix_size * matrix_size), objects_to_place))

# Filter out the positions where objects occupy the same position
positions = [position for position in positions if len(set(position)) == objects_to_place]

# Convert the positions to (x, y) coordinates
for i, position in enumerate(positions):
    positions[i] = [((pos // matrix_size)*1000+500, (pos % matrix_size)*1000+500, 45) for pos in position]

# Print the positions
print(len(positions))

# Write the positions to a file
with open(f"{resFolder}/gatewaysPositions_{objects_to_place}G.dat", "w") as f:
    for pos in positions:
        for p in pos:
            f.write(f"{p[0]},{p[1]},{p[2]}:")
        f.write(f"\n")

