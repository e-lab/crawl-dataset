#Made by Sangpil Kim
#June 2016

import sys
import csv
import subprocess as sub
import requests
import codecs
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
    return urls

if __name__ == '__main__':
    className = sys.argv[1].replace('.csv','')
    conIds = getIds(sys.argv[1])
#    className = sys.argv[2]
    for conId in conIds:
        print(conId)
        html = getUrlsFromId(conId)
        #html = html.encode('ascii','ignore')
        html = str(html)
        urls = getFlickerUrls(html)
        counter = 0
        for url in urls:
            try:
                counter += 1
                print ('-----------------')
                filePath = className+'/'+className+'_'+str(counter)+'.jpeg'
                print(filePath)
                dw = sub.call('wget --timeout=5 --tries=2 -A jpeg,jpg,bmp,gif,png '+ url +' -O ./'+filePath ,shell=True)
            except:
                print('Fail')

