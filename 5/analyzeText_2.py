from collections import Counter
import glob
import os
import re
from math import log2
from nltk.util import ngrams
import csv
import sys

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
num_of_files = len(files)
print("reading files")
sys.stdout.write("\rProgress: {:5.2f} %".format(0))
sys.stdout.flush()
for i, file in enumerate(files):
    with open(file) as csvfile:
        reader = csv.reader(csvfile,delimiter="\t")
        for row in reader:
            if len(row) < 3: continue
            word = str(row[1]).lower()
            grammarClass = str(row[2]).split(":").pop(0)
            if regexp.match(word):
                word = word+":"+grammarClass
                WORDS.append(word)
    sys.stdout.write("\rProgress: {:5.2f} %".format((i+1)/num_of_files*100))
    sys.stdout.flush()

print("\ncreating unigrams")
UNIGRAMS1 = unigrams(WORDS)
N_UNI1 = sum(UNIGRAMS1.values())

print("creating bigrams")
BIGRAMS1 = bigrams(WORDS)
N_BI1 = sum(BIGRAMS1.values())

print("saving results to file")
result = open("result.txt","w+")
for bigram in BIGRAMS1.most_common():
    llr = calcuate_llr(bigram[0],BIGRAMS1, UNIGRAMS1, N_BI1, N_UNI1)
    left = bigram[0][0].split(":").pop(1).split("'").pop(0)
    right = bigram[0][1].split(":").pop(1).split("'").pop(0)
    if(left == "subst") and ((right == "subst") or (right == "adj")):
        result.write("{}\t{}\n".format(bigram[0], llr))
result.close()

