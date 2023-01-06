from customtkinter import *
from assets.code.ui import Colors, font

class InfoBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Liver)

        date = CTkLabel(self, text="Jeudi 5 janvier 2023", font=font(20), text_color=Colors.White)
        date.pack(side=LEFT, padx=15)

        user = CTkLabel(self, text="Connecté en tant que: Dr. Attab", font=font(20), text_color=Colors.White)
        user.pack(side=RIGHT, padx=15)