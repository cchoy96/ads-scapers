#!/bin/usr/python3

import pandas as pd 
import csv 
import glob 

files = glob.glob("outputs/fbAds-*.csv")
outfile = "outputs/fbAds.csv"

with open(outfile, "w+") as f:
    writer = csv.writer(f)
    writer.writerow(["AdText", "Category", "Platform", "Keywords"])

for file in files:
    df = pd.read_csv(file)
    keyword = file.split('.')[0].split('-')[1]
    df["Keywords"] = keyword
    df.AdText = df.AdText.str.strip()
    df.to_csv(outfile, mode='a', header=False, index=False)

df = pd.read_csv(outfile)
df.drop_duplicates(subset=['AdText'], inplace=True)
df.to_csv(outfile, index=False)