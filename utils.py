import time
import random
import os

from bs4 import BeautifulSoup
import requests
import datetime

def get_article(url):
    html_page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(html_page.text, "html.parser")
    article = soup.find_all('tr')
    return article


def get_URL(month, year):
    url = "https://www.gismeteo.ru/diary/4618/" + \
          str(year) + "/" + str(month) + "/"
    return url


def get_data(article, year, mounth):
    date = article.find("td", class_="first").text
    temp = article.find("td", class_="first_in_group").text
    wind = article.find("span").text
    pressure = list(article.find_all("td"))
    pressure = str(pressure[2].text)
    data = str(datetime.date(int(year), int(mounth), int(date))) +"; " + "Day:" + temp + ", " + wind + ", " + pressure
    return data


def get_data_evening(article):
    temp = list(article.find_all("td"))
    temp = str(temp[6].text)
    pressure = list(article.find_all("td"))
    pressure = str(pressure[7].text)
    data = " Evening:" + temp + ", " + pressure
    return data


def write_day(data, path_to_csv=os.path.join("PYTHON", "dataset.csv")):
    file_name = open("dataset.csv", "a", encoding="utf-8")
    file_name.write(data)
    file_name.write("\n")


def make_dir():
    if not os.path.isdir("PYTHON"):
        os.mkdir("PYTHON")


def get_time():
    value = random.random()
    scaled_value = 1 + (value * 4)
    print("Time sleep:", scaled_value)
    time.sleep(scaled_value)


def run(path_to_csv=os.path.join("PYTHON", "dataset.csv")):
    #make_dir()
    file_name = open("dataset.csv", "w", encoding="utf-8")
    months = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]       
    year = 2022
    month = 9
    while year != 2008:
        while month != 0:
            article = get_article(get_URL(month, year))
            for i in range(2, len(article) - 1):
                write_day(get_data(article[i], year, month) + get_data_evening(article[i]))
            print("Parsing of", months[month], year)
            get_time()
            month -= 1
        month = 12
        year -= 1
    file_name.close()
