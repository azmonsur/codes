import requests
import urllib.request as urllib2
from lxml import html
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64"} 
url = "https://en.m.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_outbreak"

session_requests = requests.session()
request = urllib2.Request(url, None, header)

request = urllib2.urlopen(request).url
result = session_requests.get(request)

soup = bs(result.text, "html.parser")
items = soup.select("table.plainrowheaders tr")

covid = []
for item in items:
    covid.append(item.text.strip("\n"))
    
df = pd.DataFrame()
country = []
case = []
death = []
recovery = []


for i in covid:
    iSplit = i.split("\n")
    if iSplit[0] == "\xa0":
    	
    	while "" in iSplit: 
    	   iSplit.remove("")
    	   
    	case.append(iSplit[2])
    	death.append(iSplit[3])
    	recovery.append(iSplit[4])
    	
    	if "[" in iSplit[1]:
    		pos = iSplit[1].find("[")
    		country.append(iSplit[1][:pos])
    	else:
    		country.append(iSplit[1])
    	
df["Countries"] = country
df["Cases"] = case
df["Deaths"] = death
df["Recovs"] = recovery

df.index = np.arange(1, len(df) + 1)

df.to_excel("corona.xls")
print("Web at: {} scraped successfully".format(url))
