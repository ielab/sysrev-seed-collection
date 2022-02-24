## Seed-driven document ranking

***

### For reproduce result obtained in the paper:

Firstly, for single-pseudo-studies experiment:

> `mkdir run_search`<br>
> `mkdir run_search/single`<br>
> `mkdir run_search/single/input` <br>
> `mkdir run_search/single/output` <br>
> `mkdir run_search/single/eval` <br>

The above code would create folders for input, output and evaluation results of the experiment.

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation.py` <br>

Next please run:

> `python3 search.py --METHOD RANKING_METHOD`<br>

> Note RANKING_METHOD can include: BM25_BOW, QLM_BOW, SDR_BOW, AES_BOW, AES_BOW_P

You will need to download word2vec embeddings in order to run the AES methods.

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> `python3 aes_sdr_combine.py --AES_METHOD AES_BOW --COM_METHOD SDR_BOW_AES` <br>
> `python3 aes_sdr_combine.py --AES_METHOD AES_BOW_P --COM_METHOD SDR_BOW_AES_P`

Then evaluation can be down using:
> `python3 evaluation --METHOD RANKING_METHOD --trec_eval TREC_EVAL_DIRECTORY --tar_eval TAR_EVAL_DIRECTORY` <br>

Note you need to use tar_eval and trec_eval for evaluation.

***

For multiple-pseudo-studies experiment:
> `mkdir run_search/multiple`<br>
> `mkdir run_search/multiple/input` <br>
> `mkdir run_search/multiple/output` <br>
> `mkdir run_search/multiple/eval` <br>

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation_multiple.py --option no_seed` <br>

Next please run:

> `python3 search_multiple.py --METHOD RANKING_METHOD`<br>

ou will need to download word2vec embeddings in order to run the AES methods

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> `python3 aes_sdr_combine.py --DATA_DIR run_search/multiple --AES_METHOD AES_BOW --COM_METHOD SDR_BOW_AES` <br>
> `python3 aes_sdr_combine.py --DATA_DIR run_search/multiple --AES_METHOD AES_BOW_P --COM_METHOD SDR_BOW_AES_P`

Then evaluation can be down using:
> `python3 evaluation --DATA_DIR run_search/multiple --METHOD RANKING_METHOD --trec_eval TREC_EVAL_DIRECTORY --tar_eval TAR_EVAL_DIRECTORY` <br>

***


For real seed experiment:
> `mkdir run_search/seed`<br>
> `mkdir run_search/seed/input` <br>
> `mkdir run_search/seed/output` <br>
> `mkdir run_search/seed/eval` <br>

Next, to creatre input (qrels, queries etc), please run:

> `python3 topic_query_generation_multiple.py --option seed` <br>

Next please run:

> `python3 search_multiple.py --METHOD RANKING_METHOD`<br>

ou will need to download word2vec embeddings in order to run the AES methods.

Then to generate fused method: SDR_BOW_AES_P, and SDR_BOW_AES, please run:

> `python3 aes_sdr_combine.py --DATA_DIR run_search/seed --AES_METHOD AES_BOW --COM_METHOD SDR_BOW_AES` <br>
> `python3 aes_sdr_combine.py --DATA_DIR run_search/seed --AES_METHOD AES_BOW_P --COM_METHOD SDR_BOW_AES_P`

Then evaluation can be down using:
> `python3 evaluation --DATA_DIR run_search/seed --METHOD RANKING_METHOD --trec_eval TREC_EVAL_DIRECTORY --tar_eval TAR_EVAL_DIRECTORY` <br>

***

Please refer to the paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"
