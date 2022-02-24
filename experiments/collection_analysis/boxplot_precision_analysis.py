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
parser.add_argument("--searching_file", type=str, default="data/qrels/search_based/sr_collection.qrels")
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
with open(search_file, 'r') as f:
    for line in f:
        items = line.split()
        id = items[0]
        study = items[2]
        if id not in searching_dict:
            searching_dict[id] = [study]
        else:
            searching_dict[id].append(study)
seed_p= []
search_p = []
seed_snowballing_p = []
seed_snowballing_search_p = []
search_included_snowballing_p = []
seed_snowballing_search_snowballing_p = []
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
    seed = 0
    search = 0
    seed_snowballing = 0
    seed_snowballing_search = 0
    search_included_snowballing = 0
    seed_snowballing_search_snowballing = 0
    for f in ra_files:
        if f in seed_files:
            seed +=1
        if (f in sfs_files):
            seed_snowballing += 1
        if (f in search_files):
            search += 1

        if (f in sfs_files) or (f in seed_files) or (f in search_files):
            seed_snowballing_search += 1
        if (f in sfi_files) or (f in seed_files) or (f in search_files):
            search_included_snowballing += 1
        if (f in sfi_files) or (f in seed_files) or (f in search_files) or (f in sfs_files):
            seed_snowballing_search_snowballing += 1

    seed_p.append(seed/len(seed_files))
    search_p.append(search/len(searching_dict[id]))
    seed_snowballing_p.append(seed_snowballing/len(sfs_dict[id]))

    seed_snowballing_search_p.append(seed_snowballing_search/len(set(search_files+sfs_files+seed_files)))

    search_included_snowballing_p.append(search_included_snowballing/len(set(search_files+sfi_files+seed_files)))
    seed_snowballing_search_snowballing_p.append(seed_snowballing_search_snowballing/len(set(search_files+sfs_files+seed_files+sfs_files)))

print(statistics.mean(search_p))
print(statistics.mean(seed_snowballing_p))

print(statistics.mean(seed_snowballing_search_p))
print(statistics.mean(search_included_snowballing_p))
print(statistics.mean(seed_snowballing_search_snowballing_p))
with plt.rc_context({
    "axes.spines.right": False,
    "axes.spines.top": False,
}):
    plt.figure(figsize=(7, 6))
    plt.xlim([-0.1, 1.1])
    plt.xticks(fontsize=20)
    plt.boxplot([seed_p, seed_snowballing_p, search_p, seed_snowballing_search_p, search_included_snowballing_p, seed_snowballing_search_snowballing_p], vert=False, widths=0.2 )
    plt.yticks([])

    #plt.yticks([1, 2, 3, 4, 5, 6], ['Seed', 'Seed-snowballed','Searched', '(Seed-snowballed)+(Searched)', '(Searched)+(Screened-snowballed)', '(Seed-snowballed)+(Searched)+(Screened-snowballed)'], fontsize=12)
    plt.xlabel("Precision", fontsize=20)
    #plt.ylabel("Retrieval method", fontsize=20)
    plt.tight_layout()
    plt.savefig("graph/box_plot_precision.pdf")