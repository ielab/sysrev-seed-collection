import json
import argparse
import math
import itertools
from tqdm import tqdm
import os
size = 1000
import random

parser = argparse.ArgumentParser()
parser.add_argument("--input_json", type=str, default="data/seed_and_included.jsonl")
parser.add_argument("--option", type=str, default="seed")
parser.add_argument("--input_qrel", type=str, default ="data/qrels/search_based/sr_collection.qrels")
parser.add_argument("--input_res", type=str, default ="data/results/results_restricted.res")
parser.add_argument("--percentage", type=float, default=0.2)
parser.add_argument("--random_seed", type=int, default=2)
args = parser.parse_args()
option = args.option
seed_dict = {}

input_qrel_file = args.input_qrel
input_eval_file = args.input_qrel
input_res_file = args.input_res
input_test_eval_file = args.input_qrel
percentage = args.percentage
random_seed = args.random_seed

input_res = open(input_res_file, 'r')
input_qrel = open(input_qrel_file, 'r')
input_eval = open(input_eval_file, 'r')
input_test_eval = open(input_test_eval_file, 'r')
seed_json = args.input_json
json_read = open(seed_json, 'r').readlines()


if option == "seed":
    DATA_dir = "run_search/multiple/Real-seed"
else:
    DATA_dir = "run_search/multiple/Pseudo-seed"

output_queries_file = os.path.join(DATA_dir, "input", "queries.tsv")
output_run_fie = os.path.join(DATA_dir, "input", "run.jsonl")
output_eval_file_run = os.path.join(DATA_dir, "input", "eval_id.tsv")
output_test_eval_file_run = os.path.join(DATA_dir, "input", "eval_test_topic_id.tsv")

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
    doc_positive_dict[id]= current_dict["included_studies"]
    qid_list.append(id)


lines = input_qrel.readlines()
if option =="seed":

    for line in tqdm(lines):
        items = line.split()
        original_id = items[0]
        if original_id in seed_dict:
            seed_list = seed_dict[original_id]
            if items[0] in doc_dict:
                doc_dict[items[0]].append(items[2])
            else:
                doc_dict[items[0]] = [items[2]]

        input_qrel.close()


    for qid in tqdm(qid_list):
        data_positive_list = set(doc_positive_dict[qid])
        data_positive_list = list(data_positive_list)
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
    output_run.close()

    eval_dict = {}
    eval_list = []
    lines = input_eval.readlines()
    for line in tqdm(lines):
        items = line.split()
        qid = items[0]
        pid = items[2]
        if qid not in eval_list:
            eval_list.append(qid)
        if qid not in eval_dict:
            eval_dict[qid] = []
        if int(items[-1]) == 1:
            if qid in eval_dict:
                eval_dict[qid].append(pid)
            else:
                eval_dict[qid] = [pid]

    for qid in tqdm(eval_list):
        output_eval_file = os.path.join(DATA_dir, "input", qid + ".qrel")

        if qid in seed_dict:
            output_eval = open(output_eval_file, 'w')
            data_list = set(eval_dict[qid])
            seed_list = set(seed_dict[qid])
            id = qid

            for pid in seed_list:
                id = id + '_' + pid.strip()
            if len(data_list) != 0:
                output_eval_for_run.write(id + '\n')
                output_test_eval_run.write(id + '\n')
            removed_list = [x.strip() for x in data_list]
            for ppid in removed_list:
                output_eval.write(id + '\t' + 'Q0\t' + ppid + '\t' + '1' + '\n')
    output_eval_for_run.close()
else:
    for line in tqdm(lines):
        items = line.split()
        id = items[0]
        pid = int(items[2])
        if id in doc_dict:
            doc_dict[id].append(pid)
        else:
            doc_dict[id] = [pid]
    input_qrel.close()


    output_eval_set = set()
    total_num = 0
    for qid in tqdm(qid_list):
        data_positive_list = sorted(list(set(doc_positive_dict[qid])))

        data_list = doc_dict[qid]
        number = math.ceil(len(data_positive_list)*percentage)
        output_eval_file = os.path.join(DATA_dir, "input", str(qid) + ".qrel")
        output_eval = open(output_eval_file, 'w')

        subsets = []
        random.Random(random_seed).shuffle(data_positive_list)
        for i in range(0, len(data_positive_list)-1):
            subsets.append(data_positive_list[i:i+number])
        for positive_ids in subsets:
            id = qid + '_' + '_'.join([str(x).strip() for x in positive_ids])
            output_eval_set.add(id)
            output_quries.write(str(id) + '\n')
            removed_list = [str(x) for x in data_list if x != positive_ids]
            removed_positive_list = [str(x) for x in data_positive_list if x != positive_ids]
            for ppid in removed_positive_list:
                output_eval.write(str(id)+'\t' +'Q0\t' + str(ppid) + '\t' + '1' + '\n')

            removed_list = set(removed_list)
            removed_list = list(removed_list)
            new_dict = {
                'qid': id,
                'pid': removed_list
            }

            json.dump(new_dict, output_run)
            output_run.write('\n')
        output_eval.close()
    output_run.close()
    output_quries.close()

    for id in output_eval_set:
        output_eval_for_run.write(id + '\n')
    output_eval_for_run.close()

    test_eval_set = set()
    lines = input_test_eval.readlines()
    for line in tqdm(lines):
        items = line.split()
        #if int(items[-1]) ==1:
        qid = items[0]
            #pid = items[2]
        test_eval_set.add(qid)
    #
    for item in test_eval_set:
        output_test_eval_run.write(item+'\n')

