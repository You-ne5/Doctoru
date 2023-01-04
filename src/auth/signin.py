import bcrypt
from customtkinter import *
from assets.code.ui import Colors, clear
from src.auth import login
from PIL import Image
import bcrypt

class SignInPage(CTkFrame):
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
            font=CTkFont(family="Roboto", size=96, weight="bold"),
            text_color=Colors.Mandarin,
        ).pack(pady=15)

        signinCard = CTkFrame(
            self, corner_radius=50, fg_color=Colors.Cadet, width=550, height=550
        )
        signinCard.place(relx=0.5, rely=0.52, anchor=CENTER, width=550, height=550)

        CTkLabel(
            signinCard,
            text="Inscription",
            font=CTkFont(family="Roboto", size=64, weight="bold"),
            text_color=Colors.White,
        ).pack(pady=30)

        self.usernameEntry = CTkEntry(
            signinCard,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Nom d'utilisateur",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
        )
        self.usernameEntry.place(x=87, y=147)

        self.passwordEntry = CTkEntry(
            signinCard,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Mot de passe",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
            show="*",
        )
        self.passwordEntry.place(x=87, y=232)

        self.repeatPasswordEntry = CTkEntry(
            signinCard,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Repetez le mot de passe",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
            show="*",
        )
        self.repeatPasswordEntry.place(x=87, y=317)

        CTkButton(
            signinCard,
            width=300,
            height=60,
            fg_color=Colors.Mandarin,
            text="S'inscrire",
            font=CTkFont(family="Roboto", size=32, weight="bold"),
            corner_radius=50,
            text_color=Colors.White,
        ).place(x=125, y=426)

        CTkLabel(
            signinCard,
            width=214,
            height=19,
            text_color=Colors.White,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Vous avez deja un compte?",
        ).place(x=113, y=491)

        CTkButton(
            signinCard,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Se connecter",
            command=lambda: login.LoginPage(self.window),
            fg_color=Colors.Cadet,
        ).place(x=332, y=488)

        signinCard.bind("<Button-1>", lambda _: self.focus())
        self.bind("<Button-1>", lambda _: self.focus())

    def signin(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        repreatPassword = self.repeatPasswordEntry.get()

        user = self.window.curr.execute(
            "SELECT id FROM 'users' WHERE username=?", (username,)
        ).fetchone()

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if not user:
            errors = self.check_password(password)
            if not errors:
                if password == repreatPassword:
                    password = bcrypt.hashpw(
                        bytes(password, "ascii"), bcrypt.gensalt(14)
                    ).decode("ascii")

                    self.window.curr.execute(
                        "INSERT INTO 'users' (username, password) VALUES (?, ?)",
                        (username, password),
                    )

                    self.window.conn.commit()

                    login.LoginPage(self.window)
                    return
                else:
                    self.AlertLabel = CTkLabel(
                        self.window,
                        text="Les mots de passe ne correspondent pas !",
                        fg_color=Colors.Danger,
                        font=CTkFont(family="Roboto", size=25, weight="bold"),
                        height=40,
                    )
            else:
                self.AlertLabel = CTkLabel(
                    self.window,
                    text=errors[0],
                    fg_color=Colors.Danger,
                    font=CTkFont(family="Roboto", size=25, weight="bold"),
                    height=40,
                )
        else:
            self.AlertLabel = CTkLabel(
                self.window,
                text="L'utilisateur existe déja !",
                fg_color=Colors.Danger,
                font=CTkFont(family="Roboto", size=25, weight="bold"),
                height=40,
            )

        self.AlertLabel.pack(side="bottom", fill="x")

    def check_password(self, pwd) -> list[str]:
        conds = {
            "Le mot de passe est trop court !": lambda s: len(s) >= 5,
        }

        return [error for error, cond in conds.items() if not cond(pwd)]