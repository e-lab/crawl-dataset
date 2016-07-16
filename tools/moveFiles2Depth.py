from os import walk
from os import path
import os
import sys
from subprocess import call

PATH_FROM = sys.argv[1]
PATH_TO = path.join(os.curdir,'edataSet2Origin2')
if not path.isdir( PATH_TO ):
    os.makedirs(PATH_TO)
else:
    print('Dir exists')

for dirpaths, dirnames, files in walk(PATH_FROM):
    if dirnames:
        #print(dirnames)
        dirpaths = path.join(os.curdir,dirpaths)
        for dirpaths2, dirnames2, _ in walk(dirpaths):
            if not dirnames2:
                print("Processing dir"+dirpaths2)
                call(['cp','-r',dirpaths2,PATH_TO])
print("Target Path: "+PATH_TO)
