import json
import argparse
import math
import itertools
from tqdm import tqdm
import os
size = 1000
import random

parser = argparse.ArgumentParser()
parser.add_argument("--input_json", type=str, default="data/overall_collection.jsonl")
parser.add_argument("--option", type=str, default="seed-search")
parser.add_argument("--input_qrel", type=str, default ="data/qrels/search_based/sr_collection.qrels")
args = parser.parse_args()
option = args.option
seed_dict = {}

if option == "seed-search":
    DATA_dir = "run_snowballing/seed-search"
    input_snowballing = open("data/qrels/snowballing/seed_based/sr_snowballing.qrels", 'r')
else:
    DATA_dir = "run_snowballing/included"
    input_snowballing = open("data/qrels/snowballing/included_based/sr_snowballing.qrels", 'r')


seed_json = args.input_json
input_qrel_file = args.input_qrel
input_eval_file = args.input_qrel
input_test_eval_file = args.input_qrel
output_test_eval_file_run = os.path.join(DATA_dir, "input", "eval_test_topic_id.tsv")
output_queries_file = os.path.join(DATA_dir, "input", "queries.tsv")
output_run_fie = os.path.join(DATA_dir, "input", "run.jsonl")
output_eval_file_run = os.path.join(DATA_dir, "input", "eval_id.tsv")

json_read = open(seed_json, 'r').readlines()
input_qrel = open(input_qrel_file, 'r')
input_eval = open(input_eval_file, 'r')
input_test_eval = open(input_test_eval_file, 'r')
output_quries = open(output_queries_file, 'w')
output_test_eval_run = open(output_test_eval_file_run, 'w')
output_eval_for_run = open(output_eval_file_run, 'w')
output_run = open(output_run_fie, 'w')

doc_dict = {}
qid_list = []
doc_positive_dict = {}

for line in json_read:
    current_dict = json.loads(line)
    id = current_dict['id']
    seed_studies = current_dict["seed_studies"]
    seed_dict[id] = seed_studies
    doc_positive_dict[id] = current_dict["included_studies"]
    qid_list.append(id)

lines = input_snowballing.readlines()
for line in tqdm(lines):
    items = line.split()
    original_id = items[0]
    if original_id in seed_dict:
        if original_id  in doc_dict:
            doc_dict[original_id].append(items[2])
        else:
            doc_dict[original_id] = [items[2]]


if option == "seed-search":
    lines = input_qrel.readlines()
    for line in tqdm(lines):
        items = line.split()
        original_id = items[0]
        if original_id in seed_dict:
            if original_id in doc_dict:
                doc_dict[original_id].append(items[2])
            else:
                doc_dict[original_id] = [items[2]]
    input_qrel.close()
else:
    lines = input_qrel.readlines()
    for line in tqdm(lines):
        items = line.split()
        original_id = items[0]
        if original_id in doc_dict:
            if items[2] in doc_dict[original_id]:
                doc_dict[original_id].remove(items[2])
        if original_id in doc_positive_dict:
            current_list = doc_positive_dict[original_id]
            if int(items[-1]) == 1:
                if items[2] in current_list:
                    current_list.remove(items[2])
                    doc_positive_dict[original_id] = current_list
                    if items[2] not in seed_dict[original_id]:
                        seed_dict[original_id].append(items[2])
    input_qrel.close()
eval_dict = {}
eval_list = []
for qid in tqdm(qid_list):
    data_positive_list = set(doc_positive_dict[qid])
    data_positive_list = list(data_positive_list)
    if qid in doc_dict:
        data_list = doc_dict[qid]

    seed_list = set(seed_dict[qid])
    print(qid, len(data_list), len(data_positive_list), len(seed_list))
    id = qid
    for seed_id in seed_list:
        id = id + '_' + seed_id.strip()
    removed_list = set(data_list)
    removed_list = list(removed_list)

    new_dict = {
        'qid': id,
        'pid': removed_list
    }

    json.dump(new_dict, output_run)
    output_run.write('\n')
    output_eval_file = os.path.join(DATA_dir, "input", qid + ".qrel")
    output_eval = open(output_eval_file, 'w')
    if len(removed_list) != 0:
        output_eval_for_run.write(id + '\n')
        output_test_eval_run.write(id + '\n')
    for ppid in data_positive_list:
        output_eval.write(id + '\t' + 'Q0\t' + ppid + '\t' + '1' + '\n')
    output_eval.close()

output_run.close()
output_eval_for_run.close()
