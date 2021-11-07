#!/usr/bin/python3

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_ads():
    url = "https://transparencyreport.google.com/political-ads/advertiser/AR108481940364984320?campaign_creatives=start:1527638400000;end:1635897599999;spend:;impressions:;type:3;sort:3&lu=campaign_creatives"
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
            print(i,ad.getText())
            input()

def scrape_advertisers():
    url = "https://transparencyreport.google.com/political-ads/region/US"
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get(url)
        # advertisers = driver.find_element(By.ID, "top_advertisers")
        elems = driver.find_elements(By.XPATH, "//data-table[@id='top_advertisers']/visualization-container/div[@class='visualization']//tbody/tr")
        print(len(elems))

        # elems = driver.find_elements(By.CLASS_NAME, "google-visualization-table-td")
        for elem in elems:
            # print(elem.text)
            try:
                print(elem.text)
            except:
                pass

scrape_advertisers()