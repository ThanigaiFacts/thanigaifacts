from tkinter import *
from PIL import ImageTk, Image
from urllib.request import urlopen
from datetime import datetime
import io


def processImg(ImgURL):
    with urlopen(ImgURL) as rawfile:
        ImgFile = rawfile.read()
    return ImageTk.PhotoImage(Image.open(io.BytesIO(ImgFile)))


def loadNews():
    news.URlNextPage += 1
    news.generateNewsWithImg()
    print(f"loaded page {news.URlNextPage}")
    showNews()


def showNews():
    global NewImg
    print(news.counter)
    try:
        newsHeader = news.NewsHeader[news.counter]
        newsLink = news.NewsLink[news.counter]
        img = news.NewsImg[news.counter]

        NewImg = processImg(img)
        canvas.itemconfig(newsImg, image=NewImg)
        canvas.itemconfig(newsTitle, text=newsHeader)
        # maxLength = len(news.NewsHeader)
        # print(newsLink)

        if news.counter < 1:
            prevBtn.config(state=DISABLED)
        else:
            prevBtn.config(state=NORMAL)
    except:
        loadNews()

    '''
    if news.counter > 10:
        nextBtn.config(state=DISABLED)
    else:
        nextBtn.config(state=NORMAL)
    '''


def changeNews(isNextBntPressed):
    # DetailBtn.config(state=NORMAL)
    # canvas.config(height=500)
    DetailBtn.config(state=NORMAL)
    detailTxt.config(text='')
    if isNextBntPressed:
        news.counter += 1
    else:
        news.counter -= 1
        prevBtn.config(state=NORMAL)
    showNews()


def detailBtnPressed():
     DetailBtn.config(state = DISABLED)
     news.generateDetailedNews()
     print(news.content)
     detailTxt.config(text = news.content)


###########################

import requests
from bs4 import BeautifulSoup


# count = 1
# URL = "https://www.empireonline.com/movies/features/best-movies-2/"
# URL = f"https://www.dailythanthi.com/News/State/"
# NewsDomain = "https://www.dailythanthi.com/"

class News:

    def __init__(self):
        self.URlNextPage = 0
        self.counter = 0
        self.URL = "https://www.dailythanthi.com/News/State/"
        self.NewsDomain = "https://www.dailythanthi.com/"
        self.soup = ''
        self.content = ''
        self.NewsHeader = []
        self.NewsLink = []
        self.NewsImg = []


    def generateNewsWithImg(self):
       print(f"\nSET - {self.URlNextPage}\n----------")
       req = requests.get(f"{self.URL}{self.URlNextPage}")
       self.soup = BeautifulSoup(req.content, 'html.parser')
       a_tags = self.soup.findAll("div", class_="ListingNewsWithMEDImage")

       for tag in a_tags:
           a_tag = tag.find('a')
           link = a_tag['href']
           img = a_tag.find('img')
           img_src = img['data-src']
           title = img['alt']

           self.NewsHeader.append(title)
           self.NewsLink.append(f"{self.NewsDomain}{link}")
           self.NewsImg.append(img_src)

    def generateDetailedNews(self):
        res = requests.get(self.NewsLink[self.counter])
        soup = BeautifulSoup(res.content, 'html.parser')
        self.content = soup.find_all("div", class_="details-content-story")[-1].get_text()
        #print(self.content)


\