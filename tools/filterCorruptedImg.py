#Made by Sangpil Kim
#June 2016

from PIL import Image
import os
from os.path import join
import fnmatch
from subprocess import run
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
                if '.jpeg'in fileName:
                    filePath = join(d,fileName)
                    try:
                        v_image = Image.open(filePath)
                        si = os.path.getsize(filePath)
                        if si == 2051 or si < 3000:
                            filePath = os.getcwd()+'/'+filePath
                            print (filePath+' delete')
                            run(['rm', '-rf', str(filePath)])
                    except:
                        filePath = os.getcwd()+'/'+filePath
                        print (filePath+' delete')
                        run(['rm', '-rf', str(filePath)])
if __name__ == '__main__':
    filterCorruptPng(sys.argv[1])


