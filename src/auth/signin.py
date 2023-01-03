from customtkinter import CTkFrame, CTk
from assets.code.ui import Colors

class SignInPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)