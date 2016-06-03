
# coding: utf-8

# In[37]:

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

