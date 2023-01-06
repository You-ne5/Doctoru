from customtkinter import *
from assets.code.ui import Colors, font
from PIL import Image


class NavBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, height=120, corner_radius=0, fg_color=Colors.Cadet)

        homeButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(homeButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/home icon.png"), size=(50, 50)
            ),
        )
        homeButton.place(x=40, y=10)
        CTkLabel(self, text="Accueil", font=font(16), text_color=Colors.White).place(
            x=45.5, y=90
        )

        patientsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(patientsButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/patients icon.png"), size=(50, 50)
            ),
        )
        patientsButton.place(x=150, y=10)
        CTkLabel(self, text="Patients", font=font(16), text_color=Colors.White).place(
            x=152.5, y=90
        )

        agendaButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(agendaButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/agenda icon.png"), size=(50, 50)
            ),
        )
        agendaButton.place(x=260, y=10)
        CTkLabel(self, text="Agenda", font=font(16), text_color=Colors.White).place(
            x=264.5, y=90
        )

        statsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(statsButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/stats icon.png"), size=(50, 50)
            ),
        )
        statsButton.place(x=382.5, y=10)
        CTkLabel(
            self, text="Statistiques", font=font(16), text_color=Colors.White
        ).place(x=370, y=90)

        cashRegisterButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(cashRegisterButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/cash register icon.png"),
                size=(50, 50),
            ),
        )
        cashRegisterButton.place(x=500, y=10)
        CTkLabel(self, text="Caisse", font=font(16), text_color=Colors.White).place(
            x=508, y=90
        )
        settingsButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(settingsButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/settings icon.png"), size=(50, 50)
            ),
        )
        settingsButton.place(x=1034.5, y=10)
        CTkLabel(self, text="Parametres", font=font(16), text_color=Colors.White).place(
            x=1024, y=90
        )

        logoutButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            command=lambda: self.select(logoutButton),
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/logout icon.png"), size=(50, 50)
            ),
        )
        logoutButton.place(x=1168, y=10)
        CTkLabel(
            self, text="Deconnexion", font=font(16), text_color=Colors.White
        ).place(x=1151, y=90)

    def select(self, button: CTkButton):
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(fg_color=Colors.Cadet)
        button.configure(fg_color=Colors.Mandarin)