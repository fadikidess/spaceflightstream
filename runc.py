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
tracker = 4
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
                urllib.request.urlretrieve(urls[ind], os.getcwd() + '/space.jpg')
                cap = txts[ind] + "\n\n\nCredits: " + urls[ind] + "\n\n\n #space#nasa#spacex#elon#elonmusk#astronout#engineer#adventure#epic"
                bot.upload_photo(os.getcwd() + '/space.jpg',caption = cap)
                print(txts[ind])
                print(urls[ind])
                time.sleep(2500)
    else:
        tracker = tracker + 1
        nexts = True
    if nexts == True:
        execute()
    #print(txts[0])
my_thread = threading.Thread(target=execute, args=())
my_thread.start()



