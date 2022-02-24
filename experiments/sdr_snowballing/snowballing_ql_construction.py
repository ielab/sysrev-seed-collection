import json

files = ["seed_and_included.jsonl"]
dic_cand = {}
with open("data/snowballing/seed_based/seed_and_included/searching_content/search_output.tsv", 'r') as f:
    for line in f:
        items = line.split()
        id = items[0]
        studies = items[1].split('|')
        studies = [x.strip() for x in studies ]
        dic_cand[id] = studies


included_dict = {}
for file in files:
    file_input = "data/" + file
    with open(file_input) as f:
        for line in f:
            items = json.loads(line)
            id = items["id"]
            included_study = items["included_studies"]
            included_dict[id] = included_study
fw = open('data/qrels/snowballing/seed_based/sr_snowballing.qrels', 'w')
for id in dic_cand:

    all_study = dic_cand[id]


    included_study = included_dict[id]
    count = 0
    for s in all_study:
        if s in included_study:
            fw.write(id+" 0 " + s + " 1\n")
        else:
            fw.write(id + " 0 " + s + " 0\n")
    for s in included_study:
        if s not in all_study:
            count+=1

    print(id, count, len(included_study), len(all_study))