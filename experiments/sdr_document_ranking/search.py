from gensim.summarization import bm25
from gensim.models import KeyedVectors
from method.qlm import QLM
from method.aes import AES
from method.sdr_fullvec import SDR_full
import numpy
import argparse
import os
import json
from tqdm import tqdm
from os.path import dirname, abspath

# if you vector file is in binary format, change to binary=True


def load_weights(file):
    new_dict = {}
    with open(file) as f:
        for line in f:
            try:
                items = line.split()
                word = items[0]
                weight = float(items[1])
                new_dict[word] = weight
            except:
                continue
    return new_dict



def get_collection(collection_file):
    doc_dict = {}
    with open(collection_file) as f:
        for line in tqdm(f):
            datalist = json.loads(line)
            id = int(datalist["id"])
            content = datalist["contents"]
            doc_dict[id] = content
    return doc_dict


def build_bm25_model(result_dic):
    corpus = []
    pids = []
    for key in result_dic:
        pids.append(key)
        list_tokens = result_dic[key]
        corpus.append(list_tokens)
    #print(corpus)
    model = bm25.BM25(corpus)
    average_idf = sum(float(val) for val in model.idf.values()) / len(model.idf)
    return pids, model, average_idf

def build_qlm_model(result_dic, query_dic):
    corpus = []
    pids = []
    for key in result_dic:
        pids.append(key)
        list_tokens = result_dic[key]
        corpus.append(list_tokens)
    model = QLM(corpus, query_dic)
    return pids, model

def build_sdr_full_model(result_dic, query, query_dic):
    corpus = []
    pids = []
    overall_corpus = []
    overall_corpus.append(query)
    for key in result_dic:
        pids.append(key)
        list_tokens = result_dic[key]
        overall_corpus.append(' '.join(list_tokens))
        corpus.append(list_tokens)
    model = SDR_full(corpus, query_dic)
    return pids, model,overall_corpus

def build_aes_model(result_dic):
    corpus = []
    pids = []
    for key in result_dic:
        pids.append(key)
        list_tokens = result_dic[key]
        corpus.append(list_tokens)
    model = AES(corpus)
    return pids, model

def build_corpus_model(overall_dic):
    df = {}
    corpus_size = 0
    for key in overall_dic:
        list_tokens = overall_dic[key]
        for word in list_tokens:
            if word not in df:
                df[word] = 0
            df[word] += 1
            corpus_size += 1

    return df, corpus_size


def bm25_rerank_results(run_file, method, eval_file, collection_dic, data_dir, test_set, format, type):
    run_id_dict = {}
    if not os.path.exists(os.path.join(data_dir, "output", method)):
        os.mkdir(os.path.join(data_dir, "output", method))
    with open(run_file) as run:
        for line in tqdm(run):
            data_dict = json.loads(line)
            query_id = data_dict['qid']
            run_id_list = data_dict['pid']
            run_id_dict[query_id] = run_id_list

    with open(eval_file) as eval:
        for line in tqdm(eval):
            query_id = line.strip('\n')
            sys_id = query_id.split('_')[0]
            if format!='all':
                if sys_id not in test_set:
                    continue
            run_id_list = run_id_dict[query_id]
            actual_id = int(query_id.split('_')[-1])

            output_file = os.path.join(data_dir, "output", method, sys_id+'.trec')
            if os.path.exists(output_file):
                output = open(output_file, 'a+')
            else:
                output = open(output_file, 'w')

            if actual_id in collection_dic.keys():
                query_tokens = collection_dic[actual_id]
                result_dict = {}
                for id in run_id_list:
                    id = int(id)
                    if id in collection_dic.keys():
                        result_dict[id] = collection_dic[id]
                    else:
                        print(id, "run id not found")
                pids, model, average_idf = build_bm25_model(result_dict)
                scores = model.get_scores(query_tokens, average_idf)
                indices = sorted(range(len(scores)), key=lambda k: scores[k])[::-1]
                pid_sorted = [str(pids[i]) for i in indices]
                score_values = [scores[i] for i in indices]
                order_index = 1
                write_lines = []
                for pid_ordered in pid_sorted:
                    write_lines.append(query_id + ' Q0 ' + pid_ordered + ' ' + str(order_index) + ' ' + str(
                        score_values[order_index - 1]) + ' reranked\n')
                    order_index = order_index + 1
                output.writelines(write_lines)
            else:
                print(actual_id, "searching id not found")

