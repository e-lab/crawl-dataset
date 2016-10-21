from urllib import request as rq
from os.path import join
from os.path import isdir
from pathlib import Path
from subprocess import call
from scipy.misc import imresize, imread, imsave
import sys
import time
import multiprocessing as mul
from concurrent import futures
from tqdm import tqdm

#reSize img
def resizeImg(imgPath,img_size):
    img = imread(imgPath)
    h, w, _ = img.shape
    scale = 1
    if w >= h:
        new_w = img_size
        if w  >= new_w:
            scale = float(new_w) / w
        new_h = int(h * scale)
    else:
        new_h = img_size
        if h >= new_h:
            scale = float(new_h) / h
        new_w = int(w * scale)
    new_img = imresize(img, (new_h, new_w), interp='bilinear')
    imsave(imgPath,new_img)
    print('Img Resized as {}'.format(img_size))

def checkFile(path):
    if not isdir(path):
        call(['mkdir','-p',path])
    else:
        print('{} exist'.format(path))

#Txt file is dictionary txt return list of dicts
def readTxt(txtFile):
    tmp = []
    #Get info from txt
    idx = 0
    with open(txtFile,'r') as inf:
        for line in inf:
            tmp.append(eval(line))
    infoList = tmp[0]
    for info in infoList:
        idx += 1
        info['idx'] = idx
    return infoList


#Download img
def downLoadImg(destPath,infoList,img_size,thred_number):
    lencl= len(destPath)-1
    if destPath[lencl] == '/':
        destPath = destPath[:-1]
    className = destPath.split('/')
    className =  className[len(className)-1]
    def process(info):
        url = info['url']
        ext = info['format']
        idx = info['idx']
        print(idx)
        savePath = join(destPath,className+ str(idx) + '.' + ext)
        check = Path(savePath)
        if not check.is_file():
            print('Downloading : {} th {}' .format(idx,className))
            start = time.clock()
            p = mul.Process(target = rq.urlretrieve, name='download',args=(url,savePath))
            p.start()
            p.join(20)
            if p.is_alive():
                print('Too longdownloading terminate')
                p.terminate()
                p.join()
                call(['rm','-rf',savePath])
            if p.exitcode == 1:
                print('fail')
                call(['rm','-rf',savePath])
            else:
                resizeImg(savePath,img_size)
        else:
            print('Already Downloaded')
    with futures.ThreadPoolExecutor(max_workers=thred_number) as worker:
        mapper = [worker.submit(process,info) for info in infoList ]
        for tmp in tqdm(futures.as_completed(mapper), total=len(mapper)):
            pass


#Source txt file
txtFile = sys.argv[1]
#Destination folder
destPath = sys.argv[2]
#img size
img_size = int(sys.argv[3])
#Thread number
th_number = int(sys.argv[4])
#Check file exist not creat
checkFile(destPath)
#Get info
infoList = readTxt(txtFile)
downLoadImg(destPath,infoList,img_size,th_number)

