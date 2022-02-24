#!/bin/bash

for i in {1..3}; do
  fname=objective_dylan_${i}_recall
  if [ ! -d ${fname} ]; then
    echo ${i} ${fname}
    boogie --pipeline pipelines/formulate_objective_dylan_seed.json ${i}
    mv objective ${fname}
  else
    echo "Already found ${fname}"
  fi
done
