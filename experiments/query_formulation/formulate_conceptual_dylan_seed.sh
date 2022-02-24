#!/bin/bash
mkdir -p conceptual_queries_term_feedback
for i in {1..3}; do
  fname=conceptual_queries_term_feedback/conceptual_term_feedback_${i}
  if [ ! -d ${fname} ]; then
    echo ${i} - ${fname}
    boogie --pipeline pipelines/formulate_conceptual_dylan_seed.json rake none elastic_umls none ${i}
    mv conceptual/0 ${fname}
  else
    echo "Already found ${fname}"
  fi
done

rm -rf conceptual
