from tkinter import *
from tkinter import ttk
from tab import Tab

from crawler import Crawler
from observer_paradigm import Observer, Subject
from alarm import *

import threading


class TTCc_GUI(Observer):
    t = None

    def __init__(self, master, crawler):
        self.master = master
        self.master.title("TCCcrawler")

        self.buttons_frame = Frame(master)
        self.buttons_frame.pack(side=TOP)

        self.crawler = crawler
        self.crawler.attach(self)

        # Start/Stop searches in all tabs
        self.start_stop_button = Button(self.buttons_frame, text="Start", command=self.start_action)
        # self.start_stop_button['text'] = "Updated Text" # How to change button text
        self.start_stop_button.pack(side=LEFT, padx=5, pady=5)

        self.new_tab_button = Button(self.buttons_frame, text="New Tab", command=self.new_tab)
        self.new_tab_button.pack(side=LEFT, padx=5, pady=5)

        self.compose_url_button = Button(self.buttons_frame, text="Compose URL")
        self.compose_url_button.pack(side=RIGHT, padx=5, pady=5)

        self.tab_frame = ttk.Notebook(master)
        self.tab_frame.pack(expand=True, fill=BOTH, pady=10, padx=10)

        self.tab_list = []  # Will contain all the tabs created for recovery purposes
        self.base_tab = Tab(self.tab_frame, self.tab_list, "Base Tab")  # Default Tab, might be removed in the future
        self.tab_list.append(self.base_tab)

    def start_action(self):
        # Changes the button appearance
        if self.start_stop_button['text'] == "Start":  # If it's supposed to start
            self.start_stop_button['text'] = "Stop"
            # Gathering urls
            url_list = []
            for tab in self.tab_list:
                url = tab.url_field.get()
                tab.tab_retitle(url)
                url_list.append(url)
            self.crawler.add_url(urls=url_list)
            self.t = threading.Thread(target=self.crawler.request_items_from_urls)
            self.t.start()
        else:  # If it's supposed to stop
            self.start_stop_button['text'] = "Start"

    def new_tab(self):
        # Tabs have a temporary name for identification
        self.tab_list.append(Tab(self.tab_frame, self.tab_list, f"Tab {self.tab_frame.tabs()[-1]}"))

    def update(self, subject: Subject) -> None:
        print(self.crawler.urlArray)
        print("Reacted to the event")
        if self.crawler.content is not None:
            self.tab_list[self.crawler.position].text_field.insert(END, "\n\n")
            self.tab_list[self.crawler.position].text_field.insert(END, self.crawler.content[0])
            print("Found = ", self.crawler.found)
            if self.crawler.found is True:
                self.tab_list[self.crawler.position].text_field.insert(END, '\n\n')
                self.tab_list[self.crawler.position].text_field.insert(END, self.crawler.content[1])
                sound = threading.Thread(target=sound_alarm())
                sound.start()
                sound.join()
        else:
            self.tab_list[self.crawler.position].text_field.insert(END, "\nNo items found.\n")
        self.tab_list[self.crawler.position].text_field.see(END)

root = Tk()
crawler = Crawler()
my_gui = TTCc_GUI(root, crawler)
root.mainloop()
