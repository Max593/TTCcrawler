from tkinter import *
from tkinter import ttk


class TTCc_GUI:
    class Tab:
        def __init__(self, number, tab_frame, title="New Tab"):
            self.tab_frame = tab_frame
            self.tab_number = number
            tab = Frame(self.tab_frame)
            tab.pack(expand=True, fill=BOTH)
            self.tab_frame.add(tab, text=title)
            self.tab_content_init(tab)

        @staticmethod
        def tab_content_init(tab):
            top_Frame = Frame(tab)
            top_Frame.pack(side=TOP, padx=10, pady=5)
            bottom_Frame = Frame(tab)
            bottom_Frame.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10, pady=5)

            url_field = Entry(top_Frame, widt=150)
            url_field.pack(side=LEFT, fill='x', padx=10)

            text_field = Text(bottom_Frame)
            text_field.pack(side=BOTTOM, expand=True, fill=BOTH)

            check_button = Button(top_Frame, text="Check!")
            check_button.pack(side=RIGHT)

    def __init__(self, master):
        self.master = master
        self.master.title("TCCcrawler")

        self.buttons_frame = Frame(master)
        self.buttons_frame.pack(side=TOP)

        # Temporary button for adding tabs
        self.test_button = Button(self.buttons_frame, text="NEW TAB", command=self.new_tab)
        self.test_button.pack(side=RIGHT, padx=5, pady=5)

        # Will start a new check for all tabs
        self.check_all = Button(self.buttons_frame, text="Refresh all Tabs")
        self.check_all.pack(side=LEFT, padx=5, pady=5)

        self.tab_frame = ttk.Notebook(master)
        self.tab_frame.pack(expand=True, fill=BOTH, pady=10, padx=10)
        self.tab_list = []  # Will contain all the tabs created for recovery purposes
        self.base_tab = self.Tab(0, self.tab_frame, "Base Tab")  # Default Tab, might be removed in the future
        self.tab_list.append(self.base_tab)
        self.tab_amount = 1  # Potentially pointless, len(tab_list) is the same

    def new_tab(self):
        self.tab_list.append(self.Tab(self.tab_amount, self.tab_frame, f"Tab {self.tab_amount}"))
        self.tab_amount += 1


root = Tk()
my_gui = TTCc_GUI(root)
root.mainloop()