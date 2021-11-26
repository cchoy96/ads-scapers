#!/usr/bin/python3

import time
import csv
import glob
import pandas as pd
import urllib.parse
from os.path import exists
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

AD_TYPE = {
    'all': 'all',
    'political': 'political_and_issue_ads',
    'housing': 'housing_ads',
    'employment': 'employment_ads',
    'credit': 'credit_ads'
}

outfile = "outputs/fbAds.csv"

def fb_scrape(keyword, ad_type):
    print("Scraping {q}//{t}...".format(q=keyword, t=ad_type))
    ad_texts = set()

    def build_query(q, type=AD_TYPE['political']):
        # fb.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=US&q=biden&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=none
        getVars = {'country':'US', 'sort_data[direction]':'desc', 'sort_data[mode]':'relevancy_monthly_grouped'}
        getVars['active_status'] = 'all'
        getVars['search_type'] = 'keyword_unordered'
        getVars['media_type'] = 'none'
        getVars['ad_type'] = type
        getVars['q'] = q
        return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(getVars, encoding='utf-8')
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        WebDriverWait(driver, 10) 
        url = build_query(keyword, ad_type)
        print(url)
        driver.get(url)

        # Scroll to the bottom a bunch to load older months
        for _ in range(10): 
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom of page
        
        # Grab all ads on page
        months = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/div[1]/div/div/div[position()>3]')
        for month in months:
            try:
                ads = month.find_elements(By.XPATH, './div[3]/div[1]/div')
                for ad in ads:
                    text = ad.find_element(By.XPATH, './div/div[3]/div/div/div[2]').text.strip().encode("ascii","ignore").decode("ascii")
                    text = text.replace("\n"," ").replace(",", '').strip()
                    if text:
                        ad_texts.add(text)
            except Exception as e:
                print("[WARN] Something went wrong")
            
            n = len(ad_texts)
            print("\tAds scraped: ", n)
            if n > 500: break  # just to avoid memory issues
    return ad_texts

def remove_duplicates(filepath):
    df = pd.read_csv(filepath)
    df.drop_duplicates(subset=['AdText'], inplace=True)
    df.to_csv(filepath, index=False)

def condense_outputs():
    ''' Deprecated function used for condensing all the fbAds-{keyword}.csv files into one'''
    files = glob.glob("outputs/fbAds-*.csv")

    with open(outfile, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["AdText", "Category", "Platform", "Keywords"])

    for file in files:
        df = pd.read_csv(file)
        keyword = file.split('.')[0].split('-')[1]
        df["Keywords"] = keyword
        df.AdText = df.AdText.str.strip()
        df.to_csv(outfile, mode='a', header=False, index=False)

    remove_duplicates(outfile)

def main():
    # keywords = ['biden','trump']
    # keywords = ['guns', 'america', 'abortion']
    # keywords = ['jobs', 'infrastructure', 'environment', 'privacy', 'economy']
    keywords = ['bernie']

    if not exists(outfile):
        with open(outfile, 'w+') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['AdText', 'Category', 'Platform', 'Keyword'])
    
    with open(outfile, 'a') as f:
        writer = csv.writer(f, delimiter=',')
        for keyword in keywords:
            count = 0
            # Scrape and write political ads
            ad_texts = fb_scrape(keyword, AD_TYPE['political'])
            count += len(ad_texts)
            for ad_text in ad_texts:
                writer.writerow([ad_text, 'political', 'Facebook', keyword])
            
            # Scrape and write non-political ads
            non_political_types = ['housing', 'employment', 'credit']
            for type in non_political_types:
                ad_texts = fb_scrape(keyword, AD_TYPE[type])
                for ad_text in ad_texts:
                    writer.writerow([ad_text, 'non-political', 'Facebook', keyword])
                    count += len(ad_texts)
            print("Total ads scraped for keyword: {q} = {n}\n".format(q=keyword, n=count))
    remove_duplicates(outfile)

main()