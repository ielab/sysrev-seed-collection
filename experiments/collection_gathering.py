import json
import argparse
import time
import requests
from tqdm import tqdm
from Bio import Entrez
from bs4 import BeautifulSoup
import urllib.request
import ssl
import os
import math
import http.client
size = 2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#http.client.HTTPConnection._http_vsn = 10
#http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, required=True)
parser.add_argument("--email", type=str, required=True)
parser.add_argument("--output", type=str, required=True)
args = parser.parse_args()


input_filename = args.filename
output_path = args.output
email = args.email

Entrez.email = email
doc_id_list = []
with open(input_filename, 'r') as f:
    lines = f.readlines()
    for line in tqdm(lines):
        doc_id_list.append(line.strip())

if os.path.exists(output_path):
    output = open(output_path, 'r+')
    read_already_lines = output.readlines()
    print(len(read_already_lines))
    for line in tqdm(read_already_lines):
        current_dic = json.loads(line)
        current_pmid = current_dic['pmid']
        if current_pmid in doc_id_list:
            #print(current_pmid)
            doc_id_list.remove(current_pmid)
        else:
            print("not_appearing in list")
else:
    output = open(output_path, 'w')

for i in tqdm(range(0, math.ceil(len(doc_id_list)/1))):
    if i == math.ceil(len(doc_id_list)/1)-1:
        print(','.join(doc_id_list[i * 1:len(doc_id_list)]))
        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(doc_id_list[i * 1:len(doc_id_list)]), rettype='medline',
                                   retmode='text')
            record = handle.readlines()
        except:
            continue


    else:
        try:
            handle = Entrez.efetch(db="pubmed", id=','.join(doc_id_list[i*1:i*1+1]), rettype='medline', retmode='text')
            print(','.join(doc_id_list[i*1:i*1+1]))
            record = handle.readlines()
        except:
            continue
    previous = record[0][0:4]
    doc_id = None
    title_start = -10
    title_end = -10
    abstract_start = -10
    abstract_end = -10
    for line_index, line in enumerate(record):
        current = line[0:4]
        if current == 'PMID':
            doc_id = line.split()[-1].strip('\n')
            title_start = -10
            title_end = -10
            abstract_start = -10
            abstract_end = -10
        if current != previous:
            if current == 'TI  ':
                title_start = line_index
            if previous == 'TI  ':
                title_end = line_index
            if current == 'AB  ':
                abstract_start = line_index
            if previous == 'AB  ':
                abstract_end = line_index
        if current != "    ":
            previous = current
        record[line_index] = record[line_index].replace('\n', '')
        if '      ' in line:
            record[line_index] = record[line_index].replace('      ', '')
        if (line=='\n' and doc_id is not None) or (line_index==len(record)-1):
            if title_start == -10:
                title = ""
            else:
                title = ' '.join(record[title_start:title_end])[6:]
                if len(title) > 3:
                    if title[0] == '[' and title[-2] == ']':
                        title = title[1:-2]
            if abstract_start == -10:
                abstract = ""
            else:
                abstract = ' '.join(record[abstract_start:abstract_end])[6:]

            new_dic = {
                'pmid': doc_id,
                'title': title,
                'abstract': abstract
            }
            json.dump(new_dic, output)
            output.write("\n")


