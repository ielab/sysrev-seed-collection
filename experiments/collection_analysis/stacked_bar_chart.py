import json
import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT
import json
import matplotlib.pyplot as plt
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("--included_information", type=str, default="data/seed_and_included.jsonl")
parser.add_argument("--snowballing_file_included", type=str, default="data/snowballing/included_based/seed_and_included/searching_content/search_output.tsv")
parser.add_argument("--snowballing_file_seed", type=str, default="data/snowballing/seed_based/seed_and_included/searching_content/search_output.tsv")
parser.add_argument("--searching_file", type=str, default="data/results/results_restricted.res")
args = parser.parse_args()

ra = args.included_information
snowballing_file_included = args.snowballing_file_included
snowballing_file_seed = args.snowballing_file_seed
search_file = args.searching_file

ra_dict = {}
seed_dict = {}

with open(ra) as f:
    for line in f:
        current_dict = json.loads(line)
        id = current_dict["id"]
        seeds = current_dict["seed_studies"]
        included = current_dict["included_studies"]
        ra_dict[id] = included
        seed_dict[id] = seeds

sfi_dict = {}
sfs_dict = {}

with open(snowballing_file_included) as f:
    for line in f:
        items = line.split()
        id = items[0]
        if id =="88a" or id=="88b":
            id = "88"
        files = items[1].split("|")
        sfi_dict[id] = files

with open(snowballing_file_seed) as f:
    for line in f:
        items = line.split()
        id = items[0]
        if id =="88a" or id=="88b":
            id = "88"
        files = items[1].split("|")
        sfs_dict[id] = files
searching_dict = {}
with open(search_file) as f:
    for line in f:
        items = line.split()
        id = items[0]
        if id in searching_dict:
            searching_dict[id].append(items[2])
        else:
            searching_dict[id] = [items[2]]


percentage = 0
zero_count = 0
count_overall_list = {}
overall_count = []
not_retrieved_list = []
for id in ra_dict:
    ra_files = ra_dict[id]
    sfs_files=[]
    sfi_files = []
    seed_files = []
    search_files = []
    if id in seed_dict:
        seed_files = seed_dict[id]
    if id in sfs_dict:
        sfs_files = sfs_dict[id]
    if id in sfi_dict:
        sfi_files = sfi_dict[id]
    if id in searching_dict:
        search_files = searching_dict[id]
    countsfs = 0
    countsfi = 0
    count_search = 0
    count_seed = 0
    count_overall = 0
    not_retrieved = 0
    for f in ra_files:
        if (f in sfs_files):
            countsfs +=1
        if (f in sfi_files):
            countsfi +=1
        if (f in search_files):
            count_search +=1
        if (f in seed_files):
            count_seed +=1
        if  (f in seed_files) or (f in search_files) or (f in sfs_files) or (f in sfi_files) :
            count_overall +=1
        else:
            not_retrieved += 1
            #print(id, f)
    overall_count.append(count_overall)
    not_retrieved_list.append(not_retrieved)
    print(id, count_seed/len(ra_files), countsfs/len(ra_files), count_search/len(ra_files), countsfi/len(ra_files)
          , count_overall/len(ra_files))
    count_overall_list[id] = count_overall/len(ra_files)
    percentage += count_overall / len(ra_files)

print(statistics.mean(overall_count))
print(statistics.median(overall_count))
print(statistics.mean(not_retrieved_list))
print(statistics.median(not_retrieved_list))
print(percentage/40)
sorted_list_retrieved = {k: v*100 for k, v in sorted(count_overall_list.items(), key=lambda item: item[1])}
sorted_list_not_retrieved = {k: (1-v)*100 for k, v in sorted(count_overall_list.items(), key=lambda item: item[1])}
keys_set = list(sorted_list_retrieved.keys())
retrieved_set = list(sorted_list_retrieved.values())
not_retrieved_set = list(sorted_list_not_retrieved.values())
colors = ['#FF9999', '#00BFFF','#C1FFC1','#CAE1FF','#FFDEAD']
width = 0.7
fig, ax = plt.subplots()
ax.barh(keys_set, [x/100 for x in retrieved_set], width, label="Retrieved", color="grey")
ax.barh(keys_set, [x/100 for x in not_retrieved_set], width, left=[x/100 for x in retrieved_set], label="not_retrieved", color="silver")
plt.xlabel("Recall", fontsize = 13)
plt.ylabel("Topics", fontsize=13)
plt.xticks(fontsize=10)
plt.yticks(fontsize=5,  color = 'w')
plt.legend(["Retrieved","Not Retrieved"], loc="lower center",bbox_to_anchor=(0.5, 1.02), ncol=2, fontsize=13)
fig.set_size_inches(6, 4)
plt.tight_layout()
plt.savefig("graph/recall_bar_chart.pdf")
#print(sorted_list_retrieved)