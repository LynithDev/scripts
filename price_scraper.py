#!/usr/bin/env python
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests

with open("links.txt", "r") as f:
    links = f.read().splitlines()

table = PrettyTable()
table.field_names = ["Name", "Price", "Provider"]
table.align = "l"

HEADERS = { "USER-AGENT": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0" }

def add(name, price, provider):
    name = name.replace("Karta graficzna", "").replace("Procesor", "").strip()
    table.add_row([name, price, provider])

for link in links:
    if not link.startswith("http"): continue
    page = requests.get(url = link, headers = HEADERS).text

    if link.startswith("https://www.mediaexpert.pl"):
        soup = BeautifulSoup(page, "html.parser")
        title = soup.find("h1", { "class": "is-title" }).string
        priceBox = soup.find("div", { "class": "main-price" });
        price = priceBox.find("span", { "class": "whole" }).string + "," + priceBox.find("span", { "class": "cents" }).string + "" + priceBox.find("span", { "class": "currency"}).string
        add(title, price, "Media Expert")
    if link.startswith("https://www.amazon.pl"):
        soup = BeautifulSoup(page, "lxml")
        title = soup.find("span", { "id": "productTitle" }).string.split(",")[0]
        price = soup.find("span", { "class": "a-offscreen" }).string
        add(str(title), str(price), "Amazon")
        
print(table.get_string())

import datetime
with open("output.txt", "a") as f:
    table.border = False
    table.header = False
    f.write(datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S %Z") + "\n" + table.get_string() + "\n")