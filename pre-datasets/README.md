# Pre-DQN datasets
Pre-DQN datasets are available in the `pre-datasets` directory.
The datasets are stored in the `.dat` text format.

---
## Python Code ```gatewaysPlacementCombinations.py```
This code generates all possible positioning combinations of "n" gateways within a 10km^2 area

## File ```gatewaysPositions__G.dat```
The file contains the positions of the gateways in the scenario. 
It contains the following keys:
+ Each line in the dataset is one combination of drones positions
+ The number of drones per line is expressed on filename. e.g.: 
`gatewaysPositions_2G.dat` contains 2 drones per line.
+ Token <,> separates the drones coordinates ( x,y,z).
+ Token <:> separates each drone.

e.g.:
``` 500,500,45:500,1500,45: ```
means that the first drone is at position (500,500,45) and the second 
drone is at position (500,1500,45).

---

## Folder ```results/```
This folder contains the results of the simulations.
Each file contains the results of the simulations for a specific scenario.
The files are named as follows:
+ `transmissionData___.dat` contains the number of sent and received packets per number of gateways (g) and number of devices (d) `gxd`.
```Header: seed, sentPackets, receivedPackets```
+ `transmissionPackets___.dat` contains the packets transmission summary per seed (s), number of gateways (g) and devices (d) `s_gxd`.
```Header: senderId, receiverId, sentTime, receivedTime, delay```
+ `transmissionParameters___.dat` contains the parameters of the simulation per seed (s), number of gateways (g) and devices (d) `s_gxd`.
```Header: device_id, sf, txPower, datarate```

## ToDo: Develop a script to generate the datasets, compute QoS metrics and plot the results. 
