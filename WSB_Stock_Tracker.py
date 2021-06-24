#!/usr/bin/python3
import requests
import re
import urllib
import numpy as np
from numpy import zeros
import random
from matplotlib import pyplot as plt
import time
from operator import attrgetter

from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup

global tickerBook
global firstBook

class ticker:
    def __init__(self, name, sent, rank, diff, totaldiff, price):
        self.name = name
        self.sent = sent
        self.rank = rank
        self.diff = diff
        self.price = price
        self.totaldiff = totaldiff

"""
def getPrice()
    url = ""
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)
"""

def getSoup():
    url = "https://stocks.comment.ai/trending.html"
    internet=True
    try:
        request = requests.get(url, timeout=5)
    except (requests.ConnectionError, requests.Timeout) as exception:
        internet = False
        while(not(internet)):
            print("No internet")
            time.sleep(30)
            try:
                request = requests.get(url, timeout=5)
                internet = True
            except (requests.ConnectionError, requests.Timeout) as exception:
                internet = False

    page = urlopen(url, timeout=5)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("td")

def getSiteData(timesChecked):
    global tickerBook
    global firstBook
    rank=1
    r=0
    newtickerBook = np.empty(0)
    soup = getSoup()


    if(len(soup)<80):
        r = len(soup)
    else:
        r = 80

    if(timesChecked==0):
        for x in range(r):
            if(x%4==0):
                firstBook = np.append(newtickerBook, ticker(soup[x+2].string, soup[x].string, rank, 0.0, 0.0, 0.0))
                newtickerBook = np.append(newtickerBook, ticker(soup[x+2].string, soup[x].string, rank, 0.0, 0.0, 0.0))
                rank+=1
    else:
        for x in range(r):
            if(x%4==0):
                diff = getSentDiffPercent(soup[x+2].string, soup[x].string)
                newtick = ticker(soup[x+2].string, soup[x].string, rank, diff, getTotalDiff(soup[x+2].string, soup[x].string), 0.0)
                newtickerBook = np.append(newtickerBook, newtick)
                rank+=1
    return newtickerBook

def getSentDiff(name, sent):
    global tickerBook
    for z in range(len(tickerBook)):
        if(str(name)==str(tickerBook[z].name)):
            return int(sent) - int(tickerBook[z].sent)
    return 0.0

def getSentDiffPercent(name, sent):
    global tickerBook
    for z in range(len(tickerBook)):
        if(str(name)==str(tickerBook[z].name)):
            diff = int(sent) - int(tickerBook[z].sent)
            change = round(diff/float(int(tickerBook[z].sent)),2)
            if(change<0):
                return str(change)
            elif(change>0):
                return "+"+str(change)
            return "0.0"
    return "0.0"

def getTotalDiff(name, sent):
    global firstBook
    for z in range(len(firstBook)):
        if(str(name)==str(firstBook[z].name)):
            diff = int(sent) - int(firstBook[z].sent)
            change = round(diff/float(int(firstBook[z].sent))*(100),2)
            if(change==0):
                return 0.0
            else:
                return change

    return 0.0

def startTracker():
    timesChecked=0
    global firstBook
    global tickerBook
    tickerBook = np.empty(0)
    firstBook = np.empty(0)
    tickerBook = getSiteData(timesChecked)
    print("_________")
    print("Seconds Elapsed: 0")
    print("_________")
    printTickersHorz(tickerBook)
    timesChecked+=1
    while(True):
        print("_________")
        print("Seconds Elapsed: "+str((timesChecked-1)*30))
        print("_________")
        time.sleep(30)
        tickerBook = getSiteData(timesChecked)
        printTickersHorz(tickerBook)
        print("_________")
        print("Fastest Growers")
        displayFastestGrowers()
        timesChecked+=1

def displayFastestGrowers():
    growers = sorted(tickerBook, key=attrgetter("totaldiff"))
    growers.reverse()
    for a in range(len(growers)):
        if(growers[a].totaldiff>0):
            print(str(a+1)+". Ticker: "+str(growers[a].name)+" |"+" Total Change: +"+str(growers[a].totaldiff)+"%")
        else:
            print(str(a+1)+". Ticker: "+str(growers[a].name)+" |"+" Total Change: "+str(growers[a].totaldiff)+"%")

def printTickersHorz(tickerBook):
    for y in range(len(tickerBook)):
        print("Ticker: "+str(tickerBook[y].name)+" |"+" Sentiment: "+str(tickerBook[y].sent)+" |"+" Rank: "+str(tickerBook[y].rank)+" |"+" 30 Second Change: "+str(tickerBook[y].diff)+"%"+" |"+" Total Change: "+str(tickerBook[y].totaldiff)+"%")

def printTickersVert(tickerBook):
    for y in range(len(tickerBook)):
        print("++++++++++++++++++++++++")
        print("Ticker: "+str(tickerBook[y].name))
        print("Sentiment: "+str(tickerBook[y].sent))
        print("Rank: "+str(tickerBook[y].rank))
        print("30 Second Change: "+str(tickerBook[y].diff)+"%")
        print("Total Change: "+str(tickerBook[y].totaldiff)+"%")

startTracker()
