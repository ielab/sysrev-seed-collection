import json
import argparse
from tqdm import tqdm
from gensim.utils import tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
cachedStopwords = set(tok.lower() for tok in stopwords.words("english"))
string_set =set(string.punctuation)
import os
size = 1000

parser = argparse.ArgumentParser()
parser.add_argument("--input_collection", type=str, default="collection/raw.jsonl")
parser.add_argument("--output_collection", type=str, default="collection/weighted")
parser.add_argument("--weight", type=int, default=1)
args = parser.parse_args()

input = args.input_collection
output = args.output_collection
weight = args.weight

doc_dic = {}
already_got_id = set()


with open(output+str(weight)+"_bow.jsonl", 'w') as file:
    with open(input) as jsonfile:
        for line_index, line in tqdm(enumerate(jsonfile)):
            data_list = json.loads(line)
            id = data_list["pmid"]
            if id in already_got_id or id=="null" or id is None:
                continue
            else:
                already_got_id.add(id)
                title = data_list["title"]
                content = data_list["abstract"]

                new_content = ""
                if title!="":
                    new_content += title*weight+" " + content
                else:
                    new_content = content
                for i in string_set:
                    new_content = new_content.replace(i, ' ')

                tokenised_list = list(tokenize(new_content))

                tokenised_removed = [tok.lower() for tok in tokenised_list if tok.lower() not in cachedStopwords]
                new_dic={
                    'id':   int(id),
                'contents': tokenised_list
                }

                json.dump(new_dic, file)
                file.write('\n')




