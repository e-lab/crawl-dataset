
# coding: utf-8

# In[50]:

from PIL import Image
import os
import fnmatch
import subprocess as sub
import sys
def filterCorruptPng(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        for fileName in files:
            if '.png'in fileName:
                filePath = os.path.join(rootdir,fileName)
                try:
                    v_image = Image.open(filePath)
                    si = os.path.getsize(filePath)
                    if si == 2051 or si < 15000:
                        print fileName+' delete'
                        rm = sub.call('rm -rf '+filePath,shell=True)
                except:
                    print fileName+' delete'
                    rm = sub.call('rm -rf '+filePath,shell=True)

if __name__ == '__main__':
    filterCorruptPng(sys.argv[1])
    