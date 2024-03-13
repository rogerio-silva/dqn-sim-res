# Pre-DQN datasets

Pre-DQN datasets are available in the `pre-datasets` directory.
The datasets are stored in the `.dat` text format.

---

## Python Code ```gatewaysPlacementCombinations.py```

This code generates all possible positioning combinations of "n" gateways within a 10km^2 area

## Files ```gatewaysPositions__G.dat```

The file contains the positions of the gateways in the scenario.
It contains the following keys:

+ Each line in the dataset is one combination of drones positions
+ The number of drones per line is expressed on filename. e.g.:
  `gatewaysPositions_2G.dat` contains 2 drones per line.
+ Token <,> separates the drones coordinates ( x,y,z).
+ Token <:> separates each drone.

e.g.:
``` 500,500,45:9500,1500,45: ```
means that the first drone is at position (500,500,45) and the second
drone is at position (9500,1500,45).

---

## Folder ```results/```

This folder contains the results of the simulations.
Each file contains the results of the simulations for a specific scenario.
The files are named as follows:

+ `qos_<g>.dat`: this file contains the QoS metrics for each combination 
of gateways positions. `<g>` denotes the number of gateways adopted. 

e.g.: `qos_2.dat` contains the QoS metrics for the scenario with 2 gateways.

+ `rewards.csv`: this file contains the rewards for each combination of states
and actions to run. 
```
-------------------------------------------------------------------------------
| state | <new_state_1, expected_reward_1> | <new_state_n, expected_reward_n> |
-------------------------------------------------------------------------------
|  12   |     10,            0,5           |     11,            0,7           |   
-------------------------------------------------------------------------------
```
