import time
import datetime
import threading

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.keys import Keys

from conversions import *
from alarm import *
from os import system

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from IPython.display import display
# lxml required for selenium
# simpleaudio required for alarms


class Crawler:

    # Initiating null variables
    searchUrl = None
    driver = None
    running = False
    urlArray = []
    previousFrames = []
    chrome_options = Options()

    testingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=Mother%27s+Sorrow&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=18&ItemTraitID=13&ItemQualityID=&IsChampionPoint=true&IsChampionPoint=false&LevelMin=160&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000'
    fastChangingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='

    def __init__(self, url=None):
        self.searchUrl = url

        # Local chrome folder
        self.chrome_options.binary_location = 'ChromeStandalone/App/Chrome-bin/chrome.exe'

        # Setting up a Chrome session
        debug = False
        if not debug:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
            print("*parameters applied*")

        # Create a new Chrome session
        self.driver = webdriver.Chrome('chromedriver.exe', options=self.chrome_options)

    def open_pages(self):
        """Method that opens all the urls in the chrome browser"""
        self.driver.get(self.urlArray[0])
        for i in range(1, len(self.urlArray)):
            self.driver.execute_script("window.open();")
            self.driver.switch_to.window(self.driver.window_handles[i])
            self.driver.get(self.urlArray[i])
        self.driver.switch_to.window(self.driver.window_handles[0])

    def refresh_pages(self):
        """Method that refreshes all tabs"""
        self.driver.refresh()
        for i in range(1, len(self.urlArray)):
            self.driver.switch_to.window(self.driver.window_handles[i])
            self.driver.refresh()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def add_url(self, url: str):
        """Method that adds a url to the url array"""
        self.urlArray.append(url)

    def request_items_from_urls(self):
        """Method that requests items from all tabs"""
        self.running = True
        while self.running is True:
            #time.sleep(5)
            # pull-left load spinner
            WebDriverWait(self.driver, 60).until(
                ExpectedConditions.invisibility_of_element_located((By.CLASS_NAME, "pull-left load spinner")))
            #WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.ID, 'search-result-view')))
            time.sleep(5)
            content, found = self.request_item(0)
            print(content[0])
            # here we should send it over to the gui
            for i in range(1, len(self.urlArray)):
                self.driver.switch_to.window(self.driver.window_handles[i])
                WebDriverWait(self.driver, 60).until(
                    ExpectedConditions.invisibility_of_element_located((By.CLASS_NAME, "pull-left load spinner")))
                time.sleep(5)
                #WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.ID, 'search-result-view')))
                try:
                    content, found = self.request_item(i)
                    print(content[0])
                except:
                    print("No items found")
                # here we should send it over to the gui
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("------------------------------")
            time.sleep(2)
            self.refresh_pages()


    def request_item(self, position:int):

        # while 1:
        # driver.execute_script("window.open();")
        # driver.switch_to_window(driver.window_handles[0])
        # Load the web page
        # self.driver.get(self.searchUrl)
        # Wait for the page to fully load
        # driver.implicitly_wait(10)
        # time.sleep(10)
        content = []
        found = False
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
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
        content.append(pageFrames)
        #print("\n\n*-----------------------------------------------------*")
        #display(pageFrames)

        if len(self.previousFrames) == len(self.urlArray):
            resultFrames = dataframe_difference(pageFrames, self.previousFrames[position], which='left_only')
            #print("\n-------------------------------------------------------")
            if resultFrames.empty is False:
                # display new items
                content.append(resultFrames)
                #display(resultFrames)

                # notify
                found = True
                sound = threading.Thread(target=sound_alarm())
                sound.start()
                sound.join()
            else:
                # timestamp to notify the user when was the last time a request took place
                print("No new queries found in this search. ", datetime.datetime.now())
        # print("\n*-----------------------------------------------------*\n\n\n")
        # update previous dataframe for comparison
        self.previousFrames.insert(position, pageFrames)
        return content, found
        # close browser
        # self.driver.quit()

