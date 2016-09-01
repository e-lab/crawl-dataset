from nltk.corpus import wordnet as wn
from nltk.tree import *
import sys
import io

file = open('keywords.csv', 'w+')

for synset in list(wn.all_synsets('n')):
    if '01' in str(synset):
    	s = str(synset)
    	s = s.replace(".n.01","")
    	s = s.replace("'","")
    	s = s.replace("(","")
    	s = s.replace(")","")
    	s = s.replace("Synset","")
    	s = s.replace("_"," ")
    	file.write(s)
    	file.write("\n")

