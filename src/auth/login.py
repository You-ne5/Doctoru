from customtkinter import *
from PIL import Image
import json
import bcrypt

from assets.code.ui import Colors, clear
from src.auth import signin
from src.app import page
from assets.code.ui import font


class LoginPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)

        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = window

        self.view()

    def view(self):

        doctor_image = CTkImage(
            light_image = Image.open("assets/imgs/doctor image.png"),
            dark_image = Image.open("assets/imgs/doctor image.png"),
            size=(490, 832),
        )

        background_image = CTkLabel(self, image = doctor_image, text = "")
        background_image.image = doctor_image
        background_image.place(x= 0, y= 0)

        #title
        CTkLabel(
            self,
            text = "DoctoBot",
            text_color = Colors.Mandarin,
            font = font(96),
        ).pack(pady= 15)

        login_card = CTkFrame(self, fg_color = Colors.Cadet, corner_radius = 50, width = 550, height = 550)
        login_card.place(
            relx = 0.5,
            rely = 0.52,
            anchor = CENTER,
            width = 550,
            height = 550,
        )

        CTkLabel(
            login_card,
            text = "Connexion",
            text_color = Colors.White,
            font = font(64),
        ).pack(pady= 30)

        self.username_entry = CTkEntry(
            login_card,
            placeholder_text = "Nom d'utilisateur",
            font = font(25),
            fg_color = Colors.White,
            text_color = Colors.Cadet,
            width = 375,
            height = 60,
            corner_radius = 50,
            justify = CENTER,
        )
        self.username_entry.place(x= 88, y= 147)

        self.password_entry = CTkEntry(
            login_card,
            placeholder_text = "Entrez le mot de passe",
            text_color = Colors.Cadet,
            font = font(25),
            width = 375,
            height = 60,
            corner_radius = 50,
            fg_color = Colors.White,
            justify = CENTER,
            show = "*",
        )
        self.password_entry.place(x= 88, y= 252)

        self.remember_me_check = CTkCheckBox(
            login_card,
            text = "Se souvenir de moi",
            text_color = Colors.White,
            font = font(22),
            width = 25,
            height = 25,
            fg_color = Colors.Mandarin,
            hover_color = Colors.Sepia,
            border_color = Colors.White,
        )
        self.remember_me_check.place(x= 105, y= 350)

        #connection button
        CTkButton(
            login_card,
            text = "Se connecter",
            text_color = Colors.White,
            font = font(30),
            width = 300,
            height = 60,
            fg_color = Colors.Mandarin,
            hover_color = Colors.Sepia,
            corner_radius = 50,
            command = self.login,
        ).place(x= 125, y= 426)


        CTkLabel(
            login_card,
            text = "Pas encore de compte?",
            text_color = Colors.White,
            font = font(16),
            width = 214,
            height = 19,
        ).place(x= 126, y= 491)

        #signin redirect button
        CTkButton(
            login_card,
            text = "S'inscrire",
            text_color = Colors.Mandarin,
            font = font(16),
            width = 105,
            height = 19,
            fg_color = Colors.Cadet,
            hover_color = Colors.Cadet,
            command = lambda : signin.SignInPage(self.window),
        ).place(x= 326, y= 488)

        login_card.bind("<Button-1>", lambda _: self.focus())
        self.bind("<Button-1>", lambda _: self.focus())

    def login(self):

        username_entered = self.username_entry.get()
        password_entered = self.password_entry.get()

        try:
            self.alert_label.destroy()
        except:
            pass

        if username_entered:
            user_id, user_password = self.window.curr.execute(
                """SELECT id, password FROM "users" WHERE username=?""",
                (username_entered,),
            ).fetchone()

            if user_id:

                if bcrypt.checkpw(bytes(password_entered, "utf-8"), bytes(user_password, "utf-8")):
                    self.window.userId = user_id

                    if self.remember_me_check.get():
                        with open("config.json", "w") as f:
                            json.dump({"userId": user_id}, f)

                    page.Page(self.window)
                    return

                else:
                    alert_massage = "Mot de passe incorrect!"
            else:
                alert_massage = "Nom d'utilisateur incorrect!"

            self.alert_label = CTkLabel(
                self,
                text = alert_massage,
                text_color = Colors.White,
                font = font(20),
                height = 40,
                fg_color = Colors.Danger,
            )
            self.alert_label.pack(side= "bottom", fill= "x")
