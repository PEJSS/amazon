from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import csv
def getLink(url,tag,attribute):
    user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    headers = {'User-Agent':user_agent,'Connection':'Close'}
    req = Request(url,headers=headers)
    html = urlopen(req)
    bso = BeautifulSoup(html.read(),"lxml")
    temp = bso.find_all(tag,class_=attribute)
    return temp
def getInfo(url,Name=[],Price=[],TransP=[]):
    user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    headers = {'User-Agent':user_agent,'Connection':'Close'}
    req = Request(url,headers=headers)
    html = urlopen(req)
    bso = BeautifulSoup(html.read(),"lxml")
    name = bso.find(Name[0],id=Name[1]).string
    price = bso.find(Price[0],id=Price[1],class_=Price[2]).string
    transp = bso.find(TransP[0],class_=Price[1]).string
    return (name,price,transp)
with open('amazon.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['类别','商品名字','价格','运费'])
items = getLink('https://www.amazon.com/kitchen-dining/b/ref=sd_allcat_ki?ie=UTF8&node=284507','div','bxc-grid__image bxc-grid__image--light')
for item in items:
    if item.a != None and item.img != None:
        url1 = 'https://www.amazon.com' + item.a['href']
        categories = getLink(url1,'div','bxc-grid__image bxc-grid__image--light')
        for item in categories:
            if item.a != None and item.img != None:
                url2 = 'https://www.amazon.com' + item.a['href']
                user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
                headers = {'User-Agent':user_agent,'Connection':'Close'}
                req = Request(url2,headers=headers)
                html2 = urlopen(req)
                bso2 = BeautifulSoup(html2.read(),"lxml")
                category = bso2.find('div',class_='unified_widget pageBanner').h1.b.string
                stuffs = getLink(url2,'a','a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal')
                for item in stuffs:
                    url3 = 'https://www.amazon.com' + item['href']
                    info = category + getInfo(url3,Name=['span','productTitle'],Price=['span','priceblock_ourprice','a-size-medium a-color-price'],TransP=['span','a-size-base a-color-secondary'])
                    with open('amazon.csv','a',newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(info)
                while bso2.find('a',id='pagnNextLink') != None:
                    url2 = 'https://www.amazon.com' + bso2.find('a',id='pagnNextLink')['href']
                    stuffs = getLink(url2,'a','a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal')
                    for item in stuffs:
                        url3 = 'https://www.amazon.com' + item['href']
                        info = category + getInfo(url3,Name=['span','productTitle'],Price=['span','priceblock_ourprice','a-size-medium a-color-price'],TransP=['span','a-size-base a-color-secondary'])
                        with open('amazon.csv','a',newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(info)