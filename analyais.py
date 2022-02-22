import json

with open("collection_data/overall_collection.jsonl") as f:
    line = f.readline()
    dic = json.loads(line)
    print(dic.keys())