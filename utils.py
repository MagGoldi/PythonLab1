from bs4 import BeautifulSoup
import os
import requests
import time
import random


def get_article(URL):
    html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(html_page.text, "html.parser")
    article = soup.find_all('tr')
    return article


def get_URL(month, year):
    URL = "https://www.gismeteo.ru/diary/4618/" + \
          str(year) + "/" + str(month) + "/"
    return URL


def get_data(article):
    date = (article.find("td", class_="first").text)
    temp = (article.find("td", class_="first_in_group").text)
    wind = (article.find("span").text)
    pressure = list(article.find_all("td"))
    pressure = str(pressure[2].text)
    data = date + ") " + "День:" + temp + ", " + wind + ", " + pressure
    return data


def get_data_evening(article):
    temp = list(article.find_all("td"))
    temp = str(temp[6].text)
    pressure = list(article.find_all("td"))
    pressure = str(pressure[7].text)
    data = " Вечер:" + temp + ", " + pressure
    return data


def write_day(data):
    file = open("C:/PYTHON/dataset.csv", "w", encoding="utf-8")
    file.write(data)
    file.write("\n")


def write_month(months, month, year):
    file = open("C:/PYTHON/dataset.csv", "w", encoding="utf-8")
    file.write(months[month])
    file.write(str(year))
    file.write("\n")


def make_dir():
    if not os.path.isdir("PYTHON"):
        os.mkdir("PYTHON")
    if not os.path.isdir("dataset.csv"):
        os.mkdir("dataset.csv")


def get_time():
    value = random.random()
    scaled_valie = 1 + (value * 4)
    print("Time sleep:", scaled_valie)
    time.sleep(scaled_valie)


def run():                                                          
    file = open("C:/PYTHON/dataset.csv", "w", encoding="utf-8")
    months = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    year = 2022
    month = 9
    while year != 2007:
        while month != 0:
            article = get_article(get_URL(month, year))
            write_month(months, month, year)
            for i in range(2, len(article) - 1):
                write_day(get_data(article[i]) + get_data_evening(article[i]))
            print("Parsing of", months[month], year)
            get_time()
            month -= 1
        month = 12
        year -= 1
    file.closed
