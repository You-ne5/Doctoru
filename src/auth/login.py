from customtkinter import *
from assets.code.ui import Colors, clear
from src.auth import signin
from PIL import Image
import bcrypt
from os import environ as env
from src.app import home
import json

class LoginPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)

        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = window
        
        self.view()

    def view(self):

        image = CTkImage(
            light_image=Image.open("assets/imgs/doctor image.png"),
            dark_image=Image.open("assets/imgs/doctor image.png"),
            size=(490, 832),
        )

        backgroundImage = CTkLabel(self, image=image, text="")
        backgroundImage.image = image
        backgroundImage.place(x=0, y=0)

        CTkLabel(
            self,
            text="DoctoBot",
            text_color=Colors.Mandarin,
            font=CTkFont(family="Roboto", size=96, weight="bold"),
        ).pack(pady=15)

        loginCard = CTkFrame(
            self, fg_color=Colors.Cadet, corner_radius=50, width=550, height=550
        )

        loginCard.place(
            relx=0.5,
            rely=0.52,
            anchor=CENTER,
            width=550,
            height=550,
        )

        CTkLabel(
            loginCard,
            text="Connexion",
            font=CTkFont(family="Roboto", size=64, weight="bold"),
            text_color=Colors.White,
        ).pack(pady=30)

        self.usernameEntry = CTkEntry(
            loginCard,
            placeholder_text="Nom d'utilisateur",
            fg_color=Colors.White,
            width=375,
            height=60,
            corner_radius=50,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            text_color=Colors.Cadet
        )
        self.usernameEntry.place(x=88, y=147)

        self.passwordEntry = CTkEntry(
            loginCard,
            placeholder_text="Entrez le mot de passe",
            fg_color=Colors.White,
            width=375,
            height=60,
            corner_radius=50,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            text_color=Colors.Cadet,
            show="*"
        )
        self.passwordEntry.place(x=88, y=252)

        self.rememberMeCheck = CTkCheckBox(
            loginCard,
            text="Se souvenir de moi",
            width=25,
            height=25,
            fg_color=Colors.Mandarin,
            text_color=Colors.White,
            hover_color=Colors.Sepia,
            border_color=Colors.White,
            font=CTkFont(family="Roboto", size=22, weight="bold"),
        )
        self.rememberMeCheck.place(x=105, y=350)

        CTkButton(
            loginCard,
            text="Se connecter",
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            text_color=Colors.White,
            width=300,
            height=60,
            corner_radius=50,
            font=CTkFont(family="Roboto", size=30, weight="bold"),
            command=self.Login
        ).place(x=125, y=426)

        CTkLabel(
            loginCard,
            width=214,
            height=19,
            text_color=Colors.White,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Pas encore de compte?",
        ).place(x=126, y=491)

        CTkButton(
            loginCard,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            hover_color=Colors.Cadet,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            command=lambda: signin.SignInPage(self.window),
            text="S'inscrire",
            fg_color=Colors.Cadet,
        ).place(x=326, y=488)

        loginCard.bind("<Button-1>", lambda _: self.focus())
        self.bind("<Button-1>", lambda _: self.focus())


    def Login(self):

        entryUsername = self.usernameEntry.get()
        entryPassword = self.passwordEntry.get()

        curr = self.window.curr

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if entryUsername:
            user = curr.execute(
                """SELECT id, password FROM "users" WHERE username=?""", (entryUsername,)
            ).fetchone()

            if user:
                userId, userPassword = user
                if bcrypt.checkpw(bytes(entryPassword, "utf-8"), bytes(userPassword, "utf-8")):
                    self.window.userId = userId
                    if self.rememberMeCheck.get():
                        with open("config.json", "w") as f:
                            json.dump({"userId": userId}, f)

                    home.HomePage(self.window)
                    return

                else:
                    self.AlertLabel = CTkLabel(
                        self,
                        text="Mot de passe incorrect!",
                        fg_color=Colors.Danger,
                        font=CTkFont(family='Roboto', size=15, weight="bold"),
                        height=40,
                    )
            else:
                self.AlertLabel = CTkLabel(
                    self,
                    text="Nom d'utilisateur incorrect!",
                    fg_color=Colors.Danger,
                    font=CTkFont(family='Roboto', size=15, weight="bold"),
                    height=40,
                )
                

            self.AlertLabel.pack(side="bottom", fill="x")



        
                
            
