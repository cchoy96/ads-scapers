#!/usr/bin/python3

## REQUESTS LIBRARIES
import requests
from requests_html import HTMLSession

def get_static_html():
    '''EXAMPLE: getting html from a static webpage. We need dyanamic for the most part.'''
    url = "https://realpython.github.io/fake-jobs/"
    page = requests.get(url)
    print(page.text)

def get_dynamic_html():
    '''EXAMPLE: request-html render and search'''
    url = "https://www.epochconverter.com/clock"
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    p = r.html.search("GMT{}EpochMilliseconds")
    # p = r.html.text
    print(p)

## SELENIUM 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


def run_selenium_basic_google_search():
    '''Opens Chromium instance, searches for text, returns text of first result.'''
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get("https://google.com/ncr")
        driver.find_element(By.NAME, "q").send_keys("bubbles" + Keys.RETURN)
        first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3")))
        print(first_result.get_attribute("textContent"))

url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=US&q=biden&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=none"
def run_fb_ads_search():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get(url)
        ##################
        for _ in range(5): # need to do something a couple of times to get consistent number of elements. idk. 
            # Parse through all HTML content in <body>
            html = driver.execute_script("return document.body.outerHTML;")
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.find_all('div')
            print(len(divs))
            # for i,div in enumerate(divs):
            #     if i > 20: break
            #     print(div, "\n\n")

        #############
        # SEARCH BY DIV. All ads in one DIV in nested sub-divs we could iterate through with BS4.
        # elements = driver.find_elements(By.CLASS_NAME, "fb_content clearfix")
        # print(len(elements))
        # for i,elem in enumerate(elements):
        #     print(elem.text, "\n\n")

        #######
        # elements = driver.find_elements(By.TAG_NAME, 'div')
        # print(len(elements))
        # for i,e in enumerate(elements):
        #     if i > 14: break
        #     try:
        #         print(i, e.get_attribute('innerHTML'), "\n\n")
        #     except:
        #         pass

        # item = elements[14].get_attribute('innerHTML') 
        # print(item)
        # soup = BeautifulSoup(item, 'html.parser') 
        # print(soup.prettify)

def better_fb_search():
    '''Attempt at extracting by means better than iterating through endless divs'''
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 10) 
        driver.get(url)
        ############
        # SEARCH BY XPATH ID
        ids = driver.find_elements(By.XPATH, '//*[@id]')
        print(len(ids))
        for ii in ids:
            #print ii.tag_name
            print(ii.get_attribute('id'))

        #############
        # ROLES to search for = gridcell, presentation, button
        cells = driver.find_elements(By.CSS_SELECTOR, "a[role='gridcell']")
        print(len(cells))
        # for i, cell in enumerate(cells):
        #     try:
        #         print(i, cell.get_attribute('innerHTML'))
        #     except:
        #         pass 


run_fb_ads_search()
