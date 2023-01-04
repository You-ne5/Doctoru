from customtkinter import *
from assets.code.ui import Colors, clear
from src.auth.signin import SignInPage


class LoginPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)
        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)
        self.window = window
        window.geometry("1280x832")
        
        bg_image = CTkImage(
            light_image=Image.open("assets/imgs/doctor image.png"),
            dark_image=Image.open("assets/imgs/doctor image.png"),
            size=(490, 832),
        )

        label1 = CTkLabel(self, image=bg_image, text="")
        label1.image = bg_image
        label1.place(x=0, y=0)


        CTkLabel(
            self,
            text="DoctoBot",
            text_color=Colors.Mandarin,
            font=CTkFont(family="Roboto", size=96, weight="bold"),
        ).pack(pady=15)

        connexion_box = CTkFrame(self, fg_color=Colors.Cadet, corner_radius=50, width=550, height=550)

        connexion_box.place(
            relx=0.5,
            rely=0.52,
            anchor=CENTER,
            width=550,
            height=550,
        )

        con_label= CTkLabel(
            connexion_box,
            text="Connexion",
            font=CTkFont(family="Roboto", size=64, weight="bold"),
            text_color=Colors.White,
        )
        con_label.place(x=120, y=30)


        User_selection = CTkComboBox(
            connexion_box,
            width=375,
            height=60,
            corner_radius=50,
            fg_color=Colors.Mandarin,
            values=["Dr.Attab", "Assistante"],
            font=CTkFont(family="Roboto", size=30, weight="bold"),
            dropdown_font=CTkFont(family="Roboto", size=20, weight="bold"),
            dropdown_fg_color=Colors.Liver,
            justify=CENTER
        )
        User_selection.place(x=88, y=147)


        pw_entry = CTkEntry(
            connexion_box,
            placeholder_text="Entrez le mot de passe",
            fg_color=Colors.White,
            width=375,
            height=60,
            corner_radius=50,
            font=CTkFont(family="Roboto", size=25, weight="bold"),
            justify=CENTER
        )
        pw_entry.place(x=88, y=252)
        connexion_box.bind("<Button-1>", lambda event: self.focus())
        self.bind("<Button-1>", lambda event: self.focus())

        confirm_btn= CTkButton(connexion_box, text="Se connecter", fg_color=Colors.Mandarin, width=300, height=60, corner_radius=50, font=CTkFont(family="Roboto", size=30, weight="bold"))
        confirm_btn.place(x=125, y=426)

        no_account_label = CTkLabel(
            connexion_box,
            width=214,
            height=19,
            text_color=Colors.White,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="Pas encore de compte?",
        )
        no_account_label.place(x=126, y=491)


        signup_button =CTkButton(
            connexion_box,
            width=105,
            height=19,
            text_color=Colors.Mandarin,
            font=CTkFont(family="Roboto", size=16, weight="bold"),
            text="S'inscrire",
            fg_color=Colors.Cadet,
        )
        signup_button.place(x=326, y=488)

        remember_me = CTkCheckBox(connexion_box,text="Se souvenir de moi", width=25, height=25, font=CTkFont(family="Roboto", size=22, weight="bold"), )
        remember_me.place(x=105, y=350)


        



