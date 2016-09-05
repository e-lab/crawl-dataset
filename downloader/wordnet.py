from __future__ import print_function
from subprocess import call
import nltk
import sys
import csv
import os
from os import path


from nltk.corpus import wordnet as wn
from nltk.tree import *

def ensure_dir(d):
        d = path.join(os.getcwd(),d)
        if not path.isdir(d):
            os.mkdir(d)

def getImage(query,root):
    path = root + '/' + query
    ensure_dir(path)

    key = query + '.n.01'

    word = wn.synset(key)
    hyp = lambda s:s.hyponyms()
    tree = word.tree(hyp)

    strTmp = str(tree)
    strTmp = strTmp.replace("Synset", "")
    strTmp = strTmp.replace("(", "")
    strTmp = strTmp.replace(")", "")
    strTmp = strTmp.replace("'", "")
    strTmp = strTmp.replace(",", "")
    strTmp = strTmp.replace(" ", "")
    list_char = list(strTmp)

    result = ""
    level = 0

    index = 0

    keywords = []

    #parse tree with a stack to get only 1st and 2nd levels
    while index < len(list_char):
            if list_char[index] == '[':
                    level += 1
                    index += 1
            elif list_char[index] == ']':
                    level -= 1
                    index +=1
            else:
                    if level <= 2:
                            while list_char[index] != '.':
                                    result += list_char[index]
                                    index += 1

                            while list_char[index] != '[' and list_char[index] != ']':
                                    index += 1

                            result = result.replace("_", " ")
                            keywords.append(result)
                            result = ""

                    else:
                            index +=1

    print(keywords)
    for word in keywords:
        try:
            if not query in word:
                word = word + ' ' + query
            call(["node", "app.js", word, path])
        except:
            print('Failed')

def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        names = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row['NAME'])
    return names

csvFile = sys.argv[1]
ensure_dir("images")
names = readCSV(csvFile)
for name in names:
    try:
        getImage(name,"images")
    except:
        print(str(name)+' Failed ')
