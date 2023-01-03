import sqlite3
from os import environ as env

from customtkinter import CTk

from assets.code.ui import Colors
from src.auth.login import Login


class App(CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=Colors.White)

        self.title("Doctobot")

        env["DB"] = "main.db"

        self.conn = sqlite3.connect(env["DB"])
        self.curr = self.conn.cursor()

        Login(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
