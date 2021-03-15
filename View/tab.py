from tkinter import *


class Tab:
    def __init__(self, tab_frame, title="New Tab"):
        self.tab_frame = tab_frame
        tab = Frame(self.tab_frame)
        tab.pack(expand=True, fill=BOTH)
        self.tab_frame.add(tab, text=title)

        # Frames
        top_Frame = Frame(tab)
        top_Frame.pack(side=TOP, padx=10, pady=5)
        bottom_Frame = Frame(tab)
        bottom_Frame.pack(side=BOTTOM, expand=True, fill=BOTH, padx=10, pady=5)

        # Url field and "terminal view" text field
        self.url_field = Entry(top_Frame, widt=150)
        self.url_field.pack(side=LEFT, fill='x', padx=10)
        self.text_field = Text(bottom_Frame)
        self.text_field.pack(side=BOTTOM, expand=True, fill=BOTH)

        # Delete button, might be disabled if there's only 1 tab
        delete_tab_button = Button(top_Frame, text="Delete Tab", command=self.deleteTab)
        self.tab_frame.select(self.tab_frame.tabs()[-1])  # Jumps to the latest change
        if self.tab_frame.index(self.tab_frame.select()) == 0:  # Might change to 1 tab check
            delete_tab_button["state"] = "disable"
            delete_tab_button['text'] = "Disabled"
        delete_tab_button.pack(side=RIGHT)

    def deleteTab(self):
        self.tab_frame.forget(self.tab_frame.select())

    def write_txt_field(self, content):
        self.text_field.insert(END, content)