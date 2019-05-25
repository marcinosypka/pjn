import csv
import operator

csv =csv.reader(open("llr.txt"),delimiter="\t")


sortedlist = sorted(csv,key=operator.itemgetter(1))

file = open("llr-sorted.txt","w+")
for line in sortedlist:
    file.write("{}\n".format(line))
file.close()
