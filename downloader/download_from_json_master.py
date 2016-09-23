from os import listdir
from os.path import isfile, join
import sys
from subprocess import call

path = sys.argv[1]

for d in listdir(path):
	if d[0] != ".":
		print("In directory " + d)
		classpath = path + '/' + d
		destclasspath = './images/' + d
		onlyfiles = [f for f in listdir(classpath) if isfile(join(classpath, f))]
		for query in onlyfiles:
			print("query:" + query)
			if query[0] != ".":
				filepath = path + '/' + d + '/' + query
				call(["node", "download_from_json.js", filepath, query, destclasspath])

# for file in onlyfiles:
# 	if file[0] != '.':
# 		filepath = path + '/' + file
# 		call(["node", "download_from_json.js", filepath, file])