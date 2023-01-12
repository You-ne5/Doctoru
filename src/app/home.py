from customtkinter import *
from assets.code.ui import clear, Colors, font
from assets.code.logic import strToDatetime
from PIL import Image
from datetime import datetime
from src.app.visits import VisitsPage

class AddMeeting(CTkToplevel):
    def __init__(self, window):
        super().__init__(window, fg_color=Colors.Cadet)
        self.title("Ajouter un rendez-vous")
        self.geometry("500x500")

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
        self.master = master
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

        if not meetings:
            CTkLabel(self, text="Aucun rendez-vous", text_color=Colors.White, font=font(24)).place(relx=0.5, rely=0.5, anchor=CENTER)
            return

        pages = []

        for patientId, dt in meetings:
            if not pages or len(pages[-1]) == 4:
                pages.append([])

            dt = strToDatetime(dt)
            if datetime.now().date() == dt.date():

                firstname, lastname = self.window.curr.execute(""" SELECT firstName, lastName FROM patients WHERE id = ?""", (patientId,)).fetchone()

                pages[-1].append((" ".join([firstname.capitalize(), lastname.capitalize()]), dt))

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
        self.master = master
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
            command=lambda: self.master.master.navBar.patientsButton.invoke()
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
            command=lambda: VisitsPage(self.master.master).place(x=0, y=150, width=1280, height=682)
        )
        addVisitButton.place(x=546, y=10)
        CTkLabel(
            self, text="Ajouter Visite", font=font(16), text_color=Colors.White
        ).place(x=527, y=90)


class PatientsQueue(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)

        self.window = master.window

        self.master = master

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

        CTkFrame(self, height=5, fg_color=Colors.Cadet).place(x=0, y=35, relwidth=1)

        self.waitingPatientsFrame = CTkFrame(self, fg_color=Colors.Cadet)
        self.waitingPatientsFrame.place(x=0, y=35, relwidth=1, height=302)

        CTkButton(self, fg_color=Colors.Mandarin, hover_color=Colors.Sepia, text="Suivant", width=150, height=30, font=font(24), command=self.next).pack(side="bottom", pady=14)

        self.load()


    def load(self):
        clear(self.waitingPatientsFrame)
        patientsWaiting = self.window.curr.execute(""" SELECT patientFirstName, patientLastName, datetime FROM waiting WHERE seen = ?""", (0,)).fetchall()
        patientsWaiting = [patient for patient in patientsWaiting if patient[2].startswith(str(datetime.now().strftime("%d/%m/%Y")))]

        if patientsWaiting:
            CTkLabel(self.waitingPatientsFrame, text=" ".join(patientsWaiting[0][0:2]), width=250, height=35, fg_color=Colors.Coral, text_color=Colors.Mandarin, font=font(20), corner_radius=10).pack(pady=20)

            CTkFrame(self.waitingPatientsFrame, fg_color=Colors.Mandarin, height=2).pack(fill="x")

            waitingRoom = CTkFrame(self.waitingPatientsFrame, fg_color=Colors.Cadet)
            waitingRoom.pack(fill="x")

            for waitingPatient in patientsWaiting[1:6]:
                CTkLabel(waitingRoom, text=" ".join(waitingPatient[0:2]), width=215, height=35, fg_color=Colors.Coral, text_color=Colors.White, font=font(16), corner_radius=10).pack(pady=5)


        else:
            CTkLabel(self.waitingPatientsFrame, text="Aucun\npatient en attente", font=font(24), text_color=Colors.White).place(relx=0.5, rely=0.5, anchor=CENTER)

    def next(self):
        patientsWaiting = self.window.curr.execute(""" SELECT id, datetime FROM waiting WHERE seen = ?""", (0,)).fetchall()
        patientsWaiting = [patient for patient in patientsWaiting if patient[1].startswith(str(datetime.now().strftime("%d/%m/%Y")))]
        
        self.window.curr.execute("""UPDATE waiting SET seen = ? WHERE id = ?""", (1, patientsWaiting[0][0]))
        self.window.conn.commit()

        self.load()


class DailyVisits(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)

        self.window = master.window

        self.master = master

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

        visits = self.window.curr.execute("""SELECT datetime FROM visits""").fetchall()
        dailyVisits = [visit for visit in visits if visit[0].startswith(str(datetime.now().strftime("%d/%m/%Y")))]

        CTkLabel(
            self,
            text=f"{len(dailyVisits)} Patient{'s' if len(dailyVisits) > 1 else ''}",
            font=font(40),
            text_color=Colors.White,
            fg_color=Colors.Cadet,
        ).pack(pady=50)


class DailyCash(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=10, fg_color=Colors.Cadet)

        self.window = master.window

        self.master = master

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

        visits = self.window.curr.execute("""SELECT datetime, montant FROM visits""").fetchall()
        dailyVisits = [visit for visit in visits if visit[0].startswith(str(datetime.now().strftime("%d/%m/%Y")))]
        dailyCash = sum([montant for dt, montant in dailyVisits])

        CTkLabel(
            self,
            text=f"{int(dailyCash)} DA",
            font=font(40),
            text_color=Colors.White,
            fg_color=Colors.Cadet,
        ).pack(pady=50)


class Page(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)

        self.window = master.window

        self.master = master
        
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
        clear(master)
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
