#
#Wynik działania skryptu znajduje się w plikach:
# histogram_all.png - histogram przedstawiający rozkład wszystkich danych
# histogram_belowMillion.png - histogram przedstawiający rozkład danych, których wartość nie przekraczała 1 mln zł
# histogram_aboveMillion.png - histogram przedstawiający rozkład danych, których wartość była wyższa lub równa 1 mln zł
# histogramy opatrzone są komentarzem znajdującym się w pliku histogramy-komentarz.txt
#
import json
import glob
import os
import re
from dateutil.parser import parse
import matplotlib.pyplot as plot

resultsDir='/home/marcin/Documents/PJN/'
dataPath = '/home/marcin/Documents/PJN/data/json'
os.chdir(dataPath)
files = glob.glob('judgments*.json')
pattern=r"(([1-9])((\d{0,2}([,\. ]\d{3})*)|(\d*))([,.]\d{2})? ?(zł|pln|złotych|złote))"
prog = re.compile(pattern, re.IGNORECASE)
values = []
for file in files:
    data = json.load(open(file))
    for item in data['items']:
        date = parse(item['judgmentDate'])
        if date.year == 2011:
            matches = prog.findall(item['textContent'])
            for match in matches:
                normalizedValue = match[1]+re.sub(r'[,\. ]','',match[2])+re.sub(r',','.',match[6])
                values.append(normalizedValue)
results = open("results.txt",'w+')
for value in values:
    results.write(value+'\n')
results.close()
numbers = [float(i) for i in values]
aboveMillion = []
belowMillion = []
for number in numbers:
    if number >= 1000000:
        aboveMillion.append(number)
    else:
        belowMillion.append(number)
names=["histogram_all.png","histogram_belowMillion.png","histogram_aboveMillion.png"]
for i,dataSet in enumerate([numbers,belowMillion,aboveMillion]):
    plot.hist(dataSet, log=True)
    plot.xlabel("Przedział")
    plot.ylabel("Częstotliwość wystąpień")
    plot.savefig(resultsDir + names[i])
    plot.close()
