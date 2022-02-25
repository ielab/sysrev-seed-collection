import json
import trectools

pes = {"statistic": {"email": "email@gmail.com", "tool": "querylab", "key": "api_key"}, "pmids": []}
pmids = set()
data = []
with open("../data/seed_and_included_edited_edited.jsonl", "r") as f:
    for line in f:
        data.append(json.loads(line))
for item in data:
    for seed_pmid in item["seed_studies"]:
        pmids.add(int(seed_pmid))
    for included_study in item["included_studies"]:
        pmids.add(int(included_study))

with open("pipelines/get_titles.pes.json", "w") as f:
    pes["pmids"] = list(pmids)
    json.dump(pes, f)

# %%
