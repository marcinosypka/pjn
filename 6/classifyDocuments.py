import matplotlib.pyplot as plt
import pandas as pd
import json
import re
from glob import glob
import os
import csv
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support

stop_words_untagged = ["na","do","art","nie","że","przez","ust","się","dnia","jest","oraz","ustawy",
              "od","postępowania","sąd","nr","za","pkt","tym","to"]

stop_words_tagged = ["w","z","i","na","do","artykuł","nie","o","rok","że","on","przez",
              "ten","dzień","sąd","być","który","postępowanie","się","zamawiać"]


cywilne = re.compile(r"\bA?C.*\b")
ubezpieczenia = re.compile(r"\bA?U.*\b")
karne = re.compile(r"\bA?K.*\b")
gospodarcze = re.compile(r"\bG.*\b")
praca = re.compile(r"\bA?P.*\b")
rodzina = re.compile(r"\bR.*\b")
wykroczenia = re.compile(r"\bW.*\b")
konkurencja = re.compile(r"\bAm.*\b")

uzasadnienie = re.compile(r"(.*)(uzasadnienie)(.*)",re.IGNORECASE | re.DOTALL)

def get_pipeline(stop_words):
    return Pipeline(
    [
        ('tfidf', TfidfVectorizer(stop_words=stop_words)),
        ('clf', OneVsRestClassifier(LinearSVC())),
    ]

)

parameters = {
    'tfidf__max_df': (0.25, 0.5, 0.75),
    'tfidf__ngram_range': [(1, 1),(1, 2),(1, 3)],
    "clf__estimator__C": [0.01, 0.1, 1],
    "clf__estimator__class_weight": ['balanced', None],
}

# parameters = {
#     'tfidf__max_df': (0.5, 0.75),
#     'tfidf__ngram_range': [(1, 2)],
#     "clf__estimator__C": [1],
#     "clf__estimator__class_weight": ['balanced'],
# }

def words(text): return re.findall(r'\w+', text.lower(),re.UNICODE);


def categorize(courtCase):
    if cywilne.search(courtCase):
        return [1, 0, 0, 0, 0, 0, 0, 0]
    if ubezpieczenia.search(courtCase):
        return [0, 1, 0, 0, 0, 0, 0, 0]
    if karne.search(courtCase):
        return [0, 0, 1, 0, 0, 0, 0, 0]
    if gospodarcze.search(courtCase):
        return [0, 0, 0, 1, 0, 0, 0, 0]
    if praca.search(courtCase):
        return [0, 0, 0, 0, 1, 0, 0, 0]
    if rodzina.search(courtCase):
        return [0, 0, 0, 0, 0, 1, 0, 0]
    if wykroczenia.search(courtCase):
        return [0, 0, 0, 0, 0, 0, 1, 0]
    if konkurencja.search(courtCase):
        return [0, 0, 0, 0, 0, 0, 0, 1]


def delete_html_tags(text): return re.sub(r'<[^>]*>','',text)


def delete_broken_words(text): return re.sub(r'-\n','',text)


def delete_punctuation_marks(text): return re.sub(r'[.,-_]','',text)


def delete_words_with_numbers(text): return re.sub(r'\w*[0-9-_]+\w*','',text)


def preprocess_text(text):
    res1 = delete_broken_words(text)
    res2 = delete_html_tags(res1)
    res3 = delete_words_with_numbers(res2)
    res4 = delete_punctuation_marks(res3)
    return res4


def prepare_data(json_dir,preprocessed_csv,skipped_values_file, exclude_cases):
    os.makedirs(os.path.dirname(preprocessed_csv),exist_ok=True)
    os.makedirs(os.path.dirname(skipped_values_file),exist_ok=True)
    csv_file = open(preprocessed_csv,"w+")
    csvwriter = csv.writer(csv_file,delimiter="\t")
    csvwriter.writerow(
        ["textContent","cywilna","ubezpiecznie","karna","gospodarcza","praca","rodzina","wykroczenie","konkurencja"])
    files = glob(os.path.join(json_dir,"*.json"))
    skipped = open(skipped_values_file,"w+")
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file ! Aborting.")
            return
        data = json.load(open(file))
        for item in data['items']:

            if str(item['courtType']).lower() != "common" and str(item['courtType']).lower() != "supreme": continue
            results = uzasadnienie.match(item['textContent'])
            if set([item['courtCases'][0]['caseNumber']]) - exclude_cases == set():
                print("Case: {} excluded, skipping".format(item['courtCases'][0]['caseNumber']))
                skipped.write(item['courtCases'][0]['caseNumber'])
                skipped.write("\n")
                continue
            if not results:
                #print("Cannot find 'uzasadnienie' in case {}, skipping".format(item['courtCases'][0]['caseNumber']))
                skipped.write("{}\n".format(item['courtCases'][0]['caseNumber']))
                continue
            category_mask = categorize(item['courtCases'][0]['caseNumber'])
            if not category_mask:
               # print("Cannot categorize case: {}, skipping".format(item['courtCases'][0]['caseNumber']))
                skipped.write("{}\n".format(item['courtCases'][0]['caseNumber']))
                continue
            textContent = preprocess_text(results.group(3))
            row = [textContent] + category_mask
            csvwriter.writerow(row)
    skipped.close()
    csv_file.close()


