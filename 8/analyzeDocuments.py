import xml.etree.ElementTree as ET
import csv
import glob

writer = csv.writer(open("preprocessed.csv","w+"))
writer.writerow(["expresion","expression_base","class","class_general"])

files = glob.glob("files/*.xml")
for file in files:
    print(file)
    tree = ET.parse(file)
    root = tree.getroot()
    for sentence in root.findall("chunk/sentence"):
        expression = ""
        expression_base = ""
        category_split = ""
        category = sentence[0].find("ann")
        if category == None: continue
        category = category.get("chan")
        category_splitted = category.split("_")
        category_general = "{}_{}".format(category_splitted[0],category_splitted[1])
        for tok in sentence:
            ann = tok.find("ann")
            if ann == None: break
            if(ann.text == "1"):
                expression += tok[0].text + " "
                expression_base += tok[1][0].text + " "
        if(expression != ""):
            writer.writerow([expression,expression_base,category,category_general])