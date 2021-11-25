#!/usr/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd

DEBUG_MODE = False
dir = '/Users/cchoy/Github/ads-scapers/outputs/'
outpath = dir + 'google-political.csv'

def scrape(advertiserId):
    def build_query(advertiserId):
        baseurl = "https://transparencyreport.google.com/political-ads/advertiser/{aId}?campaign_creatives=start:{start};end:{end};spend:;impressions:;type:3;sort:3&lu=campaign_creatives"
        start = 1527638400000
        end   = 1635897600000
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
        adTexts = [ad.getText().strip().encode("ascii","ignore").decode("ascii").replace(',','') for ad in ads]
    return adTexts

def scrape_advertisers(advIds, newFile=False):
    count = 0
    mode = 'w+' if newFile else 'a'
    with open(outpath, mode) as f: 
        writer = csv.writer(f)
        if newFile:
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

def clean_duplicates():
    df = pd.read_csv(outpath)
    before = len(df.index)
    df.drop_duplicates(subset=['AdText'], keep='first', inplace=True)
    print("Dropped {n} duplicate rows.".format(n=before-len(df.index)))
    df.to_csv(outpath, index=False)

def manual_scrape():
    ''' Provide script with advertiser IDs to scrape in a list'''
    advertiser_ids = ['AR108481940364984320', 'AR105500339708362752', 'AR458000056721604608', 'AR488306308034854912', 'AR249615527784218624', 'AR128018337845215232', \
        'AR25310001757159424', 'AR194446432348930048', 'AR230475229367894016', 'AR276637125548441600', 'AR432709227698454528', 'AR383080296477622272', 
        'AR462410610177474560', 'AR157291735423123456', 'AR568293442493349888', 'AR470291909525372928', 'AR101121809528651776']
    print("num advertisers = ", len(advertiser_ids))
    scrape_advertisers(advertiser_ids)

def csv_scrape(new):
    '''Provide cleaned csv file from google-transparency-bundle with Advertiser_ID column'''
    df = pd.read_csv(dir + 'google-political-advertiser_ids.csv')
    df = df.sort_values("Spend_USD", ascending=False)
    advertiser_ids = [id for id in df['Advertiser_ID'].tolist()[:150]] # paginate through advertiser IDs

    print("num advertisers = ", len(advertiser_ids))
    scrape_advertisers(advertiser_ids, new)

csv_scrape(True)
clean_duplicates()