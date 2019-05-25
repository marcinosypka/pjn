import glob
import os
import json
import pprint
import codecs
import re
import requests
import sys

def delete_html_tags(text): return re.sub(r'<[^>]*>','',text)
def delete_broken_words(text): return re.sub(r'-\n','',text)
def delete_words_with_numbers(text): return re.sub(r'\w*[0-9-_]+\w*','',text)


def tagText(text):
    response = requests.post("http://localhost:9200",text)
    return response.text

def preprocess_text(text) :
    return delete_html_tags(
            delete_broken_words(
                text.lower()
            ))

judgements_dir = "/home/marcin/PycharmProjects/PJN/6/judgements/"
judgements_tagged_dir = "/home/marcin/PycharmProjects/PJN/6/judgements-tagged/"

files = glob.glob(os.path.join(judgements_dir,"*.json"))
files_tagged = glob.glob(os.path.join(judgements_tagged_dir,"*.json"))

filenames =set()
filenames_tagged = set()

for file in files: filenames.add(os.path.split(file)[1])
for file in files_tagged: filenames_tagged.add(os.path.split(file)[1])

files_not_tagged = filenames - filenames_tagged
files_not_tagged = list(map(lambda x: os.path.join(judgements_dir,x),files_not_tagged))
num_of_files = len(files_not_tagged)

print("Starting tagging files")
for index,file in enumerate(files_not_tagged):
    json_data = json.load(open(file, "r", encoding="utf-8"))
    items = json_data['items']
    num_of_items = len(items)
    for i,item in enumerate(items):
        item['textContent'] = tagText(preprocess_text(item['textContent']).encode('utf-8'))
        sys.stdout.write("\rtagging file: {}, progress: {:5.2f} %".format(file,((i+1)/num_of_items)*100))
        sys.stdout.flush()
    path, filename = os.path.split(file)
    with open(os.path.join(judgements_tagged_dir, filename), "w+", encoding="utf-8") as output_file:
        output_file.write(json.dumps(json_data, ensure_ascii=False))
    print("\noverall progress: {:5.2f} %".format((index+1)/num_of_files*100))

os.system("shutdown")