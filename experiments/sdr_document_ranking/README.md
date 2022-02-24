## Seed-driven document ranking


***

### For reproduce result obtained in paper:

Firstly, for single-pseudo-studies experiment:

> `mkdir run_search`<br>
> `mkdir run_search/single`<br>
> `mkdir run_search/single/input` <br>
> `mkdir run_search/single/output` <br>
> `mkdir run_search/single/eval` <br>

Above code would create folders for input, output and evaluation result of experiment.

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation.py` <br>

Next please run:

> `python3 search.py --METHOD YOUR_RANKING_METHOD`<br>

> Note YOUR_RANKING_METHOD can include: BM25_BOW, QLM_BOW, SDR_BOW, AES_BOW, AES_BOW_P

You will need to downalod word2vec embeedings in order to run AES method

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> 

Then evaluation can be down using:


***






!Please refer to paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"



