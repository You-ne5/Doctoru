from customtkinter import *
from assets.code.ui import Colors, font, clear, center
from PIL import Image
from src.app import home, patients
from src.auth import login
import json

def select(master, button: CTkButton):
    for widget in master.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(fg_color=Colors.Cadet)
    button.configure(fg_color=Colors.Mandarin)


class LogoutConfirm(CTkToplevel):
    def __init__(self, window):
        super().__init__(fg_color=Colors.Cadet)

        self.title("Deconnexion") 
        self.resizable(False, False)

        self.window = window

        center(574, 245, self)

        self.view()

    def view(self):
        CTkLabel(self, text="Deconnexion", fg_color=Colors.Liver, font=font(25), text_color=Colors.White, corner_radius=15).place(x=124, y=34, width=320, height=70)

        CTkLabel(self, text=f"Étes vous sure de vouloir vous deconnecter", font=font(16), text_color=Colors.White).place(relx=0.5, rely=0.51, anchor=CENTER)

        CTkButton(self, text="Se deconnecter", fg_color=Colors.Danger, text_color=Colors.White, hover_color=Colors.Danger_hover, command=self.logout, font=font(15)).place(x=308, y=178, width=130, height=50)
        CTkButton(self, text="Annuler", fg_color=Colors.Silver, text_color=Colors.White, hover_color=Colors.Mandarin, command=self.close, font=font(15)).place(x=140, y=178, width=130, height=50)
    
    def close(self):
        self.destroy()

    def logout(self):
        self.window.userId = None
        with open("config.json", "w") as f:
            json.dump({"userId": None}, f)
        login.LoginPage(self.window)


class NavBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master.window, height=120, corner_radius=0, fg_color=Colors.Cadet)

        self.window = master.window
        self.toplevel = None

        self.homeButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: [select(self, self.homeButton), home.HomePage(master).place(x=0, y=150, width=1280, height=682)],
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/home icon.png"), size=(50, 50)
            ),
        )
        self.homeButton.place(x=40, y=10)

        CTkLabel(self, text="Accueil", font=font(16), text_color=Colors.White).place(
            x=45.5, y=90
        )

        self.patientsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: [select(self, self.patientsButton), patients.PatientsPage(master).place(x=0, y=150, width=1280, height=682)],
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/patients icon.png"), size=(50, 50)
            ),
        )
        self.patientsButton.place(x=150, y=10)

        CTkLabel(self, text="Patients", font=font(16), text_color=Colors.White).place(
            x=152.5, y=90
        )

        self.agendaButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: select(self,self.agendaButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/agenda icon.png"), size=(50, 50)
            ),
        )
        self.agendaButton.place(x=260, y=10)

        CTkLabel(self, text="Agenda", font=font(16), text_color=Colors.White).place(
            x=264.5, y=90
        )

        self.statsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: select(self,self.statsButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/stats icon.png"), size=(50, 50)
            ),
        )
        self.statsButton.place(x=382.5, y=10)

        CTkLabel(
            self, text="Statistiques", font=font(16), text_color=Colors.White
        ).place(x=370, y=90)

        self.cashRegisterButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: select(self,self.cashRegisterButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/cash register icon.png"),
                size=(50, 50),
            ),
        )
        self.cashRegisterButton.place(x=500, y=10)

        CTkLabel(self, text="Caisse", font=font(16), text_color=Colors.White).place(
            x=508, y=90
        )

        self.settingsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: select(self,self.settingsButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/settings icon.png"), size=(50, 50)
            ),
        )
        self.settingsButton.place(x=1034.5, y=10)

        CTkLabel(self, text="Parametres", font=font(16), text_color=Colors.White).place(
            x=1024, y=90
        )

        self.logoutButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.logout(),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/logout icon.png"), size=(50, 50)
            ),
        )
        self.logoutButton.place(x=1168, y=10)

        CTkLabel(
            self, text="Deconnexion", font=font(16), text_color=Colors.White
        ).place(x=1151, y=90)

    def logout(self):
        if not self.toplevel:
            self.toplevel = LogoutConfirm(self.window)
            self.toplevel.protocol("WM_DELETE_WINDOW", self.toplevel.close)
        else:
            self.toplevel = None