#Made by Sangpil Kim
#June 2016
#Python 3.5

import os
import sys
from os.path import join

cwd = os.getcwd()
rootDir = os.path.join(cwd,sys.argv[1])
counter = 0
conDirs = []
failCon = []
extList = ['jpg','png','gif','jpeg','JPG']
# collect subdirs
for subdirs_, dirs_, files_ in os.walk(rootDir):
    if subdirs_ :
        if not '.' or not '..' in subdirs_:
            if not subdirs_ == cwd:
                conDirs.append(subdirs_)
# iter subdirs and change file name
for i in range(1,len(conDirs)):
    print(conDirs[i])
    subDir = conDirs[i]
    counter = 0
    for fileName in os.listdir(subDir):
        print('%d th image processing' %(counter))
        counter += 1
        fileName = join(subDir,fileName)
        if os.path.isfile(fileName):
            if 'py' in fileName:
                os.remove(fileName)
            if 'csv' in fileName:
                os.remove(fileName)
            folderName = subDir.split('/')
            newName = str(folderName[len(folderName)-1])+'_'+str(counter)+'.jpeg'
            newName = join(subDir,newName)
            try:
                print(fileName)
                os.rename(fileName,newName)
            except:
                print('Fail')