def analyze_counts(data_file,chart_name):
    os.makedirs(os.path.dirname(chart_name),exist_ok=True)
    data_file.info()
    df_types = data_file.drop(["textContent"], axis=1)
    counts = []
    categories = list(df_types.columns.values)
    for category in categories:
        counts.append((category, df_types[category].sum()))
    df_stats = pd.DataFrame(counts, columns=["type","#cases"])
    df_stats.plot(x="type", y="#cases", kind="bar", legend=False, grid=True, figsize=(15, 8))
    plt.savefig(chart_name)


def train_classifier(data_file,stop_words):
    data_x = data_file[['textContent']].as_matrix()
    data_y = data_file.drop('textContent',axis=1).as_matrix()
    stratified_split = StratifiedShuffleSplit(n_splits=2, test_size=0.25)
    for train_index, test_index in stratified_split.split(data_x,data_y):
        x_train, x_test = data_x[train_index], data_x[test_index]
        y_train, y_test = data_y[train_index], data_y[test_index]

    train_x = [x[0].strip() for x in x_train.tolist()]
    test_x = [x[0].strip() for x in x_test.tolist()]

    grid_search_tune = GridSearchCV(get_pipeline(stop_words), parameters,cv=2, n_jobs=3, verbose=10)
    grid_search_tune.fit(train_x,y_train)
    print
    print("Best parameters set:")
    print(grid_search_tune.best_estimator_.steps)
    print
    print("Applying best classifier on test data:")
    best_clf = grid_search_tune.best_estimator_

    predictions = best_clf.predict(test_x)

    return y_test, predictions


def drop_columns(data_file,columns):
    for column in columns:
        data_file.drop(column,inplace=True,axis=1)
def get_word_count(df):
    text_array = df["textContent"].as_matrix()
    w = words(" ".join(text_array))
    return len(w)


def get_case_count(df):
    return df.shape[0]


def get_dropped_count(skipped_filename):
    with open(skipped_filename) as file:
        for i, l in enumerate(file):
            pass
    return i+1

def get_excluded_cases(excluded_filename):
    excluded = set()
    with open(excluded_filename) as file:
        for line in file:
            excluded.add(line.rstrip())
    return excluded

def generate_report(report_filename,test_y,predictions,word_count,case_count,drop_case_count,labels):
    os.makedirs(os.path.dirname(report_filename), exist_ok=True)
    micro = precision_recall_fscore_support(test_y,predictions,average='micro')
    macro = precision_recall_fscore_support(test_y,predictions,average='macro')
    report = open(report_filename, "a+")
    report.write("Cases: {}, dropped: {}\n".format(case_count, drop_case_count))
    report.write("Words: {}\n".format(word_count))
    report.write(classification_report(test_y, predictions, target_names=labels))
    report.write("\nMicro average:\n")
    report.write("{:>10s}\t{:>10s}\t{:>10s}\n".format("precision", "recall", "f1-score"))
    report.write("{:10.2f}\t{:10.2f}\t{:10.2f}\n\n".format(micro[0], micro[1], micro[2]))
    report.write("Macro average:\n")
    report.write("{:>10s}\t{:>10s}\t{:>10s}\n".format("precision", "recall", "f1-score"))
    report.write("{:10.2f}\t{:10.2f}\t{:10.2f}\n".format(macro[0], macro[1], macro[2]))
    report.close()


def classify_text(data_file, stop_words, skipped_filename, report_name):
    test_y, predictions = train_classifier(data_file,stop_words)
    categories = list(df.drop(["textContent"], axis=1).columns.values)
    words = get_word_count(df)
    cases = get_case_count(df)
    dropped = get_dropped_count(skipped_filename)
    generate_report(report_name,test_y,predictions,words,cases,dropped,categories)

def get_random_samples(list,number_of_samples):
    if len(list) < number_of_samples:
        number_of_samples = len(list)
    return random.sample(list,number_of_samples)


# excluded = get_excluded_cases("excluded.txt")
# prepare_data("judgements", "untagged-100random/preprocessed.csv", "untagged-100random/skipped.txt", excluded)
for i in range(10):
    df = pd.read_csv("untagged-100random/preprocessed-{}.csv".format(i), delimiter="\t")
    drop_columns(df, ["gospodarcza", "rodzina", "wykroczenie", "konkurencja"])
    classify_text(df, stop_words_tagged,"untagged-100random/skipped.txt","untagged-100random/results.txt")


#classify_text(excluded,stop_words_untagged,"judgements","untagged/preprocessed.csv","untagged/skipped.txt","untagged/results.txt","untagged/counts.png")
