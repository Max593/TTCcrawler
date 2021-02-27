import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='
# Create a new Chrome session
driver = webdriver.Chrome()
# Load the web page
driver.get(url)
# Wait for the page to fully load
#driver.implicitly_wait(10)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'lxml')
tables = soup.find_all('table')
dfs = pd.read_html(str(tables))
#print(dfs[0])
print(dfs[0]["Location"])

# Last step
driver.quit()
