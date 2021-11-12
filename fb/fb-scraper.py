#!/usr/bin/python3

import urllib.parse
from requests_html import HTMLSession 

def build_query(q, ad_type="political_and_issue_ads"):
    getVars = {'country':'US', 'sort_data[direction]':'desc', 'sort_data[mode]':'relevancy_monthly_grouped'}
    getVars['active_status'] = 'all'
    getVars['search_type'] = 'keyword_unordered'
    getVars['media_type'] = 'none'
    getVars['ad_type'] = ad_type
    getVars['q'] = q
    return "https://www.facebook.com/ads/library/?" + urllib.parse.urlencode(getVars, encoding='utf-8')

def get_html_response(url):
    session = HTMLSession()
    r = session.get(url) # HTML Response
    r.html.render()
    return r

# https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=US&q=biden&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=all
url = build_query("biden")
r = get_html_response(url)
print(r.html.text)

