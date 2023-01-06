from customtkinter import *
from assets.code.ui import Colors, font
from PIL import Image
from src.app import home, patients


class NavBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, height=120, corner_radius=0, fg_color=Colors.Cadet)

        self.homeButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: [self.select(self.homeButton), home.HomePage(master).place(x=0, y=150, width=1280, height=682)],
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
            command=lambda: [self.select(self.patientsButton), patients.PatientsPage(master).place(x=0, y=150, width=1280, height=682)],
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
            command=lambda: self.select(self.agendaButton),
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
            command=lambda: self.select(self.statsButton),
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
            command=lambda: self.select(self.cashRegisterButton),
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
            command=lambda: self.select(self.settingsButton),
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
            command=lambda: self.select(self.logoutButton),
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

    def select(self, button: CTkButton):
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(fg_color=Colors.Cadet)
        button.configure(fg_color=Colors.Mandarin)