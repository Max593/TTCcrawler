import pandas as pd
import time
from conversions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from IPython.display import display

chrome_options = Options()
# Local chrome folder
chrome_options.binary_location = './ChromeStandalone/chrome'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='


def request_item():

    # Create a new Chrome session
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # Load the web page
    driver.get(url)

    # Wait for the page to fully load
    #driver.implicitly_wait(10)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tables = soup.find_all('table')
    dfs = pd.read_html(str(tables))


    #pretty print settings
    pd.set_option('display.max_rows', None) 
    pd.set_option('display.max_columns', None) 
    pd.set_option('display.width', 5000) 
    pd.set_option('display.colheader_justify', 'center') 
    pd.set_option('display.precision', 2) 

    # delete empty rows
    for i in range(len(dfs)):
        df = dfs[i]        
        df = df[df['Item'].notna()]
        dfs[i] = df

    pageFrames = pd.concat(dfs) # Joins all tables on page
    pageFrames = pageFrames.reset_index(drop=True) # Creates a unified index
    pageFrames = pageFrames.iloc[1:] # Deletes column names
    
    # Final Price column with int values
    prices = [] 
    for price in pageFrames["Price"]:
        prices.append(price_to_int(price))
    pageFrames["Final Price"] = prices

    # Time
    last_seen_minutes = []
    for last_seen in pageFrames["Last Seen"]:
        last_seen_minutes.append(time_to_int(last_seen))
    pageFrames["Last Seen Minutes"] = last_seen_minutes

    display(pageFrames)

    # Last step
    driver.quit()
