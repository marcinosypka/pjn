import glob
import os
import json
import shutil
import re

def delete_html_tags(text): return re.sub(r'<[^>]*>','',text)
def delete_broken_words(text): return re.sub(r'-\n','',text)

resultDir='/home/marcin/Documents/AGH/PJN/data/json/word2vec/new/'
if not os.path.exists(resultDir): os.mkdir(os.path.dirname(resultDir))

dataPath = '/home/marcin/Documents/AGH/PJN/data/json'
os.chdir(dataPath)
files = glob.glob('judgments*.json')

values = []

for file in files:
    if sum(os.path.getsize(f) for f in os.listdir(resultDir) if os.path.isfile(f)) > 1500000000: break;
    filename = file.split("/")[-1]
    shutil.copy(file,os.path.join(resultDir,filename))
        # data = json.load(open(file))
        # for item in data['items']:
        #     with open(os.path.join(resultDir,file.split("/")[-1:][0].split(".")[0] + item["source"]["judgmentId"] + ".txt"), "w+") as f:
        #         f.write(delete_html_tags(delete_broken_words(item['textContent'])))

# import os
# import random
# #res = sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))
# os.chdir(resultDir)
#
# while sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f)) > 1100000000:
#     files = os.listdir(".")
#     os.remove(files[random.randrange(0,len(files))])