def qlm_rerank_results(run_file, method, eval_file, collection_dic, data_dir, test_set, format, type):
    df_dic, corpus_size = build_corpus_model(collection_dic)
    run_id_dict = {}
    if not os.path.exists(os.path.join(data_dir, "output", method)):
        os.mkdir(os.path.join(data_dir, "output", method))
    with open(run_file) as run:
        for line in tqdm(run):
            data_dict = json.loads(line)
            query_id = data_dict['qid']
            run_id_list = data_dict['pid']
            run_id_dict[query_id] = run_id_list

    with open(eval_file) as eval:
        for line in tqdm(eval):
            query_id = line.strip('\n')
            sys_id = query_id.split('_')[0]
            if format != 'all':
                if sys_id not in test_set:
                    continue
            run_id_list = run_id_dict[query_id]
            actual_id = int(query_id.split('_')[-1])

            output_file = os.path.join(data_dir, "output", method, sys_id + '.trec')
            if os.path.exists(output_file):
                output = open(output_file, 'a+')
            else:
                output = open(output_file, 'w')

            if actual_id in collection_dic.keys():
                query_tokens = collection_dic[actual_id]
                query_dictionary = {}
                for word in query_tokens:
                    if word not in query_dictionary:
                        query_dictionary[word] = 0
                    query_dictionary[word] += 1
                result_dict = {}
                for id in run_id_list:
                    id = int(id)
                    if id in collection_dic.keys():
                        result_dict[id] = collection_dic[id]
                    else:
                        print(id, "run id not found")
                pids, model = build_qlm_model(result_dict, query_dictionary)
                if type == "original":
                    scores = model.get_scores(query_tokens, df_dic, corpus_size)
                else:
                    scores = model.get_scores(query_dictionary, df_dic, corpus_size)
                indices = sorted(range(len(scores)), key=lambda k: scores[k])[::-1]
                pid_sorted = [str(pids[i]) for i in indices]
                score_values = [scores[i] for i in indices]
                order_index = 1
                write_lines = []
                for pid_ordered in pid_sorted:
                    write_lines.append(query_id + ' Q0 ' + pid_ordered + ' ' + str(order_index) + ' ' + str(
                        score_values[order_index - 1]) + ' reranked\n')
                    order_index = order_index + 1
                output.writelines(write_lines)
            else:
                print(actual_id, "searching id not found")

def sdr_full_rerank_results(run_file, method, eval_file, collection_dic, data_dir, test_set, format, type):
    run_id_dict = {}
    if not os.path.exists(os.path.join(data_dir, "output", method)):
        os.mkdir(os.path.join(data_dir, "output", method))
    storing_dir = os.path.join(data_dir, "output", method, "stored_weights")
    if not os.path.exists(storing_dir):
        os.mkdir(storing_dir)
    with open(run_file) as run:
        for line in tqdm(run):
            data_dict = json.loads(line)
            query_id = data_dict['qid']
            run_id_list = data_dict['pid']
            run_id_dict[query_id] = run_id_list
    print(len(run_id_dict))
    with open(eval_file) as eval:
        for line_index, line in tqdm(enumerate(eval)):
            query_id = line.strip('\n')
            sys_id = query_id.split('_')[0]
            if format!='all':
                if sys_id not in test_set:
                    continue
            dic_file = os.path.join(storing_dir, sys_id+'.tsv')
            weight_dict = {}
            if os.path.exists(dic_file):
                weight_dict = load_weights(dic_file)
            run_id_list = run_id_dict[query_id]
            actual_id = int(query_id.split('_')[-1])
            output_file = os.path.join(data_dir, "output", method, sys_id + '.trec')
            if os.path.exists(output_file):
                output = open(output_file, 'a+')
            else:
                output = open(output_file, 'w')

            if actual_id in collection_dic.keys():
                query_tokens = collection_dic[actual_id]
                query_dictionary = {}
                for word in query_tokens:
                    if word not in query_dictionary:
                        query_dictionary[word] = 0
                    query_dictionary[word] += 1
                result_dict = {}
                for id in run_id_list:
                    id = int(id)
                    if id in collection_dic.keys():
                        result_dict[id] = collection_dic[id]
                    else:
                        print(id, "run id not found")
                pids, model, overall_corpus = build_sdr_full_model(result_dict, ' '.join(query_tokens), query_dictionary)
                if type == "original":
                    scores = model.get_scores(query_tokens, overall_corpus, weight_dict, sys_id, storing_dir)
                else:
                    scores = model.get_scores(query_dictionary, overall_corpus, weight_dict, sys_id, storing_dir)
                indices = sorted(range(len(scores)), key=lambda k: scores[k])[::-1]
                pid_sorted = [str(pids[i]) for i in indices]
                score_values = [scores[i] for i in indices]
                order_index = 1
                write_lines = []
                for pid_ordered in pid_sorted:
                    write_lines.append(query_id + ' Q0 ' + pid_ordered + ' ' + str(order_index) + ' ' + str(
                        score_values[order_index-1]) + ' reranked\n')
                    order_index = order_index + 1
                output.writelines(write_lines)
            else:
               print(actual_id, "searching id not found")

