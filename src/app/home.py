from customtkinter import *
from assets.code.ui import clear, Colors, font
from assets.code.logic import strToDatetime
from src.app import navbar, infobar
from PIL import Image
from datetime import datetime


class Meeting(CTkFrame):
    def __init__(self, master: CTkFrame, patientId: int, dt: datetime):
        super().__init__(
            master, width=350, height=100, corner_radius=20, fg_color=Colors.Coral
        )

        self.patientId = patientId
        self.dt = dt

        CTkLabel(
            self,
            text=dt.time().strftime("%H:%M"),
            font=font(32),
            text_color=Colors.Mandarin,
        ).place(x=20, y=15)

        CTkLabel(self, text=patientId, font=font(24), text_color=Colors.White).place(
            x=20, y=54
        )


class DailyMeetings(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.window = master.window
        self.page = 0

        self.view()

    def view(self):
        header = CTkFrame(self, fg_color=Colors.Mandarin, corner_radius=0, height=75)
        header.pack(fill="x")

        CTkLabel(
            header, text="Rendez-vous du jour", font=font(28), text_color=Colors.White
        ).place(x=25, y=20)

        CTkButton(
            header,
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            corner_radius=0,
            width=75,
            height=74,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/add rdv icon.png"), size=(50, 50)
            ),
        ).place(x=326)

        self.meetingsFrame = CTkFrame(self, fg_color=Colors.Cadet)
        self.meetingsFrame.place(x=0, y=75, width=400, height=607)

        self.load()

    def load(self):
        clear(self.meetingsFrame)
        meetings = self.window.curr.execute(
            """SELECT patientId, datetime FROM "meetings" """
        ).fetchall()
        pages = []

        if pages:
            for patientId, dt in meetings:
                if not pages or len(pages[-1]) == 4:
                    pages.append([])

                dt = strToDatetime(dt)
                if datetime.now().date() == dt.date():
                    pages[-1].append((patientId, dt))

            for patientId, dt in pages[self.page]:
                meetingCard = Meeting(self.meetingsFrame, patientId, dt)
                meetingCard.pack(pady=15)

        cursor = CTkFrame(
            self.meetingsFrame, width=195, height=40, fg_color=Colors.Cadet
        )
        cursor.place(x=104, y=547)

        CTkButton(
            cursor,
            text="<",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.page else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.page else Colors.Silver,
            command=lambda: self.update(-1 if self.page else 0),
        ).place(x=0, y=0)

        CTkLabel(
            cursor, text=self.page + 1, width=56, justify=CENTER, font=font(30)
        ).place(x=68, y=3)

        CTkButton(
            cursor,
            text=">",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.page < len(pages) - 1 else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.page < len(pages) - 1 else Colors.Silver,
            command=lambda: self.update(1 if self.page < len(pages) - 1 else 0),
        ).place(x=134, y=0)

    def update(self, num):
        self.page += num
        self.load()


class ActionBar(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)
        self.view()

    def view(self):
        addPatientButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/add patient icon.png"),
                size=(50, 50),
            ),
        )
        addPatientButton.place(x=270, y=10)
        CTkLabel(
            self, text="Ajouter Patient", font=font(16), text_color=Colors.White
        ).place(x=245, y=90)

        searchButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/search icon.png"), size=(50, 50)
            ),
        )
        searchButton.place(x=410, y=10)
        CTkLabel(self, text="Recherche", font=font(16), text_color=Colors.White).place(
            x=403, y=90
        )

        addVisitButton = CTkButton(
            self,
            fg_color=Colors.Cadet,
            hover_color=Colors.Sepia,
            corner_radius=10,
            width=70,
            height=70,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/add visit icon.png"), size=(50, 50)
            ),
        )
        addVisitButton.place(x=546, y=10)
        CTkLabel(
            self, text="Ajouter Visite", font=font(16), text_color=Colors.White
        ).place(x=527, y=90)


class PatientsQueue(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)
        self.view()

    def view(self):
        CTkLabel(
            self,
            text="Patients en attente",
            font=font(20),
            height=40,
            corner_radius=10,
            text_color=Colors.White,
            fg_color=Colors.Mandarin,
            bg_color=Colors.Coral,
        ).pack(fill="x")

        CTkFrame(self, height=10, fg_color=Colors.Cadet).place(x=0, y=35, relwidth=1)

        CTkLabel(
            self,
            text="Mr. Hamid",
            width=250,
            height=35,
            font=font(20),
            corner_radius=10,
            text_color=Colors.Mandarin,
            fg_color=Colors.Coral,
        ).pack(pady=20)

        CTkButton(
            self,
            text="Suivant",
            text_color=Colors.White,
            width=150,
            height=35,
            font=font(24),
            fg_color=Colors.Mandarin,
        ).pack(side="bottom", pady=15)

        CTkLabel(
            self,
            text="Mr. Hamid",
            width=250,
            height=35,
            font=font(20),
            corner_radius=10,
            text_color=Colors.Mandarin,
            fg_color=Colors.Coral,
        ).pack(pady=20)


class DailyVisits(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)
        self.view()

    def view(self):
        CTkLabel(
            self,
            text="Nombre de visites du jour",
            font=font(20),
            height=40,
            corner_radius=10,
            text_color=Colors.White,
            fg_color=Colors.Mandarin,
            bg_color=Colors.Coral,
        ).pack(fill="x")

        CTkFrame(self, height=10, fg_color=Colors.Cadet).place(x=0, y=35, relwidth=1)

        CTkLabel(
            self,
            text="2 Patients",
            font=font(40),
            text_color=Colors.White,
            fg_color=Colors.Cadet,
        ).pack(pady=50)


class DailyCash(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)
        self.view()

    def view(self):
        CTkLabel(
            self,
            text="Recette du jour",
            font=font(20),
            height=40,
            corner_radius=10,
            text_color=Colors.White,
            fg_color=Colors.Mandarin,
            bg_color=Colors.Coral,
        ).pack(fill="x")

        CTkFrame(self, height=10, fg_color=Colors.Cadet).place(x=0, y=35, relwidth=1)

        CTkLabel(
            self,
            text="1000$",
            font=font(40),
            text_color=Colors.White,
            fg_color=Colors.Cadet,
        ).pack(pady=50)


class Page(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.view()

    def view(self):
        CTkLabel(
            self,
            text="Accueil",
            font=font(45),
            width=400,
            height=75,
            text_color=Colors.White,
            fg_color=Colors.Liver,
            corner_radius=20,
        ).pack(pady=10)

        patientsQueue = PatientsQueue(self)
        patientsQueue.place(x=90, y=115, width=300, height=400)

        dailyVisits = DailyVisits(self)
        dailyVisits.place(x=485, y=115, width=300, height=175)

        dailyCash = DailyCash(self)
        dailyCash.place(x=485, y=340, width=300, height=175)


class HomePage(CTkFrame):
    def __init__(self, master: CTkFrame) -> None:
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        
        self.window = master.window

        self.master = master

        self.view()

    def view(self):
        dailyMeetings = DailyMeetings(self)
        dailyMeetings.place(x=0, y=0, width=400, height=682)

        actionBar = ActionBar(self)
        actionBar.place(x=400, y=562, width=880, height=120)

        page = Page(self)
        page.place(x=400, y=0, width=880, height=562)
