import re
from collections import Counter

WORD_LEN_TRESH =1


def words(text): return re.findall(r'\w+', text.lower(),re.UNICODE);


def filter_nowords(dictionary): return Counter(dict((filter(lambda x: len(x[0]) > WORD_LEN_TRESH, dictionary.items()))))


def load_words(filename): return filter_nowords(Counter(words(open(filename).read())))


def load_dictionary(filename):
    dictionary = set()
    import pandas as pd
    csv = pd.read_csv(filename, delimiter=";", names=['col1', 'col2', 'col3'], usecols=['col1', 'col2'])
    for word in csv['col1']:
        dictionary.add(word)
    for word in csv['col2']:
        dictionary.add(word)
    return Counter(dictionary)

WORDS = load_words("DUMP.txt")
DICTIONARY = load_dictionary("dict.txt")

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."

    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in DICTIONARY)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyząćęłńóśźż'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

data = open("wyrazy_poza_slownikiem-raw.txt").read()
words = data.split("\n")
results = open("corrections.txt","w+")
for word in words:
    result = correction(word)
    results.write(word + " => " + result + "\n")
    print(word + " => " + result)
results.close()


