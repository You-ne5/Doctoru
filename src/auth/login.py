from customtkinter import *
from assets.code.ui import Colors, clear
from src.auth.signin import SignInPage

class LoginPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)
        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)