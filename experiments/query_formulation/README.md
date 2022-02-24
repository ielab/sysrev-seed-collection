# sysrev-seed-collection
This is a collection repository for systematic review with seed studies.
The file is seperated into two sections:
>- **collection_data**: contains organised data, including basic data, search data and snowballing data.
>- **experiments**: contains result and data usage for three experiments, including seed-driven query formulation, seed-driven document ranking, and seed driven snowballing document ranking.
***

## For folder **collection_data**:

>- **overall_collection.jsonl**: with each line refering to one topic, every topics includes following attributes:

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

>- **search**: folder containing candidate_documents.res which is a trec format file for candidate documents retrieved by query, this file corresponds to **Retrieved studies** in paper
<br>

>- **snowballing**: folder containing seed_snowballing_document.tsv and screened_snowballing_documeent.tsv, these two files are for snowballing candidate document, every line corresponds to one topic, topic and documents' list is seperated by \t, documents' ids are seperated by '|', these two files corresponds to **Snowballed studies** in paper

***


<br>

## For folder **experiment**:


***

For sample data extraction processing, please run:

`python sample_data_processing.py`

!Please refer to paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"


