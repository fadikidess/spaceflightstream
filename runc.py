import threading
import re
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from instabot import Bot
import os
url = "https://www.spacetelescope.org/images/page/"
urls = {}
txts = {}
tracker = 1
nexts = False
bot = Bot() 
bot.login(username = "spaceflightstream",password = "FGKpro2003") 
def execute():
    global url
    global tracker
    global urls
    global txts
    global nexts
    def render_page(uri):
        driver = webdriver.Chrome()
        driver.get(uri)
        time.sleep(3)
        r = driver.page_source
        #driver.quit()
        return r
    uro = url + str(tracker) + "/"
    r = render_page(uro)
    soup = BeautifulSoup(r, 'html.parser')
    print("hello!")
    info = soup.find_all("img", {"class": "image-thumb"})
    txt = soup.find_all("div", {"class": "title"})
    for n,i in enumerate(info):
        urls[n] = i['src']
    for index, s in enumerate(txt):
        txts[index] = s.text
    print(len(txts))    
    for ind, r in enumerate(txts):
        with open("Memory.txt", "r+") as myfile:

            # A file is an iterable of lines, so this will
            # check if any of the lines in myfile equals line+"\n"
            if urls[ind]+"\n" not in myfile:
                urllib.request.urlretrieve(urls[ind], '/Users/fadikidess/Downloads/ISS-photo-locations-master/scripts/space.jpg')
                cap = txts[ind] + "\n\n\nCredits: " + url + "\n\n\n #space#nasa#spacex#elon#elonmusk#astronout#engineer#adventure#epic"
                bot.upload_photo('/Users/fadikidess/Downloads/ISS-photo-locations-master/scripts/space.jpg',caption = cap) 
                os.remove('/Users/fadikidess/Downloads/ISS-photo-locations-master/scripts/space.jpg')
                print(txts[ind])
                print(urls[ind])
                time.sleep(7200)
    else:
        tracker = tracker + 1
        nexts = True
    if nexts == True:
        execute()
    #print(txts[0])
my_thread = threading.Thread(target=execute, args=())
my_thread.start()


