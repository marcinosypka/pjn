from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

csv = pd.read_csv("preprocessed.csv")
counter = Counter(csv["class"])
class_general_counter = Counter(csv["class_general"])

def drawBarGraph(x,y,figname):
    rcParams.update({'figure.autolayout': True})
    rcParams.update({'font.size': 10})
    plt.tight_layout(2)
    plt.xlabel("klasa")
    plt.ylabel("ilość")
    plt.xticks(rotation='vertical')
    plt.bar(x,y)
    plt.savefig(figname)
    plt.close()

x_all = []
y_all = []


for element in counter.most_common():
    x_all.append(element[0])
    y_all.append(element[1])


x_small = x_all[5:]
y_small = y_all[5:]
# drawBarGraph(x_all,y_all,"all_classes.png")
# drawBarGraph(x_small,y_small,"minor_classes.png")

x = []
y = []
for element in class_general_counter.most_common():
    x.append(element[0])
    y.append(element[1])
#drawBarGraph(x,y,"II/all_classes.png")

# most_popular_expressions = Counter(zip(csv["expresion"],csv["class_general"]))
# most_popular_expressions_base = Counter(zip(csv["expression_base"],csv["class_general"]))
#
# with open("100_most_common.txt","w") as file:
#     file.write("expression\tclass\tcount\n")
#     for expression in most_popular_expressions.most_common(100):
#         file.write("{}\t{}\t{}\n".format(expression[0][0],expression[0][1],expression[1]))
#
# with open("100_most_common_base.txt","w") as file:
#     file.write("expression_base\tclass\tcount\n")
#     for expression in most_popular_expressions_base.most_common(100):
#         file.write("{}\t{}\t{}\n".format(expression[0][0],expression[0][1],expression[1]))


classes = set(csv["class_general"])
top10 = open("top10.txt","w")
top10base = open("top10_base.txt","w")
for general_class in classes:
    general_class_counter = Counter(csv[csv["class_general"] == general_class]["expresion"])
    general_class_base_counter = Counter(csv[csv["class_general"] == general_class]["expression_base"])
    top10.write("##########  {}  ##########\n".format(general_class))
    top10base.write("##########  {}  ##########\n".format(general_class))
    for expression in general_class_counter.most_common(10):
        top10.write("{}:{}\n".format(expression[0],expression[1]))
    for expression in general_class_base_counter.most_common(10):
        top10base.write("{}:{}\n".format(expression[0],expression[1]))
top10.close()
top10base.close()