#!/usr/bin/python3

import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
import csv

DEBUG_MODE = False
advIds = ['AR108481940364984320', 'AR105500339708362752', 'AR458000056721604608', 'AR488306308034854912', 'AR249615527784218624', 'AR128018337845215232', \
    'AR25310001757159424', 'AR194446432348930048', 'AR230475229367894016', 'AR276637125548441600', 'AR432709227698454528', 'AR383080296477622272', 
    'AR462410610177474560', 'AR157291735423123456', 'AR568293442493349888', 'AR470291909525372928', 'AR101121809528651776'] # up to Pete for America

def scrape(advertiserId):
    def build_query(advertiserId):
        baseurl = "https://transparencyreport.google.com/political-ads/advertiser/{aId}?campaign_creatives=start:{start};end:{end};spend:;impressions:;type:3;sort:3&lu=campaign_creatives"
        start = 1527638400000
        end = 1635897599999
        url = baseurl.format(aId=advertiserId, start=start, end=end)
        if DEBUG_MODE:
            print(url)
        return url

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    adTexts = []
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get(build_query(advertiserId))
        for _ in range(10): # need to render several times to collect all elements
            html = driver.execute_script("return document.body.outerHTML;")
            soup = BeautifulSoup(html, "html.parser")
        ads = soup.find_all('text-ad')
        adTexts = [ad.getText() for ad in ads]
    return adTexts

def main():
    count = 0
    with open('outputs/tr-adText.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['AdText', 'Category', 'Platform'])
            for aId in advIds:
                adTexts = scrape(aId)
                print(aId, ':', len(adTexts))
                count += len(adTexts)
                for ad in adTexts:
                    if DEBUG_MODE:
                        print(ad)
                    writer.writerow([ad, 'political', 'Google'])
    print("DONE. Ads Scraped: ", count)

main()
