#Made by Sangpil Kim
#June 2016

from PIL import Image
import os
from os.path import join
import fnmatch
import subprocess as sub
import sys
from pathlib import Path as path
di = []
def filterCorruptPng(rootdir):
    p = path(rootdir)
    for x in p.iterdir():
        if x.is_dir():
            print('Working on this dir below')
            print(str(x))
            di.append(str(x))
    for d in di:
        for subdir, dirs, files in os.walk(d):
            for fileName in files:
                if '.png'in fileName:
                    filePath = join(d,fileName)
                    print (filePath+' check')
                    try:
                        v_image = Image.open(filePath)
                        si = os.path.getsize(filePath)
                        if si == 2051 or si < 15000:
                            print (filePath+' delete')
                            rm = sub.call('rm -rf '+filePath,shell=True)
                    except:
                        print (filePath+' delete')
                        rm = sub.call('rm -rf '+filePath,shell=True)
if __name__ == '__main__':
    filterCorruptPng(sys.argv[1])


