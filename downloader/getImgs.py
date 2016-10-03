from urllib import request as rq
from os.path import join
from os.path import isdir
from pathlib import Path
from subprocess import call
import sys

def checkFile(path):
    if not isdir(path):
        call(['mkdir','-p',path])
    else:
        print('{} exist'.format(path))

#Txt file is dictionary txt return list of dicts
def readTxt(txtFile):
    tmp = []
    #Get info from txt
    with open(txtFile,'r') as inf:
        for line in inf:
            tmp.append(eval(line))
    infoList = tmp[0]
    return infoList

#Download img
def downLoadImg(destPath,infoList):
    lencl= len(destPath)-1
    if destPath[lencl] == '/':
        destPath = destPath[:-1]
    className = destPath.split('/')
    className =  className[len(className)-1]

    idx = 1
    for info in infoList:
        url = info['url']
        ext = info['format']
        savePath = join(destPath,className+ str(idx) + '.' + ext)
        check = Path(savePath)
        if not check.is_file():
            try:
                print('Downloading : {} th {}' .format(idx,className))
                rq.urlretrieve(url,savePath)
                idx += 1
            except:
                print('fail')
        else:
            print('Already Downloaded')
            idx += 1


#Source txt file
txtFile = sys.argv[1]
#Destination folder
destPath = sys.argv[2]
#Check file exist not creat
checkFile(destPath)
#Get info
infoList = readTxt(txtFile)
downLoadImg(destPath,infoList)

