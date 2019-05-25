import argparse
import os
import json
import glob

from elasticsearch import Elasticsearch



headers = { "Content-Type": "application/json" }

parser = argparse.ArgumentParser(usage="Script for importing data to elasticsearch.")
parser.add_argument('input_json_dir', help='directory with json files to import')
parser.add_argument('url', help='elastic search url i.e. http://localhost:9200')
parser.add_argument('index_name', help='Name of elasticsearch index')
parser.add_argument('doc_type', help='Type of elastic search document')
args = parser.parse_args()
api_url = args.url

es = Elasticsearch(args.url)


input_json_dir = args.input_json_dir
if not os.path.isdir(input_json_dir):
    print("Given input_json_dir is not a directory !")
    exit(-1)

files = glob.glob(os.path.join(input_json_dir,"*.json"))
for file in files:
    data = json.load(open(file))
    for item in data['items']:
        res = es.index(index=args.index_name,doc_type=args.doc_type,body=item,id=item['id'])
        print('index ' + res['_index'] + ' type ' + res['_type'] + ' id: ' + res['_id'] + " " + res['result'])