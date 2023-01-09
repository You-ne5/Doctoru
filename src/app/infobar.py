from customtkinter import *
from assets.code.ui import Colors, font

class InfoBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master.window, corner_radius=0, fg_color=Colors.Liver)

        username = master.window.curr.execute("""SELECT username FROM users WHERE id = ?""", (master.window.userId,)).fetchone()

        date = CTkLabel(self, text="Jeudi 5 janvier 2023", font=font(20), text_color=Colors.White)
        date.pack(side=LEFT, padx=15)

        user = CTkLabel(self, text=f"Connecté en tant que: {username[0]}", font=font(20), text_color=Colors.White)
        user.pack(side=RIGHT, padx=15)