## For folder **experiment**:

Three experiments in the paper are included in this folder, including:
>- **query_formulation:** Automatic query formulation expeirment.
>- **sdr_document_ranking:** Seed-driven document ranking.
>- **sdr_snowballing:** Seed-driven snowballing document ranking.

For collection analysis:
>- **collection_analysis:** code running for original collection analysis and graph making.

***

## Code to run
> ### Before running seed_driven document ranking or snowballing document ranking experiment, you need to run the following code to get title and abstract of all pubmed article title and abstract:
> `mkdir collection`<br>
> `python3 gather_all_pids.py`<br>
> `python3 collection_gathering.py`<br>
> `python3 collection_processing.py` <br>
> #### In this way you will create a jsonl file inside folder **collection** that's storing the processed title and abstract of all pubmed articles appeared in the collection.

***
Please refer to paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"
