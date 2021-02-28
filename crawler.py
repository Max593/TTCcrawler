import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
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
    #   print(dfs[0])
    #print(dfs[0]["Location"])

    pd.set_option('display.max_rows', None) 
    pd.set_option('display.max_columns', None) 
    pd.set_option('display.width', 2000) 
    pd.set_option('display.colheader_justify', 'center') 
    pd.set_option('display.precision', 2) 

    for i in range(len(dfs)):
        df = dfs[i]        
        df = df[df['Item'].notna()]
        df = df.reset_index(drop=True)
        dfs[i] = df

    pageFrames = pd.concat(dfs)
    pageFrames = pageFrames.reset_index(drop=True)
    pageFrames = pageFrames.iloc[1:]
    display(pageFrames)

    # Last step
    driver.quit()
