from customtkinter import *
from assets.code.ui import Colors, clear
from src.auth import signin
from PIL import Image
import bcrypt
from src.app import home
import json
from assets.code.ui import font


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
            font=font(96),
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
            font=font(64),
            text_color=Colors.White,
        ).pack(pady=30)

        self.usernameEntry = CTkEntry(
            loginCard,
            placeholder_text="Nom d'utilisateur",
            fg_color=Colors.White,
            width=375,
            height=60,
            corner_radius=50,
            font=font(25),
            justify=CENTER,
            text_color=Colors.Cadet,
        )
        self.usernameEntry.place(x=88, y=147)

        self.passwordEntry = CTkEntry(
            loginCard,
            placeholder_text="Entrez le mot de passe",
            fg_color=Colors.White,
            width=375,
            height=60,
            corner_radius=50,
            font=font(25),
            justify=CENTER,
            text_color=Colors.Cadet,
            show="*",
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
            font=font(22),
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
            font=font(30),
            command=self.Login,
        ).place(x=125, y=426)

        CTkLabel(
            loginCard,
            width=214,
            height=19,
            text_color=Colors.White,
            font=font(16),
            text="Pas encore de compte?",
        ).place(x=126, y=491)

        CTkButton(
            loginCard,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            hover_color=Colors.Cadet,
            font=font(16),
            command=lambda: signin.SignInPage(self.window),
            text="S'inscrire",
            fg_color=Colors.Cadet,
        ).place(x=326, y=488)

        loginCard.bind("<Button-1>", lambda _: self.focus())
        self.bind("<Button-1>", lambda _: self.focus())

    def Login(self):

        entryUsername = self.usernameEntry.get()
        entryPassword = self.passwordEntry.get()

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if entryUsername:
            user = self.window.curr.execute(
                """SELECT id, password FROM "users" WHERE username=?""",
                (entryUsername,),
            ).fetchone()

            if user:
                userId, userPassword = user

                if bcrypt.checkpw(
                    bytes(entryPassword, "utf-8"), bytes(userPassword, "utf-8")):
                    self.window.userId = userId
                    if self.rememberMeCheck.get():
                        with open("config.json", "w") as f:
                            json.dump({"userId": userId}, f)

                    home.HomePage(self.window)
                    return

                else:
                    alert = "Mot de passe incorrect!"
            else:
                alert = "Nom d'utilisateur incorrect!"

            self.AlertLabel = CTkLabel(
                self,
                text=alert,
                fg_color=Colors.Danger,
                text_color=Colors.White,
                font=font(20),
                height=40,
            )

            self.AlertLabel.pack(side="bottom", fill="x")
