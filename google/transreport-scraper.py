#!/usr/bin/python3

import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options

def build_tr_query(advertiserId):
    baseurl = "https://transparencyreport.google.com/political-ads/advertiser/{aId}?campaign_creatives=start:{start};end:{end};spend:;impressions:;type:3;sort:3&lu=campaign_creatives"
    start = 1527638400000
    end = 1635897599999
    return baseurl.format(aId=advertiserId, start=start, end=end)


# url = "https://transparencyreport.google.com/political-ads/advertiser/AR108481940364984320?campaign_creatives=start:1527638400000;end:1635897599999;spend:;impressions:;type:3;sort:3&lu=campaign_creatives"

def scrape(url):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get(url)
        for _ in range(10): # need to render several times to collect all elements
            html = driver.execute_script("return document.body.outerHTML;")
            soup = BeautifulSoup(html, "html.parser")
        # print(soup.prettify())
        ads = soup.find_all('text-ad')
        for i,ad in enumerate(ads):
            print(i, ad.prettify())
            # print(i,ad.getText())

url = build_tr_query('AR108481940364984320')
print(url)
scrape(url)
