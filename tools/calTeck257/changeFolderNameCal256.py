from os import walk
from os import path
import os
import sys
from subprocess import call
from walkdir import filtered_walk, dir_paths, all_paths, file_paths

PATH_FROM = path.join(sys.argv[1])
#Get paths in 1 and 2 depth
dirsDepth1 = dir_paths(filtered_walk(PATH_FROM, depth=1, min_depth=1))

#copy file
def moveFile(SRC,DST):
    call(['mv', SRC, DST])
#Copy target depth 1 dir
for x in dirsDepth1:
    src = x
    x    = x.replace('-101','')
    x    = x.replace('-',' ')
    name = x.split('.')
    name = name[3]
    print('From')
    print(src)
    dst = path.join(PATH_FROM,name)
    print('To')
    print(dst)
    moveFile(src,dst)


