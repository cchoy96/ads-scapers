#!/usr/bin/python3

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

## EXAMPLE: getting html from a static webpage. We need dyanamic for the most part.
# url = "https://realpython.github.io/fake-jobs/"
# page = requests.get(url)
# print(page.text)

## EXAMPLE: request-html render and search
url = "https://www.epochconverter.com/clock"
session = HTMLSession()
r = session.get(url)
r.html.render()
p = r.html.search("GMT{}EpochMilliseconds")
print(p)