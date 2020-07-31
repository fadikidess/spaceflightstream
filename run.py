import threading
import re
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from instabot import Bot
import os
url = "https://www.flickr.com/photos/nasa2explore/page"
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
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get(uri)
        time.sleep(3)
        r = driver.page_source
        #driver.quit()
        return r
    uro = url + str(tracker)
    r = render_page(uro)
    soup = BeautifulSoup(r, 'html.parser')
    print("hello!")
    info = soup.find_all("div", {"class": "view photo-list-photo-view requiredToShowOnServer photostream awake"})
    txt = soup.find_all("div", {"class": "interaction-bar"})
    for n,i in enumerate(info):
        i['style'] = i['style'].split('\n+')
        style = i['style']
        for u in style:
            u = u[:-3]

            urls[n] = "https:"+u.split('url("')[1]
            #print("https:"+u.split('url("')[1])
    for index, s in enumerate(txt):
        txts[index] = s['title']
    print(len(txts))

    for ind, r in enumerate(txts):
        with open("Memory.txt", "r+") as myfile:

            # A file is an iterable of lines, so this will
            # check if any of the lines in myfile equals line+"\n"
            if urls[ind]+"\n" not in myfile:

                # Write it; assumes file ends in "\n" already
                myfile.write(urls[ind]+"\n")
                myfile.flush()
                urllib.request.urlretrieve(urls[ind], os.getcwd() + '/space.jpg')
                cap = txts[ind] + "\n\n\nCredits: " + url + "\n\n\n #space#nasa#spacex#elon#elonmusk#astronout#engineer#adventure#epic"
                bot.upload_photo(os.getcwd() + '/space.jpg',caption = cap)
                print(txts[ind])
                print(urls[ind])
                time.sleep(2400)
    else:
        tracker = tracker + 1
        nexts = True
    if nexts == True:
        execute()
    #print(txts[0])
my_thread = threading.Thread(target=execute, args=())
my_thread.start()



