import pandas as pd
import time
import threading
from conversions import *
from alarm import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from IPython.display import display

chrome_options = Options()
# Local chrome folder
#chrome_options.binary_location = 'ChromeStandalone/GoogleChromePortable.exe'
chrome_options.binary_location = 'ChromeStandalone/App/Chrome-bin/chrome.exe'
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='
testingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=Mother%27s+Sorrow&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=18&ItemTraitID=13&ItemQualityID=&IsChampionPoint=true&IsChampionPoint=false&LevelMin=160&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000'


def request_item():

    # Create a new Chrome session
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

    # Load the web page
    driver.get(testingUrl)

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
    # for i in range(len(dfs)):
    #    df = dfs[i]
    #    df = df[df['Item'].notna()]
    #    dfs[i] = df

    pageFrames = dfs[0]
    pageFrames = pageFrames[pageFrames['Item'].notna()]
    # pageFrames = pd.concat(dfs) # Joins all tables on page
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


    # Testing
    # print(pageFrames.sort_values(by=['Last Seen Minutes']).head())
    pageFrames = pageFrames.sort_values(by=['Final Price'])
    result = pageFrames[pageFrames["Last Seen Minutes"] == 0].head()
    if len(result) > 0:
        print(result)
        threading.Thread(target=sound_alarm()).start()

    # Last step
    driver.quit()
    time.sleep(300)
