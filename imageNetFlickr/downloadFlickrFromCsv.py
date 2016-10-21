#Made by Sangpil Kim
#June 2016
#python 3.5

import sys
import csv
from os.path import join
import subprocess as sub
import requests
import codecs
import click
from walkdir import filtered_walk, dir_paths, all_paths, file_paths
from getImgs import downLoadImg
from bs4 import BeautifulSoup as bs4

def getIdfromHtml(html):
    #Open html file
    f = codecs.open(html,'r', 'utf-8')
    dom = f.read().encode('ascii','ignore')
    f.close()
    #make soup
    soup = bs4(dom)
    urls = soup.find_all(href=True)
    #get id
    conId = []
    for url in urls:
        id = url.get('href').split('=')
        conId.append(id[1])
    return conId
def getIds(csvFile):
    conIds = []
    with open(csvFile, 'r') as f:
         reader = csv.reader(f)
         for row in reader:
             conIds.append(row[0])
    return conIds
def getUrlsFromId(id):
    url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='+id
    print(url)
    r = requests.get(url)
    html = r.text
    return html
def getFlickerUrls(html):
    urls =[]
    urls = html.split('\n')
    for url in urls:
        if not 'flickr' in url:
            urls.pop()
    infoList = []
    idx = 0
    for url in urls:
        idx += 1
        dic = {}
        dic['idx'] = idx
        dic['url'] = url
        infoList.append(dic)
    return infoList
def down(csvfile,destpath,img_size,thread_number):
    className = csvfile.replace('.csv','')
    destpath = join(destpath,className)
    conIds = getIds(csvfile)
    for conId in conIds:
        print(conId)
        html = getUrlsFromId(conId)
        #html = html.encode('ascii','ignore')
        html = str(html)
        infoList = getFlickerUrls(html)
        downLoadImg(destpath,infoList,img_size,thread_number)

@click.command()
@click.argument('srcdir') #,help='Dir of json file which has url txt')
@click.option('-destpath',default='images') #,help='Dest dir')
@click.option('-img_size',default=256)
@click.option('-thread_number',default=5)
def main(srcdir,destpath,img_size,thread_number):
    #Iterate csv container
    csvFiles = file_paths(filtered_walk(srcdir, depth=1, included_files='*.csv'))
    for csvfile in list(csvFiles):
        #Download files
        down(csvfile,destpath,img_size,thread_number)

if __name__ == '__main__':
    main()

