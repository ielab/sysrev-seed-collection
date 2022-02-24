import json
import argparse
import statistics

from tqdm import tqdm
overall = 0
overall2 = 0

included_studies_dict = {}
seed_list = []
with open("data/seed_and_included.jsonl", 'r') as f:
    percentages = 0
    for index, line in enumerate(f):
        items = json.loads(line)
        id = items['id']
        name = items["search_name"]
        seeds = items["seed_studies"]
        overall += len(seeds)
        inclus = items["included_studies"]
        seed_list.append(len(seeds))
        included_studies_dict[id] = inclus
        overall2 += len(inclus)
        count = 0
        for seed in seeds:
            if seed in inclus:
                count+=1
        percentage = count/len(inclus)

        percentages += percentage
        #print(id, name, len(seeds), percentage)
    #print(overall/(index+1))
    #print(overall2 / (index + 1))
    #print("all",index+1, percentages/(index+1))
all_dic = {}
with open("data/results/results_restricted.res") as f:
    for line in tqdm(f):
        items = line.split()
        if items[0] not in all_dic:
            all_dic[items[0]] = [items[2]]
        else:
            all_dic[items[0]].append(items[2])
results_dict = {}
output = open("b.txt", 'w')
percentage_list = []
for qid in included_studies_dict:
    inclus = included_studies_dict[qid]
    if qid not in results_dict:
        results_dict[qid] = []
    for i in inclus:
        if i in all_dic[qid]:
            results_dict[qid].append(i)
    if len(results_dict[qid])>0:
        percentage_list.append(len(results_dict[qid])/(len(included_studies_dict[qid])))
        #print(qid, len(all_dic[qid]))
    output.write(qid+ '\t' +  ','.join(results_dict[qid]) + '\n\n' )

        #print(qid)
print(statistics.median([len(x) for x in included_studies_dict.values()]))
print(statistics.median(seed_list))
count = sum(percentage_list)/len(percentage_list)
print(count, len(percentage_list))
print(overall/len(included_studies_dict))
print(overall2/len(included_studies_dict))
print(percentages/len(included_studies_dict))


