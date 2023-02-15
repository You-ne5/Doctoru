from customtkinter import *
from assets.code.ui import Colors, font
from datetime import datetime



class InfoBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master.window, corner_radius=0, fg_color=Colors.Liver)

        username = master.window.curr.execute("""SELECT username FROM users WHERE id = ?""", (master.window.userId,)).fetchone()

        monthsli=['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre']

        date = CTkLabel(self, text=f"{datetime.now().day} {monthsli[datetime.now().month-1]} {datetime.now().year}", font=font(20), text_color=Colors.White)
        date.pack(side=LEFT, padx=15)

        user = CTkLabel(self, text=f"Connecté en tant que: {username[0]}", font=font(20), text_color=Colors.White)
        user.pack(side=RIGHT, padx=15)