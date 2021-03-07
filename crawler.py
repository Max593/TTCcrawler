import time
import datetime
import threading

from conversions import *
from alarm import *

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from IPython.display import display
# lxml required for selenium
# simpleaudio required for alarms


class Crawler:

    searchUrl = None
    chrome_options = Options()

    testingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=Mother%27s+Sorrow&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=18&ItemTraitID=13&ItemQualityID=&IsChampionPoint=true&IsChampionPoint=false&LevelMin=160&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000'
    fastChangingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='

    def __init__(self, url):
        self.searchUrl = url
        # Local chrome folder
        self.chrome_options.binary_location = 'ChromeStandalone/App/Chrome-bin/chrome.exe'
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

    def request_item(self):
        previousFrames = None

        while 1:
            # Create a new Chrome session
            driver = webdriver.Chrome('chromedriver.exe', options=self.chrome_options)
            # Load the web page
            driver.get(self.searchUrl)
            # Wait for the page to fully load
            # driver.implicitly_wait(10)
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            tables = soup.find_all('table')
            dfs = pd.read_html(str(tables))

            # pretty print settings
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 5000)
            pd.set_option('display.colheader_justify', 'center')
            pd.set_option('display.precision', 2)

            pageFrames = dfs[0]
            pageFrames = pageFrames[pageFrames['Item'].notna()]
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

            # Pretty printing
            # display(pageFrames)

            if previousFrames is not None:
                resultFrames = dataframe_difference(pageFrames, previousFrames, which='left_only')
                if resultFrames.empty is False:
                    # display new items
                    display(resultFrames)

                    # notify
                    sound = threading.Thread(target=sound_alarm())
                    sound.start()
                    sound.join()
                else:
                    # timestamp to notify the user when was the last time a request took place
                    print("No new queries found in this search. ", datetime.datetime.now())
            # update previous dataframe for comparison
            previousFrames = pageFrames
            # close browser
            driver.quit()
            #time.sleep(60)
