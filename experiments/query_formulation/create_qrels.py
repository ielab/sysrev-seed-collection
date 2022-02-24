import json

# %%

with open("../data/seed_and_included.jsonl", "r") as f:
    lines = f.readlines()
data = {}
for line in lines:
    data_line = json.loads(line)
    data[data_line["id"]] = data_line

# %%
with open("seed_studies.qrels", "w") as f:
    for topic_id, topic in data.items():
        for seed_study in topic["seed_studies"]:
            f.write(f"{topic_id} 0 {seed_study} 1\n")
with open("included_studies.qrels", "w") as f:
    for topic_id, topic in data.items():
        for study in topic["included_studies"]:
            f.write(f"{topic_id} 0 {study} 1\n")
# %%
