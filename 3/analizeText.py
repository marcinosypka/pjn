from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

WORD_LEN_TRESH = 1
WORD_COUNT = 100


def words(text): return re.findall(r'\w+', text.lower(),re.UNICODE);


def filter_nowords(dictionary): return Counter(dict((filter(lambda x: len(x[0]) > WORD_LEN_TRESH, dictionary.items()))))


def top_values(dictionary, n): return Counter(dict(dictionary.most_common(n)));


def punkt4(dict):
    names = list(dict.keys())
    values = list(dict.values())
    sort = sorted(zip(values,names), reverse=True)
    y_axis = [i[0] for i in sort]
    x_axis = [index+1 for index, item in enumerate(sort)]

    print(x_axis)
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    rcParams.update({'font.size': 10})
    # tick_label does the some work as plt.xticks()
    #plt.figure(figsize=(WORD_COUNT/5,5))
    plt.tight_layout(2)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Pozycja w rankingu")
    plt.ylabel("Liczba wystąpień w tekstach")
    plt.plot(x_axis,y_axis)
    #plt.bar(range(len(dict)), y_axis, 0.5, tick_label=x_axis)
    #plt.yticks()
    #plt.xticks(rotation='vertical')
    plt.savefig("wykres.png")
    plt.show()


def punkt5_6(dict):
    #text = open("DUMP.txt").read();
    import pandas as pd
    csv = pd.read_csv("dict.txt", delimiter=";", names=['col1', 'col2', 'col3'], usecols=['col1', 'col2'])
    dictionary = set()
    for word in csv['col1']:
        dictionary.add(word.lower())
    for word in csv['col2']:
        dictionary.add(word.lower())
    results = dict.keys() - dictionary
    file = open("wyrazy_poza_slownikiem.txt","w+")
    file_raw = open("wyrazy_poza_slownikiem-raw.txt","w+")
    file.write("Ilosc wyrazów w dumpie: " + str(len(dict)) + "\n")
    file.write("Ilosc unikatowych wyrazów w słowniku: " + str(len(dictionary)) + "\n")
    file.write("Wyrazy nieznajdujące się w słowniku: \n\n")
    for word in results:
        file.write(word+'\n')
        file_raw.write(word+'\n')
    file.close()


text = open("DUMP.txt").read();
words = filter_nowords(Counter(words(text)))

punkt5_6(words)

# names = list(words.keys())
# values = list(words.values())
# sort = sorted(zip(values, names), reverse=True)
# file = open("wystapienia.txt","w+")
# for word in sort:
#     file.write(word[1] + ": " + str(word[0])+"\n")
# file.close()


