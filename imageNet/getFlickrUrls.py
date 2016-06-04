#Made by Sangpil Kim
#Jun 2016

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from getIdcon import getIdfromHtml
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

def initDriver(url):
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver,1)
    driver.get(url)
    return driver
def getUrlsFromId(id):
    url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='+id
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
    conId = getIdfromHtml('imDogDom.html')
    html = getUrlsFromId(conId[0])
    html = html.encode('ascii','ignore')
    urls = getFlickerUrls(html)
    className ='dog'
    counter = 0
    for url in urls:
        counter += 1
        dw = sub.call('wget '+ url +' -O ./'+className+'/img'+str(counter)+'.png',shell=True)

