import json
import argparse
from tqdm import tqdm
import os

parser = argparse.ArgumentParser()
parser.add_argument("--filenames", nargs='+', type=str, required=True)
parser.add_argument("--original_collection", type=str, default="data/seed_and_included.jsonl")
parser.add_argument("--output_dir", type=str, default="collection/pid_dir/")
parser.add_argument("--chunks", type=int, default=1)
args = parser.parse_args()


input_filenames = args.filenames
output_path = args.output_dir
chunks = args.chunks

doc_id_set = set()
ra = args.original_collection

with open(ra) as f:
    for line in f:
        current_dict = json.loads(line)
        id = current_dict["id"]
        seeds = current_dict["seed_studies"]
        included = current_dict["included_studies"]
        doc_id_set.update(set(included))
        doc_id_set.update(set(seeds))

for input_file in tqdm(input_filenames):
    print(input_file)
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            doc_id_set.add(line.split()[2].strip())
    print(len(doc_id_set))

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










