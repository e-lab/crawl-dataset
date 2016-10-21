import csv
import sys
from os.path import join
from os.path import isdir
from subprocess import call
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
        writer = csv.writer(csvfile,delimiter='\n', lineterminator='\n')
        writer.writerow(array)

def getId(name):
    ids = []
    try:
        ss = wn.synset(str(name)+'.n.01')
        wordid = ss.pos()+str(ss.offset())
        print(wordid)
        ids.append(wordid)
    except:
        print(name+' failed')
    return ids
def checkFile(path):
    if not isdir(path):
        call(['mkdir','-p',path])
    else:
        print('{} exist'.format(path))
#argv[1] will get name of files
lists = readCSV(sys.argv[1])
dest = 'lists'
checkFile(dest)
print(lists)
for name in lists:
    destfile = join(dest,name+'.csv')
    #Get ids from lists
    ids = getId(name)
    #Writing to list csv
    writeCSV(ids, destfile)
