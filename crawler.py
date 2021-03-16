import os
import time
import datetime
import threading
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.keys import Keys

from conversions import *
from alarm import *

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from IPython.display import display
# lxml required for selenium
# simpleaudio required for alarms
from observer_paradigm import Subject, Observer


def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method

class Crawler(Subject):

    # Initiating null variables
    searchUrl = None
    driver = None
    running = False
    urlArray = []
    previousFrames = []
    chrome_options = Options()
    content = None
    found = False
    position = -1
    _observers: List[Observer] = []
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    testingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=Mother%27s+Sorrow&ItemCategory1ID=1&ItemCategory2ID=2&ItemCategory3ID=18&ItemTraitID=13&ItemQualityID=&IsChampionPoint=true&IsChampionPoint=false&LevelMin=160&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax=20000'
    fastChangingUrl = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?SearchType=Sell&ItemID=&ItemNamePattern=mother%27s+sorrow&ItemCategory1ID=&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax=&AmountMin=&AmountMax=&PriceMin=&PriceMax='

    def __init__(self, url=None):
        self.searchUrl = url

        # Local chrome folder
        self.chrome_options.binary_location = self.ROOT_DIR + '/ChromeStandalone/App/Chrome-bin/chrome.exe'

        # Setting up a Chrome session
        debug = True
        if not debug:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
            print("*parameters applied*")

        # Create a new Chrome session
        self.driver = webdriver.Chrome(self.ROOT_DIR +'/chromedriver.exe', options=self.chrome_options)

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
        if self.running is False:
            self.urlArray.append(url)

    def add_url(self, urls: []):
        """Method that adds a url to the url array"""
        self.urlArray = urls

    def delete_url(self, position):
        """Method that removes a url from the url array"""
        if self.running is False:
            self.urlArray.pop(position)

    @synchronized_method
    def stop_search(self):
        """Method that starts the process of gradually stopping the search. """
        """Note that the method is synchronized in order to pause the thread. """
        self.running = False

    def request_items_from_urls(self):
        """Method that requests items from all tabs"""
        self.running = True
        self.open_pages()
        while self.running is True:
            # pull-left load spinner
            WebDriverWait(self.driver, 60).until(
                ExpectedConditions.invisibility_of_element_located((By.CLASS_NAME, "pull-left load spinner")))
            time.sleep(5)
            self.position = 0
            try:
                self.content, self.found = self.request_item(0)
            except KeyError:
                self.content = None
                self.found = False
            self.notify()
            #print(content[0])
            for i in range(1, len(self.urlArray)):
                self.driver.switch_to.window(self.driver.window_handles[i])
                WebDriverWait(self.driver, 60).until(
                    ExpectedConditions.invisibility_of_element_located((By.CLASS_NAME, "pull-left load spinner")))
                time.sleep(5)
                self.position = i
                try:
                    self.content, self.found = self.request_item(i)
                    #print(content[0])
                except KeyError:
                    self.content = None
                    self.found = False
                self.notify()
                #print("\n- Either no items were found, or the page failed to load in time. -\n")
                # here we should send it over to the gui
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(2)
            self.refresh_pages()
        # Clearing saved data frames
        self.previousFrames = []
        self.urlArray = []

    def request_item(self, position:int):
        # read all tables from html
        self.content = []
        self.found = False
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
        self.content.append(pageFrames)
        #print("\n\n*-----------------------------------------------------*")
        #display(pageFrames)
        # This check is to see if it has any previous data to compare it to
        if len(self.previousFrames) == len(self.urlArray):
            resultFrames = dataframe_difference(pageFrames, self.previousFrames[position], which='left_only')
            #print("\n-------------------------------------------------------")
            if resultFrames.empty is False:
                # display new items
                self.content.append(resultFrames)
                #display(resultFrames)

                # notify
                self.found = True
                sound = threading.Thread(target=sound_alarm())
                sound.start()
                sound.join()
            else:
                # timestamp to notify the user when was the last time a request took place
                print("No new queries found in this search. ", datetime.datetime.now())
        # print("\n*-----------------------------------------------------*\n\n\n")
        # update previous dataframe for comparison
        self.previousFrames.insert(position, pageFrames)
        return self.content, self.found
        # close browser
        # self.driver.quit()

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)
