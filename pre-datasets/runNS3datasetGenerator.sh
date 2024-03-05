#!/bin/sh
# dataset Generator

exec 3< gatewaysPositions_1G.dat

  # Read the file line by line
while IFS= read -r line <&3
do
  # process each line
  echo "$line"
#  for s in $(seq 1 30); do #30 executions
#    start=$(date +%s.%N)
#    # device sets (10 devices to 50 devices)
#    for d in 10 20 30 40 50; do
#      echo "teste $d"
#    done
#  done
#  end=$(date +%s.%N)
#  runtime=$(python -c "print(${end} - ${start})")
#  echo "Runtime was [$runtime]. Run:[$s]"
done
# Close the file descriptor
exec 3<&-
