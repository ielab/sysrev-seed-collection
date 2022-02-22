# sysrev-seed-collection
This is a collection repository for systematic review with seed studies.
The file is seperated into two sections:
- collection_data: contains organised data, including basic data, search data and snowballing data.
- experiments: contains result and data usage for three experiments, including seed-driven query formulation, seed-driven document ranking, and seed driven snowballing document ranking.

For collection data:

- overall_collection.jsonl: with each line refering to one topic, every topics includes following attributes:

    | Attributes | Description |
    | --- | ----------- |
    | id | Title |
    | search_name | Text |
    | Date_from | Title |
    | Date_to | Text |
    | query | Title |
    | seed_studies | Text |
    | included_studies | Text |
- search: folder containing candidate_documents.res which is a trec format file for candidate documents retrieved by query.
- snowballing: folder containing seed_snowballing_document.tsv and screened_snowballing_documeent.tsv, these two files are for snowballing candidate document, every line corresponds to one topic, topic and documents' list is seperated by \t, documents' ids are seperated by '|'




Please refer to paper "From Little Things Big Things Grow: A Collection with Seed Studies for Medical Systematic Review Literature Search"


