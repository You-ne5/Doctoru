from customtkinter import *
from assets.code.ui import Colors, clear
from PIL import Image


class SignInPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)
        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        bg_image = CTkImage(
            light_image=Image.open("assets/imgs/doctor image.png"),
            dark_image=Image.open("assets/imgs/doctor image.png"),
            size=(490, 832),
        )

        label1 = CTkLabel(self, image=bg_image, text="")
        label1.image = bg_image

        label1.place(x=0, y=0)

        label = CTkLabel(
            self,
            text="DoctoBot",
            font=CTkFont(family="Roboto", size=96, weight="bold"),
            text_color=Colors.Mandarin,
        )
        label.pack(pady=15)

        card = CTkFrame(
            self, corner_radius=50, fg_color=Colors.Cadet, width=550, height=550
        )
        card.place(relx=0.5, rely=0.5, anchor=CENTER, width=550, height=550)

        label = CTkLabel(
            card,
            text="Inscription",
            font=CTkFont(family="Roboto", size=64, weight="bold"),
            text_color=Colors.White,
        )
        label.pack(pady=30)

        CTkEntry(
            card,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Nom d'utilisateur",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
        ).place(x=87, y=147)

        CTkEntry(
            card,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Mot de passe",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
        ).place(x=87, y=232)

        CTkEntry(
            card,
            width=375,
            height=60,
            fg_color=Colors.White,
            placeholder_text="Repetez le mot de passe",
            placeholder_text_color=Colors.Silver,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER,
            corner_radius=50,
            text_color=Colors.Cadet,
        ).place(x=87, y=317)

        CTkButton(
            card,
            width=300,
            height=60,
            fg_color=Colors.Mandarin,
            text="S'inscrire",
            font=CTkFont(family="Roboto", size=32, weight="bold"),
            corner_radius=50,
            text_color=Colors.White,
        ).place(x=125, y=426)

        CTkLabel(
            card,
            width=214,
            height=19,
            text_color=Colors.White,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Vous avez deja un compte?",
        ).place(x=113, y=491)
        CTkButton(
            card,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Se connecter",
            fg_color=Colors.Cadet,
        ).place(x=332, y=488)
