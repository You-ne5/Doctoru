import sqlite3
from os import environ as env

from customtkinter import CTk

from assets.code.ui import Colors, center
from src.auth.login import LoginPage


class App(CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=Colors.Coral)

        self.title("Doctobot")
        self.iconbitmap("assets\imgs\Dbot logo.ico")

        center(1280, 832, self)
        self.resizable(False, False)
        env["DB"] = "main.db"

        self.conn = sqlite3.connect(env["DB"])
        self.curr = self.conn.cursor()

        LoginPage(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
