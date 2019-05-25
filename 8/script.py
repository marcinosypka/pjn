import json
import glob
import os
import re
import requests
import sys

from dateutil.parser import parse

def delete_html_tags(text): return re.sub(r'<[^>]*>','',text)
def get_json(text):
    return {"lpmn": "any2txt|wcrft2|liner2({\"model\":\"n82\"})",
            "text": text,
            "user": "moj@adres.mail"
           }
dataPath = '/home/marcin/Documents/AGH/PJN/data/json/2011/'
api_url = "http://ws.clarin-pl.eu/nlprest2/base/process"

print(os.path.exists(dataPath))

files = glob.glob(os.path.join(dataPath,'*.json'))

print("Starting process of named-entity recognition")
num = 0

for file in files:
    data = json.load(open(file))
    for item in data['items']:
        if item["id"] != 142540: continue
        if num == 100: exit(1)
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            num += 1
            with open("142540","w") as f:
                f.write(delete_html_tags(item['textContent']))
                exit()
            text = delete_html_tags(item['textContent'])
            sys.stdout.flush()
            response = requests.post(url=api_url,json=get_json(text))
            with open("{}.xml".format(item["id"]),"w+") as file:
                file.write(response.text);
            sys.stdout.write("\rProgress: {:5.2f} %".format(num))

