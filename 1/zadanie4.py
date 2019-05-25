#
#Wynik działania skryptu znajduje się w pliku results4.txt
#

import json
import glob
import os
import re
from dateutil.parser import parse


resultsDir='/home/marcin/Documents/PJN/'
dataPath = '/home/marcin/Documents/PJN/data/json/2011/'
os.chdir(dataPath)
files = glob.glob('judgments*.json')
pattern=r'\b(szkod(a|ą|ę|om|y|zie|ach|ami)|szkód)\b'
prog = re.compile(pattern, re.IGNORECASE)
counter=0
matches = []
files = glob.glob(dataPath + "*.json")
for file in files:
    data = json.load(open(file))
    for item in data['items']:
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            match = prog.search(item['textContent'])
            if match:
                matches.append(match.group())
                counter+=1
#print(set(matches))
print(counter)









