# sysrev-seed-collection
This is a collection repository for systematic review topics with seed studies.
The file is separated into two sections:
>- **collection_data**: contains organised data, including basic data, search data and snowballing data.
>- **experiments**: contains the result and data usage for three experiments, including seed-driven query formulation, seed-driven document ranking, and seed driven snowballing document ranking.
***

## For folder **collection_data**:

>- **overall_collection.jsonl**: with each line referring to one topic, every topic includes following attributes:

| Attributes | Description |
| ----------- | ----------- |
| id | correpsonds to ID in paper |
| link_to_review | corresponds to Link to Review in paper |
| title | Corresponds to Title in paper |
| search_name | corresponds to Description in paper |
| Date_from | Corresponds to Date restriction in paper |
| Date_to | Corresponds to Date restriction in paper |
| query | Corresponds to PubMed query in paper |
| seed_studies | Corresponds to Seed studies in paper |
| included_studies | Corresponds to DIncluded studies in paper |
<br>

>- **search**: a folder containing candidate_documents.res, which is a trec format file for candidate documents retrieved by systematic review boolean queries, this file corresponds to **Retrieved studies** in paper
<br>

>- **snowballing**: a folder containing seed_snowballing_document.tsv and screened_snowballing_documeent.tsv, these two files are for snowballing candidate document, every line corresponds to one topic, topic and documents' list is separated by \t, documents' ids are separated by '|', these two files correspond to **Snowballed studies** in paper

***


<br>

## For folder **experiment**:

Three experiments in the paper are included in this folder, including:
- **query_formulation:** Automatic query formulation experiment.
- **sdr_document_ranking:** SDR-driven document ranking.
- **sdr_snowballing:** SDR-driven snowballing document ranking.

Instructions on how to run these experiments are inside each experiment folder.

***

For sample data extraction processing, please run:

`python3 sample_data_processing.py`
> This is a sample data extraction work, with an input of topic id; the python script will output all the information for this topic.

***

Please refer to the paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"


