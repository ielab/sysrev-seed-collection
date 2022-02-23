import json

input = input("Please input the topic id you want to search:")


retrieved_document_dict = {}
with open("collection_data/search/candidate_documents.res") as f:
    for line in f:
        items = line.split()
        id = items[0]
        did = items[2]
        if id not in retrieved_document_dict:
            retrieved_document_dict[id] = [did]
        else:
            retrieved_document_dict[id].append(did)

screened_snowballed_dict = {}
with open("collection_data/snowballing/screened_snowballing_candidates.tsv") as f:
    for line in f:
        items = line.split()
        id = items[0]
        dids = items[1].split('|')
        screened_snowballed_dict[id] = dids

seed_snowballed_dict = {}
with open("collection_data/snowballing/seed_snowballing_candidates.tsv") as f:
    for line in f:
        items = line.split()
        id = items[0]
        dids = items[1].split('|')
        seed_snowballed_dict[id] = dids

basic_infor_dict = {}
with open("collection_data/overall_collection.jsonl") as f:

    for line in f:
        dic = json.loads(line)
        id = dic['id']
        basic_infor_dict[id] = dic


print("Basic information: " + str(basic_infor_dict[input]))
print("Retrieved documents: " + str(retrieved_document_dict[id]))
print("Screened_snowballed document list: " + str(screened_snowballed_dict[id]))
print("Seed_snowballed document list: " + str(seed_snowballed_dict[id]))
