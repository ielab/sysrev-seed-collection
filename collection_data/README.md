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



