from os import walk
from os import path
import os
import sys
from subprocess import call
from walkdir import filtered_walk, dir_paths, all_paths, file_paths

PATH_FROM = path.join(os.curdir, 'test')
PATH_TO = path.join(os.curdir,'testTarget')
#Get paths in 1 and 2 depth
dirsDepth1 = dir_paths(filtered_walk(PATH_FROM, depth=1, min_depth=1))
dirsDepth2 = dir_paths(filtered_walk(PATH_FROM, depth=2, min_depth=2))

#Create folders
def createDir(PATH_TO):
    if path.isdir(PATH_TO):
        print('Dir exist')
    else:
        call(['mkdir', '-p',PATH_TO])
def copyFile(SRC,DST):
    call(['cp', SRC, DST])
#Copy target depth 1 dir
for x in dirsDepth1:
    createDir(x.replace(PATH_FROM, PATH_TO))


for depth2 in dirsDepth2:
    files = file_paths(filtered_walk(depth2,depth=2,included_files=['*.jpg','*.png','*.jpeg']))
    dirList   = depth2.split('/')
    last  = dirList.pop()
    for f in files:
        #Remove dept2 filename and replace source folder to target folder
        dst = f.replace(depth2,'/'.join(dirList)).replace(PATH_FROM,PATH_TO)
        copyFile(f, dst)

