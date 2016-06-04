import subprocess as sub
import os.path
import sys

def init():
    if not os.path.isdir('./images'):
        init = sub.call('mkdir images',shell=True)
    else:
        print 'images folder exist'

def makeFolder(name):
    name = os.getcwd()+'/images/'+name
    if not os.path.isdir(name):
        print 'creating new images folder'
        make_folder = sub.call('mkdir -p '+name,shell=True)
    else:
        print name+' already exist'

def moveFiles(name):
    target = os.getcwd()+'/images/'+name
    if not os.path.isdir(target):
        print 'moving images'
        makeFolder(name)
        mv_files = sub.call('mv images/*.png '+target,shell=True)

def getImages(name):
    down = sub.call('node app.js '+name,shell=True)

def getNames(txt):
    f = open(txt,'r')
    con = []
    lines = f.readlines()
    for line in lines:
        con.append(line)
    return con

if __name__=='__main__':
    names = getNames(sys.argv[1])
    init()
    for name in names:
        getImages(name)
        makeFolder(name)
        moveFiles(name)



