from os import listdir
from os.path import isfile, join
import sys
from subprocess import call

path = sys.argv[1]

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for file in onlyfiles:
	if file[0] != '.':
		filepath = path + '/' + file
		call(["node", "download_from_json.js", filepath, 'images'])