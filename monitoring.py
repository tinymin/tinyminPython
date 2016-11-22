import requests
import re
import telebot
from bs4 import BeautifulSoup
from datetime import datetime

targets = [
{"url":"http://www.apple.com/kr/shop/browse/home/specialdeals/mac", "filter":{"2015년", "13.3형", "8GB", "256GB"}, "funcFind":lambda x:x.find("div", attrs={"class":"box refurb-list"}).find_all("td", attrs={"class":"specs"})}
]
API_TOKEN = <Telegram_Bot Token>
bot = None
seq = 1

def getSoup(url):
    return BeautifulSoup(requests.get(url).text, 'lxml')

def getFilteredHtml(item):
    soup = getSoup(item["url"])
    item["html"] = item["funcFind"](soup)
    return item

def isContain(s, f):
    if(1 > s.count(f)):
        return False

    return True

def checkMyItem(s,filtering):
    for f in filtering:
        if False == isContain(s, f):
            return False

    return True

def getTelegramBot():
    if (None == bot):
        return telebot.TeleBot(API_TOKEN)
    return bot

def do(item):
    for l in item["html"]:
        t = l.text.replace(" ", "").strip("\r")
        if (False == checkMyItem(t, item["filter"])):
            continue

        bot = getTelegramBot()
        bot.send_message(<본인 Telegram ID (int 타입)>, item["url"])
        print(str(datetime.now()) + "\t" + str(seq).zfill(2) + " found matched : " + str(item["filter"]))
        break

print(str(datetime.now()) + "\tStarting lookup...")
for item in targets:
    print(str(datetime.now()) + "\t" + str(seq).zfill(2) + " Lookup " + item["url"])
    getFilteredHtml(item)
    do(item)
    seq += 1
print(str(datetime.now()) + "\tdone")