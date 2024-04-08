#!/bin/sh
# to run this code type: ./runNS3datasetGenerator.sh -g <number_of_gateways>
# shellcheck disable=SC1068
progr="~/git/ns-allinone-3.40/ns-3.40/build/scratch/ns3.40-generate-dataset-dqn-experiment-debug"

# get prompt parameter
while getopts "g:" opt; do
  case $opt in
    g) g=$OPTARG ;;
    \?) echo "Invalid option -$OPTARG"; exit 1 ;;
  esac
done
state=0
thread=1
seed=1
fname="gatewaysPositions_${g}G.dat"

# dataset Generator
exec 3< $fname
while IFS= read -r line <&3
do
#  for s in $(seq 1 10); do #seed = 30 executions
    start=$(date +%s.%N)
    # device sets (10 devices to 50 devices)
#    for d in 10 20 30 40 50; do
      d10="$progr --nDevices=10 --nGateways=$g --state=$state --seed=$seed --tGatewaysPositions=$line"
      # shellcheck disable=SC2090
      echo $d10
      # shellcheck disable=SC2003
      thread=$(expr $state % 20)
      taskset -c $thread $d10 &
      pid=$!
      if [ "$thread" -eq 0 ]; then
        waitpid $pid
      fi
#    done
    end=$(date +%s.%N)
    runtime=$(python -c "print(${end} - ${start})")
    echo "Runtime was [$runtime]. Run:[$s]"
#  done
  # shellcheck disable=SC2004
  state=$(($state+1))
  wait
done
exec 3<&-
