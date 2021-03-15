from tkinter import *
from tkinter import ttk
from tab import Tab


class TTCc_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("TCCcrawler")

        self.buttons_frame = Frame(master)
        self.buttons_frame.pack(side=TOP)

        # Start/Stop searches in all tabs
        self.start_stop_button = Button(self.buttons_frame, text="Start")
        # self.start_stop_button['text'] = "Updated Text" # How to change button text
        self.start_stop_button.pack(side=LEFT, padx=5, pady=5)

        self.new_tab_button = Button(self.buttons_frame, text="New Tab", command=self.new_tab)
        self.new_tab_button.pack(side=LEFT, padx=5, pady=5)

        self.compose_url_button = Button(self.buttons_frame, text="Compose URL")
        self.compose_url_button.pack(side=RIGHT, padx=5, pady=5)

        self.tab_frame = ttk.Notebook(master)
        self.tab_frame.pack(expand=True, fill=BOTH, pady=10, padx=10)

        self.tab_list = []  # Will contain all the tabs created for recovery purposes
        self.base_tab = Tab(self.tab_frame, "Base Tab")  # Default Tab, might be removed in the future
        self.tab_list.append(self.base_tab)

    def new_tab(self):
        # Tabs have a temporary name for identification
        self.tab_list.append(Tab(self.tab_frame, f"Tab {self.tab_frame.tabs()[-1]}"))


root = Tk()
my_gui = TTCc_GUI(root)
root.mainloop()
