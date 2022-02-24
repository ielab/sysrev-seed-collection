## Seed-driven snowballing document ranking

***

### For reproduce result obtained in paper:

Firstly, for seed_snowballing + search experiment:

> `mkdir run_snowballing`<br>
> `mkdir run_snowballing/seed-search`<br>
> `mkdir run_snowballing/seed-search/input` <br>
> `mkdir run_snowballing/seed-search/output` <br>
> `mkdir run_snowballing/seed-search/eval` <br>

Above code would create folders for input, output and evaluation result of experiment.

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation_snowballing.py` <br>

Next please run:

> `python3 search_multiple.py --METHOD RANKING_METHOD`<br>

> Note RANKING_METHOD can include: BM25_BOW, QLM_BOW, SDR_BOW, AES_BOW, AES_BOW_P

You will need to downalod word2vec embeedings in order to run AES method

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> `python3 aes_sdr_combine.py --AES_METHOD AES_BOW --COM_METHOD SDR_BOW_AES` <br>
> `python3 aes_sdr_combine.py --AES_METHOD AES_BOW_P --COM_METHOD SDR_BOW_AES_P`

Then evaluation can be down using:
> `python3 evaluation --METHOD RANKING_METHOD --trec_eval TREC_EVAL_DIRECTORY --tar_eval TAR_EVAL_DIRECTORY` <br>

Note you need to use tar_eval and trec_eval for evaluation.

***

Secondly, for screened-snowballing experiment:

> `mkdir run_snowballing/included`<br>
> `mkdir run_snowballing/included/input` <br>
> `mkdir run_snowballing/included/output` <br>
> `mkdir run_snowballing/included/eval` <br>

Above code would create folders for input, output and evaluation result of experiment.

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation_snowballing.py --option included` <br>

Next please run:

> `python3 search_multiple.py --DATA_DIR run_snowballing/included --METHOD RANKING_METHOD`<br>

> Note RANKING_METHOD can include: BM25_BOW, QLM_BOW, SDR_BOW, AES_BOW, AES_BOW_P

You will need to downalod word2vec embeedings in order to run AES method

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> `python3 aes_sdr_combine.py --DATA_DIR run_snowballing/included --AES_METHOD AES_BOW --COM_METHOD SDR_BOW_AES` <br>
> `python3 aes_sdr_combine.py --DATA_DIR run_snowballing/included --AES_METHOD AES_BOW_P --COM_METHOD SDR_BOW_AES_P`

Then evaluation can be down using:
> `python3 evaluation --DATA_DIR run_snowballing/included --METHOD RANKING_METHOD --trec_eval TREC_EVAL_DIRECTORY --tar_eval TAR_EVAL_DIRECTORY` <br>

Note you need to use tar_eval and trec_eval for evaluation.

***

Please refer to paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"
