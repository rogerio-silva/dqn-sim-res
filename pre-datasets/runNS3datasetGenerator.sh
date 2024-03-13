#!/bin/sh

# shellcheck disable=SC1068
progr="/home/rogerio/git/ns-allinone-3.40/ns-3.40/build/scratch/ns3.40-generate-dataset-dqn-experiment-debug"
g=2
state=0
thread=1
seed=1

# dataset Generator
exec 3< gatewaysPositions_2G.dat
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
      if [ "$thread" -eq 0 ]; then
        wait
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
