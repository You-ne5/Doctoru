import bcrypt
from customtkinter import *
from assets.code.ui import Colors, clear, font
from src.auth import login
from src.app import page
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
            font=font(96),
            text_color=Colors.Mandarin,
        ).pack(pady=15)

        signinCard = CTkFrame(
            self, corner_radius=50, fg_color=Colors.Cadet, width=550, height=550
        )
        signinCard.place(relx=0.5, rely=0.52, anchor=CENTER, width=550, height=550)

        CTkLabel(
            signinCard,
            text="Inscription",
            font=font(64),
            text_color=Colors.White,
        ).pack(pady=30)

        self.usernameEntry = CTkEntry(
            signinCard,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Nom d'utilisateur",
            placeholder_text_color=Colors.Silver,
            font=font(25),
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
            font=font(25),
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
            font=font(25),
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
            font=font(32),
            corner_radius=50,
            hover_color=Colors.Sepia,
            command=self.signin,
            text_color=Colors.White,
        ).place(x=125, y=426)

        CTkLabel(
            signinCard,
            width=214,
            height=19,
            text_color=Colors.White,
            font=font(16),
            text="Vous avez deja un compte?",
        ).place(x=113, y=491)

        CTkButton(
            signinCard,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            font=font(16),
            text="Se connecter",
            command=lambda: login.LoginPage(self.window),
            fg_color=Colors.Cadet,
        ).place(x=332, y=488)

        signinCard.bind("<Button-1>", lambda _: self.focus())
        self.bind("<Button-1>", lambda _: self.focus())

    def signin(self):
        entryUsername = self.usernameEntry.get()
        entryPassword = self.passwordEntry.get()
        entryRepreatPassword = self.repeatPasswordEntry.get()

        user = self.window.curr.execute(
            "SELECT id FROM 'users' WHERE username=?", (entryUsername,)
        ).fetchone()

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if not user:
            errors = self.check_password(entryPassword)
            if not errors:
                if entryPassword == entryRepreatPassword:
                    entryPassword = bcrypt.hashpw(
                        bytes(entryPassword, "ascii"), bcrypt.gensalt(14)
                    ).decode("ascii")

                    self.window.curr.execute(
                        "INSERT INTO 'users' (username, password) VALUES (?, ?)",
                        (entryUsername, entryPassword),
                    )

                    self.window.conn.commit()

                    userId = self.window.curr.execute(
                        """SELECT id FROM "users" WHERE username=?""", (entryUsername,)
                    ).fetchone()[0]

                    self.window.userId = userId

                    page.Page(self.window)
                    return
                else:
                    alert = "Les mots de passe ne correspondent pas !"
            else:
                alert = errors[0]

        else:
            alert = "L'utilisateur existe déja !"

        self.AlertLabel = CTkLabel(
            self.window,
            text=alert,
            fg_color=Colors.Danger,
            text_color=Colors.White,
            font=font(20),
            height=40,
        )

        self.AlertLabel.pack(side="bottom", fill="x")

    def check_password(self, pwd) -> list[str]:
        conds = {
            "Le mot de passe est trop court !": lambda s: len(s) >= 5,
        }

        return [error for error, cond in conds.items() if not cond(pwd)]
