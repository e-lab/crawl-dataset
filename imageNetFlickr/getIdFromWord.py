import csv
import sys
from nltk.corpus import wordnet as wn

def readCSV(fileName):
    names=[]
    with open(fileName,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['NAME']
            word = word.replace('\t','')
            word = word.replace(' ','')
            word = word.strip()
            names.append(word)
    return names

def writeCSV(array,dstFile):
    with open(dstFile,'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile,delimiter='\n')
        writer.writerow(array)

def getId(lists):
    ids = []
    for name in lists:
        try:
            ss = wn.synset(str(name)+'.n.01')
            wordid = ss.pos()+str(ss.offset())
            print(wordid)
            ids.append(wordid)
        except:
            print(name+' failed')
    return ids
#argv[1] will get name of files
lists = readCSV(sys.argv[1])
print(lists)
#Get ids from lists
ids = getId(lists)
#Writing to list csv
writeCSV(ids, sys.argv[2])
