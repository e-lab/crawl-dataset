#Made by Sangpil Kim
#June 2016

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
    for fileName in os.listdir(subDir):
        fileName = join(subDir,fileName)
        if os.path.isfile(fileName):
            if 'py' in fileName:
                os.remove(fileName)
            if 'csv' in fileName:
                os.remove(fileName)
            if '\r' or '^M'in fileName:
                counter += 1
                print('%d/%d' %(counter,len(fileName)))
                check = False
                for ext in extList:
                    if ext in fileName:
                        check = True
                        newName = fileName.replace(ext+'\r',ext)
                if not check:
                    newName = fileName.replace('\r','') + '.jpeg'
                #print(fileName)
                newName = join(subDir,newName)
                try:
                    os.rename(fileName,newName)
                except:
                    failCon.append(fileName)
                    print('Fail')
    '''
print(failCon)
print(len(failCon))
