import threading
import re
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from instabot import Bot
import os
import psycopg2
url = "https://www.spacetelescope.org/images/page/"
urls = {}
txts = {}
tracker = 4
nexts = False
bot = Bot() 
bot.login(username = "spaceflightstream",password = "FGKpro2003") 
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn = psycopg2.connect(database = "d9i3n82aq3qb6v", user = "cdlxvjkiuieoeu", password = "d0487bbce60768a4e6e96831b8b3e6cb7d98b93d2ddc4ebd16410d098fad8761", host = "ec2-52-22-216-69.compute-1.amazonaws.com", port = "5432")
print("Opened database successfully")
postgreSQL_select_Query = "select * from urls"
cur = conn.cursor()
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
        tempdr = False
        cur.execute(postgreSQL_select_Query)
        records = cur.fetchall() 
        for row in records:
            if row[0] == urls[ind]:
                tempdr = True
        if tempdr == False:
            urllib.request.urlretrieve(urls[ind], os.getcwd() + '/space.jpg')
            cap = txts[ind] + "\n\n\nCredits: " + uro + "\n\n\n #space#nasa#spacex#elon#elonmusk#astronout#engineer#adventure#epic#cool#launch"
            po = "INSERT INTO urls (url) VALUES ('"+urls[ind]+"')"
            record_to_insert = (urls[ind])
            cur.execute(po, record_to_insert)
            bot.upload_photo(os.getcwd() + '/space.jpg',caption = cap)
            print(txts[ind])
            print(urls[ind])
            

            conn.commit()
            time.sleep(14400)
    else:
        tracker = tracker + 1
        nexts = True
    if nexts == True:
        execute() 
    #print(txts[0])
hashtags = ["space","nasa","spacex","elon","elonmusk","astronout","engineer","adventure","epic","cool","launch"]
wait = 35 * 60
def gainer():
    while True:
        for hashtag in hastags:
            users = bot.get_hashtag_users(hashtag)
            bot.follow_users(users)
            bot.like_hashtag(hashtag)
        time.sleep(wait)
my_thread = threading.Thread(target=execute, args=())
my_thread.start()
trdr = threading.Thread(target=gainer, args=())
trdr.start()

