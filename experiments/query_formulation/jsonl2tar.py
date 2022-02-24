import json
import os

# %%

with open("../data/seed_and_included_edited_edited.jsonl", "r") as f:
    lines = f.readlines()
data = []
for line in lines:
    data.append(json.loads(line))

# %%
basedir = "topics_tar_format_seed"
os.makedirs(basedir, exist_ok=True)
nl = '\n'
tb = '\t'
for topic in data:
    with open(f"{basedir}/{topic['id']}", "w") as f:
        f.write(f"""Topic: {topic['id']}

Title: {topic['title']}

Query: 
{topic['query']}

Pids:
{nl.join([tb + x for x in topic['seed_studies']])}""")

# -----------------------------------------------------------
basedir = "topics_tar_format_included"
os.makedirs(basedir, exist_ok=True)
nl = '\n'
tb = '\t'
for topic in data:
    with open(f"{basedir}/{topic['id']}", "w") as f:
        f.write(f"""Topic: {topic['id']}

Title: {topic['title']}

Query: 
{topic['query']}

Pids:
{nl.join([tb + x for x in topic['included_studies']])}""")
# %%
