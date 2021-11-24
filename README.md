# ads-scapers
Collection of web measurement scripts for scraping political ads off of platforms.

## Usage 
There are scrapers here for both [Facebook Ads Library](https://www.facebook.com/ads/library/) and [Google Transparency Reports](https://transparencyreport.google.com/political-ads/region/US).

### Google
To scrape political ads from Google, I built a web scraper to extract text ads from their Transparency Report. Currently, Google organizes the ads in the transparency report by country and advertiser. The `transparency-report-scraper.py` allows for extraction of ads from advertiser pages. Google Transparency reports currently only show political advertisers and their political advertisements. To get a list of advertiser IDs for the web scraper, download Google's [political ads transparency bundle](https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip) and process it with `format-transparency-bundle.py`.

### Facebook (Meta)
The web scraper I built scrapes ads from Facebook Ads Library. You can feed the scraper a keyword and it will scrape all text ads for that keyword under both political and non-political categories. Given how Facebook renders its ad pages, you can also configure the script to scrape more ads per keyword per category by having the script scroll further down the each page of ads (thus loading more ads) before scraping. 

# Developer Notes
## Imports
requests: `$ python3 -m pip install requests`
beautifulsoup4: `$ python3 -m pip install beautifulsoup4`
requests-html: `$ python3 -m pip install requests_html`
selenium: `$pythong3 -m pip install selenium`

## Tutorials
[Beautiful Soup Web Scraper](https://realpython.com/beautiful-soup-web-scraper-python/#challenges-of-web-scraping)
[requests-html library usage](https://github.com/psf/requests-html)
[Selenium](https://www.selenium.dev/documentation/)

## Various Notes
- running requests-html:HTMLSession().get().html.render() the first time will install chromium to render it.
- todo: check out selenium
- https://www.freecodecamp.org/news/webscraping-in-python/
- xpath cheatsheet = https://devhints.io/xpath 
- xpath syntax/tutorail = https://www.w3schools.com/xml/xpath_syntax.asp
- scrolling in selenium python = https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
- XPATHs can be obtained by inspecting page, right-clicking on desired block and hitting Copy > XPath. 