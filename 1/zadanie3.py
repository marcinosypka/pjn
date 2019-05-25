#
#Wynik działania skryptu znajduje się w pliku results3.txt
#
import json
import glob
import os
import re
from dateutil.parser import parse


resultsDir='/home/marcin/Documents/PJN/'
dataPath = '/home/marcin/Documents/PJN/data/json'
os.chdir(dataPath)
files = glob.glob('judgments*.json')
pattern=r"23 kwietnia 1964.*art. 445"
prog = re.compile(pattern, re.IGNORECASE)
counter=0
for file in files:
    data = json.load(open(file))
    for item in data['items']:
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            for refRegulation in item['referencedRegulations']:
                if refRegulation['journalYear'] == 1964:
                    match = prog.search(refRegulation['text'])
                    if(match):
                        counter += 1
results = open(resultsDir+"results3.txt","w+")
results.write(str(counter))
results.close()










