import argparse
import os
import glob
from subprocess import Popen, PIPE, STDOUT

parser = argparse.ArgumentParser()
parser.add_argument("--DATA_DIR", type=str, default="run_snowballing/seed-search")
parser.add_argument("--METHOD", type=str, required=True)
parser.add_argument("--format", type=str, default="all")
parser.add_argument("--trec_eval", type = str, default="trec_eval/trec_eval")
parser.add_argument("--tar_eval", type = str, default="tar/scripts/tar_eval.py")
parser.add_argument("--evaluation_type", type=str, default="new")
args = parser.parse_args()

input_d = os.path.join(args.DATA_DIR, "input")
data_eval_file = os.path.join(args.DATA_DIR, "input", "eval.qrel")
data_test_eval_file = os.path.join(args.DATA_DIR, "input", "eval_test_topic_id.tsv")
data_output_dir = os.path.join(args.DATA_DIR, "output", args.METHOD)
eval_base_dir = os.path.join(args.DATA_DIR, "eval")
data_eval_dir = os.path.join(args.DATA_DIR, "eval", args.METHOD)
eval_type = args.evaluation_type
trec_eval = args.trec_eval
tar_eval = args.tar_eval

test_eval_list = []
data_test_eval = open(data_test_eval_file, 'r')
lines = data_test_eval.readlines()
for line in lines:
    test_eval_list.append(line.strip('\n'))

if not os.path.exists(eval_base_dir):
    os.mkdir(eval_base_dir)

if not os.path.exists(data_eval_dir):
    os.mkdir(data_eval_dir)


output_list= glob.glob(data_output_dir+"/*.trec")
qrel_list = glob.glob(input_d+"/*.qrel")
test_list = []
for q in qrel_list:
    output_qid = q.split('/')[-1].split('.')[0]
    if output_qid in test_eval_list:
        test_list.append(output_qid)

eval_dict = {}
eval_dict["recall_10"] = data_eval_dir + "/recall_10.res"
eval_dict["recall_100"] = data_eval_dir + "/recall_100.res"
eval_dict["recall_1000"] = data_eval_dir + "/recall_1000.res"
eval_dict["P_10"] = data_eval_dir + "/P_10.res"
eval_dict["P_100"] = data_eval_dir + "/P_100.res"
eval_dict["P_1000"] = data_eval_dir + "/P_1000.res"
eval_dict["map"] = data_eval_dir + "/map.res"
eval_dict["ndcg_cut_10"] = data_eval_dir + "/ndcg_cut_10.res"
eval_dict["ndcg_cut_100"] = data_eval_dir + "/ndcg_cut_100.res"
eval_dict["ndcg_cut_1000"] = data_eval_dir + "/ndcg_cut_1000.res"
eval_tar_dict = {}
eval_tar_dict["last_rel"] = data_eval_dir + "/last_rel.res"
eval_tar_dict["wss"] = data_eval_dir + "/wss.res"

for eval_r in eval_dict:
    ev_o = open(eval_dict[eval_r], 'w')
for eval_r in eval_tar_dict:
    ev_o = open(eval_tar_dict[eval_r], 'w')

if args.format=="all":
    result_dict = {}
    for output_file in output_list:
        output_file_qid = output_file.split('/')[-1].split('.')[0]
        command = trec_eval+" -m recall.10,100,1000 -m P.10,100,1000 -m map -m ndcg_cut.10,100,1000 " + ' ' + input_d +'/' +output_file_qid+'.qrel' + " " + output_file
        print(command)
        results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()

        if len(results) == 0:
            print(output_file_qid)
        for result in results:
            items = result.split()
            for k in eval_dict:
                if len(items)== 3 and items[0]==k:

                    current_output = open(eval_dict[k], 'a+')
                    current_output.write(output_file_qid + '\t' + k + '\t' + items[-1].strip('\n') + '\n')
                    if k in result_dict:
                        result_dict[k].append(float(items[-1]))
                    else:
                        result_dict[k] = [float(items[-1])]
        #print(result_list)
    if eval_type == "original":
        for k in result_dict:
            if k.split('_')[0]=="recall":
                print(k, (sum(result_dict[k])+(len(qrel_list)-len(result_dict[k]))) / len(qrel_list), len(result_dict[k]), len(qrel_list))
            else:
                print(k, sum(result_dict[k])/len(qrel_list), len(result_dict[k]), len(qrel_list))
    else:
        for k in result_dict:
            print(k, sum(result_dict[k])/len(result_dict[k]), len(result_dict[k]))


    last_eval = []
    wss = []
    for output_file in output_list:
        output_file_qid = output_file.split('/')[-1].split('.')[0]
        if output_file_qid == "CD009263":
            print(output_file_qid)
            continue
        command = tar_eval + " " +  input_d +'/' +output_file_qid+'.qrel' + " " + output_file
        results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
        #print(output_file, len(results))
        if results[0].split(':')[0]=="Skipping topic":
            continue
        for result in results:
            items = result.split('\t')
            if len(items)== 3 and items[0]=="ALL":
                if items[1] == "min_req":
                    last_eval.append(float(items[-1]))
                    current_output = open(eval_tar_dict["last_rel"], 'a+')
                    current_output.write(output_file_qid + '\t' + "last_rel" + '\t' + items[-1].strip('\n') + '\n')

                    #print(float(items[-1]))
                elif items[1]=='wss_100':
                    wss.append(float(items[-1]))
                    current_output = open(eval_tar_dict["wss"], 'a+')
                    current_output.write(output_file_qid + '\t' + "wss" + '\t' + items[-1].strip('\n') + '\n')
    #print(last_eval)
    #print(last_eval)
    if eval_type == "original":
        average_last_eval = (sum(last_eval)+ len(qrel_list)-len(last_eval)) / len(qrel_list)
        print("last_eval", average_last_eval,len(last_eval),len(qrel_list) )

    else:
        average_last_eval = sum(last_eval)/len(qrel_list)
        print("last_eval", average_last_eval)
    average_wss = (sum(wss)) / len(qrel_list)
    print("wss", average_wss, len(wss), len(qrel_list))

