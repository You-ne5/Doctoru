from customtkinter import CTkFrame, CTk

from assets.code.ui import Colors
from src.app import navbar, infobar
from assets.code.ui import clear

class Page(CTkFrame):
    def __init__(self, window: CTk):
        clear(window)
        super().__init__(window, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = window

        self.info_bar = infobar.InfoBar(self)
        self.info_bar.place(x=0, y=0, height=30, relwidth=1)

        self.nav_bar = navbar.NavBar(self)
        self.nav_bar.place(x=0, y=30, height=120, relwidth=1)
        self.nav_bar.homeButton.invoke()

