## Scratch folder
This folder contains the ns-3 simulation code.

The code is used to generate the QoS datasets used to train the DQN model.

You need to have the ns-3 simulator, and the module `LoRaWAN`,  installed on your machine. To compile this code, copy them to the `ns-3/scratch` folder, compile anr.

To run the code, use the following command:
```bash
./ns3 run 'scratch/generate-dataset-dqn-experiment.cc --nDevices=10 --seed=1 --state=1 --nGateways=3 --tGatewaysPositions="500,500,45:500,1500,45:500,6500,45:"'
```
or compile ns-3 code and run the script `runNS3datasetGenerator.sh` with the following command:
Before running the script, make sure to edit the script to set the path to the ns-3 simulator on line 4.
```bash

./runNS3datasetGenerator.sh -g <number_of_gateways>
```
