#coding:'UTF-8'
import requests
import time
import json
import re
from bs4 import BeautifulSoup as bs
import codecs
import sys
from bs4 import BeautifulSoup
import os
from os import listdir
from os.path import isfile, isdir, join
import cloudscraper
#from playwright.sync_api import sync_playwright



# check link
def GetWebContent(bangou):
    URL = f'https://www.javlibrary.com/ja/vl_searchbyid.php?keyword={bangou}'
    r = scraper.get(URL,headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    soup.encoding = 'utf-8'
    if soup.select_one(".videothumblist"):
        try:
            link = "http://www.javlibrary.com/ja/" + soup.select_one(".videothumblist").select_one('.video a')["href"]
            r = scraper.get(link,headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            soup.encoding = 'utf-8'   
            #print(link)
        except:
            print('gg')
            return ""

    return(soup)




# 以迴圈處理
def getLink(number):
  session = requests.session()
  headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",'Cache-Control': "no-cache"}
  scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False}, sess=session,delay = 100)
  content = GetWebContent(number)
  if not content:
    print("ff")
  else:
    getL = content.select_one("#video_jacket_img").get("src")
    if getL.startswith('http'):
      piclink = getL
    else:
      piclink = "http:"+content.select_one("#video_jacket_img").get("src")
  return piclink




  
