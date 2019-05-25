from collections import Counter
import glob
import os
import re
from math import log2
import pandas as pd
from nltk.util import ngrams
import csv

def unigrams(words): return Counter(words)

def bigrams(words): return Counter(ngrams(words,2))

def H(elements):
    N = sum(elements)
    return -sum([k * log2(k/N + (k==0)) for k in elements])

def calcuate_llr(bigram, BIGRAMS,UNIGRAMS, N_BI, N_UNI):
    k_11 = BIGRAMS[bigram] / N_UNI
    px = UNIGRAMS[bigram[0]]/N_BI
    py = UNIGRAMS[bigram[1]]/N_BI
    k_22 =  1 - (px+py-k_11)
    k_21 = px-k_11
    k_12 = py - k_11
    sumOfEvents = k_11+k_12+k_21+k_22;
    H_all = H((k_11,k_12,k_21,k_22))
    H_rows = H((k_11+k_12,k_21+k_22))
    H_cols = H((k_11+k_21,k_12+k_22))
    llr =  2*sumOfEvents * (H_rows + H_cols - H_all)
    return llr;

dataPath = 'dump/'
regexp = re.compile("\w+")
files = glob.glob(os.path.join(dataPath,"*.txt"))
WORDS = []
WORDS2 = []
i = 0
grammarClasses=set(["subst", "depr", "num", "numcol", "adj", "ppron12", "ppron3", "siebie", "ger", "pact", "ppas", "prep"])
for file in files:
    print("reading csv file: " + file)
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        print("file read, getting words from csv")
        for row in reader:
            if len(row) < 3: continue
            word = str(row[1]).lower()
            if regexp.match(word):
                grammarClass = str(row[2]).split(":").pop(0)
                word = word+":"+grammarClass
                WORDS.append(word)
                if(set([grammarClass]) & grammarClasses != set()):
                    WORDS2.append(word)
print("creating unigrams 1")
UNIGRAMS1 = unigrams(WORDS)
N_UNI1 = sum(UNIGRAMS1.values())
print("creating bigrams 1")
BIGRAMS1 = bigrams(WORDS)
N_BI1 = sum(BIGRAMS1.values())

print("creating unigrams 2")
UNIGRAMS2  = unigrams(WORDS2)
N_UNI2 = sum(UNIGRAMS2.values())
print("creating bigrams 2")
BIGRAMS2 = bigrams(WORDS2)
N_BI2 = sum(BIGRAMS2.values())

print("saving results1 to files")
big1 = open("bigrams1.txt","w+")
llr1 = open("llr1.txt","w+")
results = open("results.txt","w+")
for bigram in BIGRAMS1.most_common():
    big1.write("{}\t{}\n".format(bigram[0], bigram[1]))
    llr = calcuate_llr(bigram[0],BIGRAMS1, UNIGRAMS1, N_BI1, N_UNI1)
    llr1.write("{}\t{}\n".format(bigram[0], llr))
    left = bigram[0][0].split(":").pop(1).split("'").pop(0)
    right = bigram[0][1].split(":").pop(1).split("'").pop(0)
    if(left == "subst") and ((right == "subst") or (right == "adj")):
        results.write("{}\t{}\n".format(bigram[0], llr))
llr1.close()
big1.close()
results.close()

print("saving results2 to file")
big2 = open("bigrams2.txt","w+")
llr2 = open("llr2.txt","w+")
for bigram in BIGRAMS2.most_common():
    big2.write("{}\t{}\n".format(bigram[0], bigram[1]))
    llr = calcuate_llr(bigram[0],BIGRAMS2, UNIGRAMS2, N_BI2, N_UNI2)
    llr2.write("{}\t{}\n".format(bigram[0], llr))
llr2.close()
big2.close()