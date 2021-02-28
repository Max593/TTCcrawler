import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

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
    print(dfs[0]["Location"])

    # Last step
    driver.quit()
