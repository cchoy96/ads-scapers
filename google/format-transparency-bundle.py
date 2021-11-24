#!/bin/usr/python3

import pandas as pd
''' 
Formats data found in Google's published google-political-ads-transparency-bundle.zip
Data is filtered and then written to separate files for usage by other scripts like the web scraper. 
'''

dir = '/Users/cchoy/Downloads/google-political-ads-transparency-bundle/'

def get_advertiser_ids():
    advertiser_stats_path = dir + 'google-political-ads-advertiser-stats.csv'
    outpath = 'outputs/google_political_advertiser_ids.csv'
    # Filter and format
    df = pd.read_csv(advertiser_stats_path)
    df = df.drop(df[df.Regions != 'US'].index) 
    df = df[['Advertiser_ID','Advertiser_Name','Total_Creatives','Spend_USD','Regions','Elections']]
    # Write
    print(df.head())
    df.to_csv(outpath)
    print("Number of US Advertisers = ", len(df.index))

def get_creative_urls():
    ad_urls_path = dir + 'google-political-ads-creative-stats.csv'
    outpath = 'outputs/google-political-ad_urls.csv'
    # Filter and format
    df = pd.read_csv(ad_urls_path, dtype={"Regions": "string", "Spend_USD": "string"})
    df = df.drop(df[(df.Regions != 'US') & (df.Ad_Type != 'Text')].index)
    df = df[['Ad_ID', 'Ad_URL', 'Ad_Type', 'Regions', 'Advertiser_ID', 'Advertiser_Name', 'Ad_Campaigns_List', 'Num_of_Days', 
    'Impressions', 'Spend_USD', 'Last_Served_Timestamp', 'Age_Targeting', 'Gender_Targeting', 'Geo_Targeting_Included',
    'Geo_Targeting_Excluded', 'Spend_Range_Min_USD', 'Spend_Range_Max_USD']]
    df = df.head(10_000) # limit number of rows to reduce output filesize
    # Write
    print(df.head())
    df.to_csv(outpath)
    print("Number of US Text Ads = ", len(df.index))

# get_advertiser_ids()
get_creative_urls()