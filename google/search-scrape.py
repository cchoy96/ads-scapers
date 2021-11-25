#!/usr/bin/python3

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
import time
import csv
import pandas as pd
import random

DEBUG = False
outpath = 'outputs/google-search-ads.csv'

def writeToDisk(ads, initialize=False):
    mode = 'w+' if initialize else 'a'
    with open(outpath, mode) as f:
        writer = csv.writer(f, delimiter=',')
        if initialize: # write header
            writer.writerow(['AdText', 'Category', 'Platform'])
        for adText, isPolitical in ads:
            category = 'political' if isPolitical else 'non-political'
            writer.writerow([adText, category, 'Google'])

def scrape_search_ads(queries, newFile):
    count = 0
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    writeToDisk([], newFile) # initialize output file

    for query in queries:
        with webdriver.Chrome(options=options) as driver:
            wait = WebDriverWait(driver, 10) 
            driver.get("https://google.com/ncr")
            
            ## Load Page ##
            driver.find_element(By.NAME, "q").send_keys(query + Keys.RETURN)
            wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3")))
            driver.execute_script("window.scrollTo(0, 200);") # just adding some human behavior
            time.sleep(2)

            ## Scrape ads from page ##
            ads = [] # list of tuples (adText: String, isPolitical: boolean)
            adBlock = driver.find_elements(By.XPATH, "//*[@id='tads']//div[@data-text-ad='1']")
            print("Found {n} ads for query: {q}".format(n=len(adBlock), q=query))
            for ad in adBlock:
                political = "Paid for by" in ad.text # all Google political ads required to have this disclosure in the adText
                # Source: https://support.google.com/adspolicy/answer/6014595?hl=en#zippy=%2Celection-ads-in-the-united-states
                adText = ad.find_element(By.XPATH, "./div/div[2]").text.strip().encode("ascii","ignore").decode("ascii")
                adText.replace('\n', ' ').replace(',', '')
                if DEBUG:
                    print("\t" + adText)
                ads.append((adText, political))
        writeToDisk(ads)
        count += len(ads)
    return count

def remove_duplicates():
    df = pd.read_csv(outpath)
    before = len(df.index)
    df.drop_duplicates(subset=['AdText'], keep='first', inplace=True)
    df.to_csv(outpath, index=False)
    dropped = before - len(df.index)
    return dropped

def main():
    with open("google/search_queries.txt", 'r') as f:
        qs = [line.strip() for line in f.readlines()]
        if '===' in qs: # search only terms before this break sequence in queries file
            qs = qs[:qs.index('===')]
        for line in f.readlines():
            if line == "===": break 
            qs.append(line.strip())
    if DEBUG: print(qs)
    c = scrape_search_ads(qs, False)
    d = remove_duplicates()
    print("DONE. Scraped {c} ads. Dropped {d} duplicates. Total: {t} ads".format(c=c, d=d, t=c-d))

main()