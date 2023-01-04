import sqlite3
from customtkinter import CTk
from assets.code.ui import Colors, center
from src.auth import login
from src.app import home
import json


class App(CTk):
    def __init__(self) -> None:
        super().__init__(fg_color=Colors.Coral)

        self.title("Doctobot")
        self.iconbitmap("assets/imgs/Dbot Logo.ico")

        center(1280, 832, self)
        self.resizable(False, False)

        self.conn = sqlite3.connect("main.db")
        self.curr = self.conn.cursor()

        self.init_db()

        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                if config and config["userId"]:
                    self.userId = config["userId"]
                    home.HomePage(self)
                else:
                    raise
        except:
            self.userId = None
            login.LoginPage(self)

    def init_db(self):
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS "users" (
				"id" INTEGER NOT NULL UNIQUE, 
				"username" string NOT NULL, 
				"password" string NOT NULL, 
				PRIMARY KEY ("id" AUTOINCREMENT)
				)"""
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
