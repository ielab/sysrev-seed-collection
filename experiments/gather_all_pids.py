import json
import argparse
from tqdm import tqdm
import os

from os.path import dirname, abspath
parser = argparse.ArgumentParser()
parser.add_argument("--snowballing_candidates", type=str, default="snowballing/seed_snowballing_candidates.tsv+snowballing/screened_snowballing_candidates.tsv" )
parser.add_argument("--search_candidates", type=str, default="search/candidate_documents.res")
parser.add_argument("--original_collection", type=str, default="overall_collection.jsonl")
parser.add_argument("--output_dir", type=str, default="collection/pid_dir/")
parser.add_argument("--chunks", type=int, default=1)
args = parser.parse_args()

base_dir = dirname(dirname(os.path.abspath(__file__))) + '/collection_data/'

snowballing_candidates =  args.snowballing_candidates.split("+")
print(snowballing_candidates)
search_candidates = args.search_candidates
output_path = args.output_dir
chunks = args.chunks

doc_id_set = set()
ra = args.original_collection

with open(base_dir + ra) as f:
    for line in f:
        current_dict = json.loads(line)
        id = current_dict["id"]
        seeds = current_dict["seed_studies"]
        included = current_dict["included_studies"]
        doc_id_set.update(set(included))
        doc_id_set.update(set(seeds))

for input_file in tqdm(snowballing_candidates):
    print("snowballing_file: " + input_file)
    with open(base_dir + input_file) as f:
        lines = f.readlines()
        for line in lines:
            id_list = set([x.strip() for x in line.split()[1].split('|')])
            doc_id_set.update(id_list)
    print(len(doc_id_set))

with open(base_dir+ search_candidates) as f:
    for line in f:
        items = line.split()
        doc_id_set.add(items[2])

if not os.path.exists(output_path):
    os.mkdir(output_path)
doc_id_list = list(doc_id_set)
num = int(len(doc_id_list)/chunks)+1

for i in range(0,chunks):
    output = open(output_path+str(i)+'.txt', 'w')
    current_list = doc_id_list[i*num: i*num+num]
    if i==chunks-1:
        current_list = doc_id_list[i * num: len(doc_id_list)]
    for item in current_list:
        output.write(item+'\n')










