import os
import csv
import sys
import json
from scipy.misc import imresize, imread, imsave
from urllib import request as rq
from os.path import join
from os.path import isdir
from pathlib import Path
from subprocess import call
import multiprocessing as mul

#Write Json
def writeJson(label,filename):
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(label,f)
#read Json
def readJson(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        jsonV = json.load(f)
    return jsonV
#Loading csv
def load_csv(csv_filepath):
    csv_filepath = join(os.curdir,csv_filepath)
    print('loading csv from {}'.format(csv_filepath))
    with open(csv_filepath) as csvfile:
        reader = csv.reader(csvfile)
        lists = list(reader)
    return lists
#Loading dic format csv for images.csv
def load_dic_csv(csv_filepath):
    csv_filepath = join(os.curdir,csv_filepath)
    print('loading dic from {} '.format(csv_filepath))
    with open(csv_filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        lists = []
        for row in reader:
            lists.append({ 'ImageID': row['ImageID'],
                           'Subset': row['Subset'],
                           'OriginalURL': row['OriginalURL'],
                           'License': row['License'],
                           'Title': row['Title']})
    return lists
#Loading label csv
def load_label_csv(csv_filepath):
    csv_filepath = join(os.curdir,csv_filepath)
    tmp = load_csv(csv_filepath)
    lists = []
    print('Laoding label from csv')
    for i in range(1,len(tmp)):
        tmp2 = tmp[i]
        for i in range(1,len(tmp2)):
            tmp3 = tmp2[i].split(':')
            lists.append({ tmp3[1]:tmp2[0]})
    return lists

#code extract function
def getCode(classes41,dicts):
    print('Combin class with dict.csv')
    match = {}
    #Iter target classes
    for name in classes41:
        name = name[0]
        tmp = []
        #Iter 9murl classes
        for info in dicts:
            #Perform exact match
            if name == info[1]:
                tmp.append(info[0])
        #Since exact match it mas only 1 code
        match[name] = tmp[0]
    #Check missing item
    for item in match:
        list = match[item]
        if not list:
            print('{} item missing in dict'.format(item))
    return match

#Check file if not create
def checkFile(path):
    if not isdir(path):
        call(['mkdir','-p',path])
    else:
        print('{} exist'.format(path))
#reSize img
def resizeImg(imgPath):
    img = imread(imgPath)
    h, w, _ = img.shape
    scale = 1
    if w >= h:
        new_w = 256
        if w  >= new_w:
            scale = float(new_w) / w
        new_h = int(h * scale)
    else:
        new_h = 256
        if h >= new_h:
            scale = float(new_h) / h
        new_w = int(w * scale)
    new_img = imresize(img, (new_h, new_w), interp='bilinear')
    imsave(imgPath,new_img)

#Download img
#Later we can do multi thread apply workers to do faster work
def downLoadImg(rootPath,infoList,codeTable):
    rootPath = join(rootPath,infoList[0]['Subset'])
    #MAKE code as key change infoList
    dic = {}
    #Convert infoList to hashable dic with 64bit img code ID
    for info in infoList:
        dic[info['ImageID']] = info
    #Check classes with own code
    #Iterate code table
    for code in codeTable:
        print('Downloading class : {}'.format(code[0]))
        folderPath = join(rootPath,code[0])
        #Check folder if not create
        checkFile(folderPath)
        #Lets download code code[1] has option number of code
        for id in code[1]:
            #Get info from dictionary
            if id in dic.keys():
                info = dic[id]
            #Get url
            url = info['OriginalURL']
            #Extract extention
            ext = url.split('.')
            ext = ext[len(ext)-1]
            #Set save path for image
            savePath = join(folderPath,str(id)+ '.' + ext)
            check = Path(savePath)
            #Check if we downloaded before
            if not check.is_file():
                print('Downloading : {} at {}' .format(info['ImageID'],info['Subset']))
                print(url)
                p = mul.Process(target = rq.urlretrieve, name='download',args=(url,savePath))
                p.start()
                # Let's wait 20 sec for downloading
                p.join(20)
                if p.is_alive():
                    print('Too longdownloading terminate')
                    p.terminate()
                    p.join()
                    #Delete junks which we fail to download
                    call(['rm','-rf',savePath])
                # If we succeed exitcode will be 0
                if p.exitcode == 1:
                    print('fail')
                else:
                    #Lets resize with 256 size
                    try:
                        resizeImg(savePath)
                        print('resized')
                    except Exception as e:
                        print(e)
            else:
                print('Already Downloaded')
# num : number of image match: dic of image class
#labels from labes.csv
def getCodeFromLabel(num,match,labels):
    print('Get code from labels')
    t = []
    for key, value in match.items():
        tmp = []
        for label in labels:
            if value in label.keys():
                tmp.append(label[value])
                if len(tmp) == num:
                    break
        t.append([key,tmp])
    return t

# dict is class name and own id mapper from google
fileName = sys.argv[1]
# We want this classes csv
fileName2 = sys.argv[2]
#Load dictionary
dicts     = load_csv(fileName)
#Get our class
classes41 = load_csv(fileName2)
# MApping our to google dictionary
match = getCode(classes41,dicts)
#Print for test
print('Show classes and target code')
print(match)
#Decide where we want train? validation
#images.csv have url, authorm licence, etc
sourcePath = sys.argv[3]
#ImageID, Subset, OriginalURL, Title
source = load_dic_csv(sourcePath)
#labels.csv has 64bit img ids and map to target class
labelPath = sys.argv[4]
labels = load_label_csv(labelPath)
#Set our number per class
num = int(sys.argv[5])
#Get img 64bit info mapping
codeTable = getCodeFromLabel(num,match,labels)
#Set up our target folder
rootPath = sys.argv[6]
#Call downloader to download images
downLoadImg(rootPath,source,codeTable)
