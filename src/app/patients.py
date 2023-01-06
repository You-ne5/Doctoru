from customtkinter import *
from assets.code.ui import clear, Colors, font
from src.app import navbar, infobar
from PIL import Image


class PageFrame(CTkFrame):
    def __init__(self, master: CTkFrame, patientid=None):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)

        self.master = master

        self.view()

    def view(self):
        CTkLabel(
            self,
            text="Section patients",
            font=font(45),
            fg_color=Colors.Liver,
            corner_radius=20,
            width=430,
            height=75,
            text_color=Colors.White,
        ).pack(pady=15)

        patientInfo = CTkFrame(
            self, width=360, height=560, fg_color=Colors.Cadet, corner_radius=20
        )
        patientInfo.place(x=23, y=106)

        info = lambda text, y: CTkLabel(patientInfo, font=font(20), text=text, text_color=Colors.White).place(x=20, y=y)

        info(f"Nom: Mr. ", 30)
        info(f"Prénom: Hamid ", 74)
        info(f"Date de naissance: 9/11/2001", 118)
        info(f"Genre: Garcon ", 162)
        info(f"Age: 45 ", 206)
        info(f"Poids recent: 80  ", 250)
        info(f"Taille recente: 1m80", 294)
        info(f"IMC recent: 24.9 ", 338)
        info(f"Numero de téléphone: 05123456 ", 382)
        info(f"Derniere visite: 20/7/2021 ", 426)
        info(f"Mots clés: Angine, Fievre ", 470)

        CTkButton(
            patientInfo,
            text="Modifier",
            width=240,
            height=42,
            fg_color=Colors.Mandarin,
            corner_radius=16,
            hover_color=Colors.Sepia,
            font=font(20),
            text_color=Colors.White,
        ).place(x=60, y=506)

        CTkButton(
            self,
            text="Historique des visites",
            font=font(26),
            fg_color=Colors.Cadet,
            width=380,
            height=72,
            corner_radius=20,
            hover_color="#10162b",
            text_color=Colors.Mandarin,
        ).place(x=433, y=494)

        CTkButton(
            self,
            text="Ajouter une visite",
            font=font(26),
            fg_color=Colors.Mandarin,
            width=380,
            height=72,
            corner_radius=20,
            hover_color=Colors.Sepia,
            text_color=Colors.White,
        ).place(x=433, y=585)

        courbeDeCroissance = CTkFrame(self, width=375, height=370, corner_radius=20, fg_color=Colors.Cadet)
        courbeDeCroissance.place(x=433, y=109, width=375, height=370)

        CTkButton(
            courbeDeCroissance,
            text="Courbes de croissance",
            fg_color=Colors.Cadet,
            text_color=Colors.White,
            height=55,
            width=375,
            corner_radius=10,
            font=font(28),
            hover_color=Colors.Mandarin,
            bg_color=Colors.Coral,
        ).place(x=0, y=0)

        CTkFrame(courbeDeCroissance, height=10, fg_color=Colors.Cadet, corner_radius=0).place(x=0, y=45, relwidth=1)

        img = CTkImage(
            light_image=Image.open("assets/imgs/courbe de croissance.png"),
            size=(380, 305),
        )

        CTkLabel(courbeDeCroissance, image=img).place(x=0, y=43)


class PatientsList(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.master = master
        self.page = 0

        self.view()

    def view(self):
        header = CTkFrame(self, fg_color=Colors.Mandarin, corner_radius=0, height=75)
        header.pack(fill="x")

        CTkLabel(header, text="Liste des patients", font=font(28), text_color=Colors.White).place(x=25, y=20)

        CTkButton(
            header,
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            corner_radius=0,
            width=75,
            height=74,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/add patient icon.png"),
                size=(50, 50),
            ),
        ).place(x=326)

        searchPatient = CTkEntry(
            self,
            placeholder_text="Rechercher un patient...",
            height=25,
            width=400,
            font=font(15),
            text_color=Colors.Cadet,
            fg_color=Colors.White,
            bg_color=Colors.Coral,
            border_width=0,
            corner_radius=0,
        )
        searchPatient.pack()

        self.patientsframe = CTkFrame(self, fg_color=Colors.Cadet)
        self.patientsframe.place(x=0, y=100, width=400, height=582)

        self.load()

        for widget in self.master.winfo_children():
            widget.bind("<Button-1>", lambda _: self.focus())

    def load(self):
        clear(self.patientsframe)

        pages = []
        patients = [
            "Hamid",
            "Cristiano Ronaldo",
            "zaim",
            "zaim",
            "zaim",
            "zaim",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
            "hamid",
        ]

        for patient in patients:
            if not pages or len(pages[-1]) == 4:
                pages.append([])
            pages[-1].append(patient)

        for patient in pages[self.page]:
            patientcard = CTkFrame(
                self.patientsframe,
                width=350,
                height=100,
                corner_radius=20,
                fg_color=Colors.Coral,
            )
            patientcard.pack(pady=15)

            CTkLabel(
                patientcard, text=patient, font=font(32), text_color=Colors.Mandarin
            ).place(x=21, y=11)
            CTkLabel(
                patientcard,
                text="Derniere visite: 9/11/2021",
                font=font(24),
                text_color=Colors.White,
            ).place(x=21, y=59)
        
        CTkButton(
            self.patientsframe,
            text="<",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.page else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.page else Colors.Silver,
            command=lambda: self.update(-1 if self.page else 0),
        ).place(x=104, y=522)

        CTkLabel(
            self.patientsframe,
            text=self.page + 1,
            font=font(30),
            text_color=Colors.White,
        ).place(x=190, y=523)

        CTkButton(
            self.patientsframe,
            text=">",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.page < len(pages) - 1 else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.page < len(pages) - 1 else Colors.Silver,
            command=lambda: self.update(+1 if self.page < len(pages) - 1 else 0),
        ).place(x=238, y=522)

    def update(self, num):
        if num:
            self.page += num
            self.load()


class PatientPage(CTkFrame):
    def __init__(self, window: CTk) -> None:
        clear(window)

        super().__init__(window, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = window
        
        self.view()

    def view(self):
        infoBar = infobar.InfoBar(self)
        infoBar.place(x=0, y=0, relwidth=1, height=30)

        navBar = navbar.NavBar(self)
        navBar.place(x=0, y=30, relwidth=1, height=120)
        navBar.select(navBar.patientsButton)

        pageframe = PageFrame(self)
        pageframe.place(x=399, y=150, width=879, height=681)

        patientlist = PatientsList(self)
        patientlist.place(x=0, y=150, width=400, height=682)
