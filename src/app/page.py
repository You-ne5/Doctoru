from customtkinter import *
from assets.code.ui import Colors
from src.app import navbar, infobar

class Page(CTkFrame):
    def __init__(self, window: CTk):
        super().__init__(window, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = window

        self.infoBar = infobar.InfoBar(self)
        self.infoBar.place(x=0, y=0, height=30, relwidth=1)

        self.navBar = navbar.NavBar(self)
        self.navBar.place(x=0, y=30, height=120, relwidth=1)
        self.navBar.homeButton.invoke()

