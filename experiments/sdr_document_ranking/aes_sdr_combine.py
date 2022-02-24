import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT
from tqdm import tqdm
parser = argparse.ArgumentParser()
parser.add_argument("--DATA_DIR", type=str, default="run_search/single")
parser.add_argument("--AES_METHOD", type=str, default="AES_BOW")
parser.add_argument("--SDR_METHOD", type=str, default="SDR_BOW")
parser.add_argument("--COM_METHOD", type=str, default="SDR_BOW_AES")
parser.add_argument("--ALPHA", type=float, default=0.3)
args = parser.parse_args()

input_d = os.path.join(args.DATA_DIR, "input")
data_eval_file = os.path.join(args.DATA_DIR, "input", "eval.qrel")
data_test_eval_file = os.path.join(args.DATA_DIR, "input", "eval_test_topic_id.tsv")
alpha = args.ALPHA

data_output_dir_aes = os.path.join(args.DATA_DIR, "output", args.AES_METHOD)
data_output_dir_sdr = os.path.join(args.DATA_DIR, "output", args.SDR_METHOD)
data_output_dir = os.path.join(args.DATA_DIR, "output",args.COM_METHOD)

if not os.path.exists(data_output_dir):
    os.mkdir(data_output_dir)


output_list_aes= glob.glob(data_output_dir_aes+"/*.trec")
#output_list_sdr= glob.glob(data_output_dir_sdr+"/*.trec")


for output_file_aes in tqdm(output_list_aes):
    output_file_qid = output_file_aes.split('/')[-1].split('.')[0]
    output_file_sdr = data_output_dir_sdr + '/' + output_file_qid + '.trec'
    output_file_combined = data_output_dir+ '/' + output_file_qid + '.trec'
    output_aes = open(output_file_aes, 'r')
    output_sdr = open(output_file_sdr, 'r')
    output_combined = open(output_file_combined, 'w')
    aes_dict = {}
    sdr_dict = {}

    lines = output_aes.readlines()
    for line in lines:
        items = line.split()
        qid = items[0]
        pid = items[2]
        score = float(items[-2])
        if qid not in aes_dict:
            aes_dict[qid] = {}
            aes_dict[qid][pid] = score
        else:
            aes_dict[qid][pid] = score
    lines = output_sdr.readlines()
    for line in lines:
        items = line.split()
        qid = items[0]
        pid = items[2]
        score = float(items[-2])
        if qid not in sdr_dict:
            sdr_dict[qid] = {}
            sdr_dict[qid][pid] = score
        else:
            sdr_dict[qid][pid] = score

    for qid in aes_dict:
        current_dict = aes_dict[qid]
        minimum = min(current_dict.values())
        maximum = max(current_dict.values())
        if maximum==minimum:
            for pid in current_dict:
                current_dict[pid] = 0
        else:
            for pid in current_dict:
                current_dict[pid] = (current_dict[pid]-minimum)/(maximum-minimum)
        aes_dict[qid] = current_dict

    for qid in sdr_dict:
        current_dict = sdr_dict[qid]
        minimum = min(current_dict.values())
        maximum = max(current_dict.values())
        if maximum==minimum:
            for pid in current_dict:
                current_dict[pid] = 0
        else:
            for pid in current_dict:
                current_dict[pid] = (current_dict[pid]-minimum)/(maximum-minimum)
        sdr_dict[qid] = current_dict

    for qid in aes_dict:
        combined_dict = {}
        aes_data = aes_dict[qid]
        sdr_data = sdr_dict[qid]
        for pid in aes_data:
            combined_dict[pid] = (sdr_data[pid]*alpha) + ((1-alpha)*aes_data[pid])
        sort_orders = sorted(combined_dict.items(), key=lambda x: x[1], reverse=True)
        for index, i in enumerate(sort_orders):
            output_combined.write(qid+' Q0 ' + i[0] + ' ' + str(index+1) + ' ' + str(i[1]) + ' combined\n')






