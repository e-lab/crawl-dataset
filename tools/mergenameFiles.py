from os import walk
from os import path
import os
import sys
from subprocess import call
from walkdir import filtered_walk, dir_paths, all_paths, file_paths

PATH_FROM = path.join(os.curdir, 'edataSet2Depth1')
PATH_TO = path.join(os.curdir,'edataSet2Depth1')
#Get paths in 1 and 2 depth
dirsDepth1 = dir_paths(filtered_walk(PATH_FROM, depth=1, min_depth=1))
dirsDepth2 = dir_paths(filtered_walk(PATH_FROM, depth=2, min_depth=2))

#Create folders
def createDir(PATH_TO):
    if path.isdir(PATH_TO):
        print('Dir exist')
    elsed:
        call(['mkdir', '-p',PATH_TO])

#copy file
def copyFile(SRC,DST):
    call(['cp', SRC, DST])

#change file name
def changFileName(SRC, DST):
    call(['mv', SRC, DST])

#Copy target depth 1 dir
for depth1 in dirsDepth1:
    files = file_paths(filtered_walk(depth1,depth=1,included_files=['*.jpg','*.png','*.jpeg']))
    print('working on '+str(depth1))
    for f in files:
        dst = f.replace(' ','_')
        if f != dst:
            changFileName(f, dst)

