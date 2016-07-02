from __future__ import print_function
from subprocess import call
import nltk
import sys


from nltk.corpus import wordnet as wn
from nltk.tree import *

key = sys.argv[1] + '.n.01'

word = wn.synset(key)
hyp = lambda s:s.hyponyms()
tree = word.tree(hyp)

str = str(tree)
str = str.replace("Synset", "")
str = str.replace("(", "")
str = str.replace(")", "")
str = str.replace("'", "")
str = str.replace(",", "")
str = str.replace(" ", "")
list_char = list(str)

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
	call(["node", "app.js", word])


