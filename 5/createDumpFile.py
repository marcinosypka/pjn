import json
import glob
import os
import re
from dateutil.parser import parse
import sys

def delete_html_tags(text): return re.sub(r'<[^>]*>','',text)


def delete_broken_words(text): return re.sub(r'-\n','',text)


def delete_words_with_numbers(text): return re.sub(r'\w*[0-9-_]+\w*','',text)


def preprocess_text(text) :
    return delete_words_with_numbers(
        delete_html_tags(
            delete_broken_words(
                text.lower()
            )
        )
    )


dataPath = '/home/marcin/Documents/AGH/PJN/data/json/2011/'

files = glob.glob(os.path.join(dataPath,"*.json"))
for file in files:

    filename = file.split('/').pop(9).split('.').pop(0)
    save_dir = "dump/"
    text = '';
    data = json.load(open(file))
    for item in data['items']:
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            text += item['textContent']
    file = open(save_dir+filename+".txt","w+")
    file.write(preprocess_text(text))
    file.close()