else:
    result_dict = {}
    over_all_set = set(test_eval_list)
    for output_file in output_list:
        output_qid = output_file.split('/')[-1].split('.')[0]

        #print(output_qid)
        if output_qid in test_eval_list:
            if output_qid == "CD009263":
                continue
            #print(test_eval_list)
            command = trec_eval+" -m recall.10,100,1000 -m P.10,100,1000 -m map -m ndcg_cut.10,100,1000 " + input_d +'/' +output_qid+'.qrel' + " " + output_file
            results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
            #print(output_qid, len(results))
            #print(results)
            if len(results)!= 0:
                over_all_set.remove(output_qid)
            for result in results:
                items = result.split()
                for k in eval_dict:
                    if len(items) == 3 and items[0] == k:
                        current_output = open(eval_dict[k], 'a+')
                        current_output.write(output_qid + '\t' + k + '\t' + items[-1].strip('\n') + '\n')
                        if k in result_dict:
                            result_dict[k].append(float(items[-1]))
                        else:
                            result_dict[k] = [float(items[-1])]
    if eval_type == "original":
        for k in result_dict:
            if k.split('_')[0]=="recall":
                print(k, (sum(result_dict[k])+(len(test_list)-len(result_dict[k]))) / len(test_list), len(result_dict[k]), len(test_list))
            else:
                print(k, sum(result_dict[k])/len(test_list), len(result_dict[k]), len(test_list))
    else:
        for k in result_dict:
            print(k, sum(result_dict[k])/len(result_dict[k]), len(result_dict[k]), len(test_list))
    print(', '.join(list(over_all_set)))

    over_all_set = set(test_eval_list)
    last_eval = []
    wss = []
    for output_file in output_list:
        output_qid = output_file.split('/')[-1].split('.')[0]
        if output_qid in test_eval_list:
            if output_qid == "CD009263":
                continue
            command = tar_eval +" " +   input_d +'/' +output_qid+'.qrel' + " " + output_file
            results = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True).stdout.readlines()
            if results[0].split(':')[0] == "Skipping topic":
                continue
            if len(results)!= 0:
                over_all_set.remove(output_qid)
            for result in results:
                items = result.split('\t')
                if len(items)== 3 and items[0]=="ALL":
                    if items[1] == "min_req":
                        last_eval.append(float(items[-1]))
                        current_output = open(eval_tar_dict["last_rel"], 'a+')
                        current_output.write(output_qid + '\t' + "last_rel" + '\t' + items[-1].strip('\n') + '\n')
                    elif items[1]=='wss_100':
                        wss.append(float(items[-1]))
                        current_output = open(eval_tar_dict["wss"], 'a+')
                        current_output.write(output_qid + '\t' + "wss" + '\t' + items[-1].strip('\n') + '\n')

    if eval_type == "original":
        average_last_eval = (sum(last_eval)+ len(test_list)-len(last_eval)) / len(test_list)
        print("last_eval", average_last_eval,len(last_eval), len(test_list))
    else:
        average_last_eval = sum(last_eval)/len(last_eval)
        print("last_rel", average_last_eval, len(last_eval), len(test_list))
    average_wss = sum(wss) / len(wss)
    print("wss", average_wss, len(wss), len(test_list))
    print(', '.join(list(over_all_set)))





