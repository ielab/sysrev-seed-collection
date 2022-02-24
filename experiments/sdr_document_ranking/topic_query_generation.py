import json
import argparse
from tqdm import tqdm
import os
size = 1000

parser = argparse.ArgumentParser()
parser.add_argument("--input_json", type=str, default="data/seed_and_included.jsonl")
parser.add_argument("--input_qrel", type=str, default ="data/qrels/search_based/sr_collection.qrels")
parser.add_argument("--DATA_DIR", type=str, default="run_search/single")
args = parser.parse_args()

input_qrel_file = args.input_qrel
input_json_file = args.input_json
input_eval_file = args.input_qrel
input_test_eval_file = args.input_qrel
output_queries_file = os.path.join(args.DATA_DIR, "input", "queries.tsv")
output_run_fie = os.path.join(args.DATA_DIR, "input", "run.jsonl")
output_eval_file_run = os.path.join(args.DATA_DIR, "input", "eval_id.tsv")
output_test_eval_file_run = os.path.join(args.DATA_DIR, "input", "eval_test_topic_id.tsv")

input_json = open(input_json_file, 'r')
input_qrel = open(input_qrel_file, 'r')
input_eval = open(input_eval_file, 'r')
input_test_eval = open(input_test_eval_file, 'r')
output_quries = open(output_queries_file, 'w')
#output_eval = open(output_eval_file, 'w')
output_test_eval_run = open(output_test_eval_file_run, 'w')
output_eval_for_run = open(output_eval_file_run, 'w')
output_run = open(output_run_fie, 'w')


doc_dict = {}
qid_list = []

doc_positive_dict = {}
lines = input_json.readlines()


for line in lines:
    current_dict = json.loads(line)
    id = current_dict['id']
    doc_positive_dict[id] = current_dict["included_studies"]
    qid_list.append(id)
input_json.close()


lines = input_qrel.readlines()

for line in tqdm(lines):
    items = line.split()
    if items[0] in doc_dict:
        doc_dict[items[0]].append(items[2])
    else:
        doc_dict[items[0]] = [items[2]]

input_qrel.close()
# output_quries.close()

for qid in tqdm(qid_list):
    data_positive_list = set(doc_positive_dict[qid])
    data_positive_list = list(data_positive_list)
    data_list = doc_dict[qid]
    print(qid, len(data_list), len(data_positive_list))
    for positive_id in data_positive_list:
        id = qid + '_' + positive_id
        removed_list = [x for x in data_list if x != positive_id]
        removed_list = set(removed_list)
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
    if int(items[-1]) ==1:
        if qid in eval_dict:
            eval_dict[qid].append(pid)
        else:
            eval_dict[qid] = [pid]


test_eval_set = set()
lines = input_test_eval.readlines()
for line in tqdm(lines):
    items = line.split()
    qid = items[0]
    test_eval_set.add(qid)

for item in test_eval_set:
    output_test_eval_run.write(item+'\n')

for qid in tqdm(eval_list):
    output_eval_file = os.path.join(args.DATA_DIR, "input", qid+".qrel")
    output_eval = open(output_eval_file, 'w')
    data_list = set(eval_dict[qid])
    for pid in data_list:
        id = qid + '_' + pid
        removed_list = [x for x in data_list if x != pid]
        for ppid in removed_list:
            output_eval.write(id+'\t' +'Q0\t' + ppid + '\t' + '1' + '\n')

        output_eval_for_run.write(id+'\n')

output_eval_for_run.close()