def aes_rerank_results(run_file, method, eval_file, collection_dic, data_dir, model, test_set, format):
    run_id_dict = {}
    if not os.path.exists(os.path.join(data_dir, "output", method)):
        os.mkdir(os.path.join(data_dir, "output", method))
    with open(run_file) as run:
        for line in tqdm(run):
            data_dict = json.loads(line)
            query_id = data_dict['qid']
            run_id_list = data_dict['pid']
            run_id_dict[query_id] = run_id_list
    with open(eval_file) as eval:
        for line_index, line in tqdm(enumerate(eval)):
            query_id = line.strip('\n')
            sys_id = query_id.split('_')[0]
            if format!='all':
                if sys_id not in test_set:
                    continue
            run_id_list = run_id_dict[query_id]
            actual_id = int(query_id.split('_')[-1])
            output_file = os.path.join(data_dir, "output", method, sys_id + '.trec')
            if os.path.exists(output_file):
                output = open(output_file, 'a+')
            else:
                output = open(output_file, 'w')

            if actual_id in collection_dic.keys():
                query_tokens = collection_dic[actual_id]
                query_vector = [numpy.average([model[w] for w in query_tokens if w in model], axis=0)]
                result_dict = {}
                for id in run_id_list:
                    id = int(id)
                    if id in collection_dic.keys():
                        collection_token = collection_dic[id]

                        pre_array = numpy.average([model[w] for w in collection_token if w in model], axis=0)
                        if not isinstance(pre_array, numpy.float64):
                            result_dict[id] = pre_array
                    else:
                        print(id, "run id not found")
                scores = []
                pids, model_corpus = build_aes_model(result_dict)
                scores = model_corpus.get_scores(query_vector)
                indices = sorted(range(len(scores)), key=lambda k: scores[k])
                #print(indices)
                pid_sorted = [str(pids[i]) for i in indices]
                score_values = [1-scores[i] for i in indices]
                #print(score_values)
                order_index = 1
                write_lines = []
                for pid_ordered in pid_sorted:
                    write_lines.append(query_id + ' Q0 ' + pid_ordered + ' ' + str(order_index) + ' ' + str(
                        score_values[order_index-1]) + ' reranked\n')
                    order_index = order_index + 1
                output.writelines(write_lines)
            else:
               print(actual_id, "searching id not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--DATA_DIR", type=str, default="run_search/single")
    parser.add_argument("--METHOD", type=str, required=True)
    parser.add_argument("--format", type=str, default='all')
    collection_base = dirname(dirname(os.path.abspath(__file__))) + '/'
    args = parser.parse_args()

    DATA_DIR = args.DATA_DIR
    method = args.METHOD
    format = args.format
    queries_file = os.path.join(DATA_DIR, "input", "queries.tsv")
    run_file = os.path.join(DATA_DIR, "input", "run.jsonl")
    eval_file = os.path.join(DATA_DIR,"input", "eval_id.tsv")
    test_file = os.path.join(DATA_DIR, "input", "eval_test_topic_id.tsv")

    if not os.path.exists(os.path.join(DATA_DIR, 'output')):
        os.mkdir(os.path.join(DATA_DIR, 'output'))

    test_set = set()
    test_lines =  open(test_file, 'r').readlines()
    for line in test_lines:
        test_set.add(line.strip('\n'))

    print("Start processing " + method)
    type = "new"
    if method=="BM25_BOW":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow.jsonl")
        collection_dict = get_collection(collection_file)
        bm25_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="BM25_BOW_LEE":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow_cased_lee.jsonl")
        collection_dict = get_collection(collection_file)
        bm25_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="BM25_BOC_WORD":
        collection_file = os.path.join(collection_base, "collection", "weighted1_boc_word.jsonl")
        collection_dict = get_collection(collection_file)
        bm25_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)

    if method=="QLM_BOW":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow.jsonl")
        collection_dict = get_collection(collection_file)
        qlm_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="QLM_BOW_LEE":
        type = "original"
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow_cased_lee.jsonl")
        collection_dict = get_collection(collection_file)
        qlm_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="QLM_BOC_WORD":
        collection_file = os.path.join(collection_base, "collection", "weighted1_boc_word.jsonl")
        collection_dict = get_collection(collection_file)
        qlm_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)

    if method=="SDR_BOW":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow.jsonl")
        collection_dict = get_collection(collection_file)
        sdr_full_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="SDR_BOC_FULL_WORD":
        collection_file = os.path.join(collection_base, "collection", "weighted1_boc_word.jsonl")
        collection_dict = get_collection(collection_file)
        sdr_full_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)
    if method=="SDR_BOW_FULL_LEE":
        type = "original"
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow_cased_lee.jsonl")
        collection_dict = get_collection(collection_file)
        sdr_full_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, test_set, format, type)

    if method=="AES_BOW":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow.jsonl")
        collection_dict = get_collection(collection_file)
        model = KeyedVectors.load_word2vec_format('/scratch/itee/uqswan37/Reproduce_SR/wikipedia-pubmed-and-PMC-w2v.bin', binary=True)
        aes_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, model, test_set, format)

    if method == "AES_BOW_P":
        collection_file = os.path.join(collection_base, "collection", "weighted1_bow.jsonl")
        collection_dict = get_collection(collection_file)
        model = KeyedVectors.load_word2vec_format('/scratch/itee/uqswan37/Reproduce_SR/PubMed-w2v.bin', binary=True)
        aes_rerank_results(run_file, method, eval_file, collection_dict, DATA_DIR, model, test_set, format)
