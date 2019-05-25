#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.util import ngrams
from collections import Counter
from math import log2
import operator
import re

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

def words(text): return re.findall(r'\w+', text.lower(),re.UNICODE);


def P_BI(bigram):
    return BIGRAMS[bigram] / N_UNI


def P_UNI(unigram):
    return UNIGRAMS[unigram]/ N_UNI

def unigrams(words): return Counter(words)


def bigrams(words): return Counter(ngrams(words,2))

text = open("DUMP.txt").read();
#text = "Ala ma kota ma kota a kot ma ale i chuj"
print("text loaded")
W = words(text)
#W = [W[i] for i in range(10)]
print("text tokenized, number of tokens: {}".format(len(W)))
UNIGRAMS = unigrams(W)
N_UNI = sum(UNIGRAMS.values())
print("unigrams created,number of unigrams: {}".format(len(UNIGRAMS)))
BIGRAMS = bigrams(W)
N_BI = sum(BIGRAMS.values())
print("bigrams created, number of bigrams: {}".format(len(BIGRAMS)))

def calculate_pmi(bigram):
    #print("CALCULATING PMI:")
    pxy = P_BI(bigram)
    px = P_UNI(bigram[0])
    py = P_UNI(bigram[1])
    #print("P(XY):{:.2E} P(X):{:.2E} P(Y):{:.2E}".format(pxy,px,py))
    pmi = log2(pxy/(px*py));
   # print("CALCULATED PMI: {:f}".format(pmi))
   # print()
    return pmi

def punkt35():
    results = {}
    for bigram in BIGRAMS:
        ppm = calculate_pmi(bigram)
        results[bigram] = ppm;
    sorted_collection = sorted(results.items(),key=operator.itemgetter(1),reverse=True)
    results_file = open("pmi-filtered400.txt", "w+")
    results_file.write("BIGRAM\tPMI\tx\ty\txy\n")
    for bigram, ppm in sorted_collection:
        if BIGRAMS[bigram] > 400:
            results_file.write(bigram[0] + " " + bigram[1] + "\t{:f}\t{}\t{}\t{}\n"
                           .format(ppm,BIGRAMS[bigram],UNIGRAMS[bigram[0]],UNIGRAMS[bigram[1]]))
    results_file.close()
def H(elements):
    N = sum(elements)
    return -sum([k * log2(k/N + (k==0)) for k in elements])

def calcuate_llr(bigram):
    k_11 = P_BI(bigram)
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

def punkt67():
    results = {}
    for bigram in BIGRAMS:
        llr = calcuate_llr(bigram)
        results[bigram] = llr;
    sorted_collection = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    results_file = open("llr-filtered.txt","w+")
    results_file.write("BIGRAM\tLLR\n")
    for bigram, llr in sorted_collection:
        if BIGRAMS[bigram] > 50:
            results_file.write("{} {}\t{:f}\n".format(bigram[0], bigram[1], llr))
    results_file.close()



punkt35()
#punkt67()
