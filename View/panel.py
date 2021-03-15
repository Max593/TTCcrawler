from tkinter import *
from tkinter import ttk


class TTCc_GUI:
    class Tab:
        def __init__(self, tab_frame, title="New Tab"):
            self.tab_frame = tab_frame
            tab = Frame(self.tab_frame)
            tab.pack(expand=True, fill=BOTH)
            self.tab_frame.add(tab, text=title)
            self.tab_content_init(tab)

        def tab_content_init(self, tab):
            top_Frame = Frame(tab)
            top_Frame.pack(side=TOP, padx=10, pady=5)
            bottom_Frame = Frame(tab)
            bottom_Frame.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10, pady=5)

            url_field = Entry(top_Frame, widt=150)
            url_field.pack(side=LEFT, fill='x', padx=10)

            text_field = Text(bottom_Frame)
            text_field.pack(side=BOTTOM, expand=True, fill=BOTH)

            delete_tab_button = Button(top_Frame, text="Delete Tab", command=self.deleteTab)
            self.tab_frame.select(self.tab_frame.tabs()[-1])  # Jumps to the latest change
            if self.tab_frame.index(self.tab_frame.select()) == 0:
                delete_tab_button["state"] = "disable"
                delete_tab_button['text'] = "Disabled"
            delete_tab_button.pack(side=RIGHT)

        def deleteTab(self):
            self.tab_frame.forget(self.tab_frame.select())

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
        self.base_tab = self.Tab(self.tab_frame, "Base Tab")  # Default Tab, might be removed in the future
        self.tab_list.append(self.base_tab)

    def new_tab(self):
        # Tabs have a temporary name for identification
        self.tab_list.append(self.Tab(self.tab_frame, f"Tab {self.tab_frame.tabs()[-1]}"))
        #self.tab_frame.select(self.tab_frame.tabs()[-1]) # Jumps to the latest change


root = Tk()
my_gui = TTCc_GUI(root)
root.mainloop()