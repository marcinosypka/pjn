import json
import glob
import os
import re
from dateutil.parser import parse


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


dataPath = '/home/marcin/Documents/PJN/data/json/2011/'
text = '';
files = glob.glob(os.path.join(dataPath,"*.json"))
for file in files:
    data = json.load(open(file))
    for item in data['items']:
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            text += item['textContent']
file = open("DUMP.txt","w+")
file.write(preprocess_text(text))
file.close()

