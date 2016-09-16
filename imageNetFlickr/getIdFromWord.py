import csv
import sys
from nltk.corpus import wordnet as wn

def readCSV(fileName):
    names=[]
    with open(fileName,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row['NAME'])
    return names
def writeCSV(array,dstFile):
    with open(dstFile,'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile,delimiter='\n')
        writer.writerow(array)

#argv[1] will get name of files
lists = readCSV(sys.argv[1])
#Writing to list csv
writeCSV(lists, sys.argv[2])

for name in lists:
    ss = wn.synset(str(name)+'.n.01')
    wordid = ss.pos()+str(ss.offset())
    print(wordid)
