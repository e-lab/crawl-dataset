import os
import sys

f = open('keywords.csv', 'w+')

for file in os.listdir("/media/HDD1/spk/256_ObjectCategories"):
	if file != '.DS_Store':
	    s = str(file)
	    s = s.split('.', 1)[-1]
	    f.write(s)
	    f.write('\n')