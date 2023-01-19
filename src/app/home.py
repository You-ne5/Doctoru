from customtkinter import *
from assets.code.ui import clear, Colors, font, center
from assets.code.logic import strToDatetime
from PIL import Image
from datetime import datetime
from src.app.visits import VisitsPage
import sqlite3


class AddMeeting(CTkToplevel):
    def __init__(self, master):
        super().__init__(fg_color=Colors.Cadet)

        self.title("Ajouter un rendez-vous") 
        self.resizable(False, False)
        center(400, 420, self)

        self.conn = sqlite3.connect("main.db")
        self.curr = self.conn.cursor()
        
        self.master = master

        self.patientAlertLabel = None
        self.infoAlertLabel = None
        self.suggestions = None
        self.patientlist = self.curr.execute("""SELECT firstName, lastName FROM patients""").fetchall()

        self.view()
        

    def view(self):
        CTkLabel(self, width=300, height=60, text="Ajouter rendez-vous", fg_color=Colors.Liver, text_color=Colors.White, corner_radius=20, font=font(24)).pack(pady=15)

        CTkLabel(self,text="Patient:", font=font(24), text_color=Colors.White).place(x=44, y=118)
        CTkLabel(self, text="Date:", font=font(24), text_color=Colors.White).place(x=72, y=197)
        CTkLabel(self,text="Heure:", font=font(24), text_color=Colors.White).place(x=57, y=276)

        CTkLabel(self,text="/", font=font(15), text_color=Colors.White).place(x=197, y=198)
        CTkLabel(self,text="/", font=font(15), text_color=Colors.White).place(x=247, y=198)
        CTkLabel(self,text=":", font=font(15), text_color=Colors.White).place(x=252, y=277)

        self.patientInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="Patient", font=font(20), text_color=Colors.Cadet, width=200, height=30, corner_radius=10, justify=CENTER)
        self.patientInput.place(x=155, y=117)
        self.patientInput.bind("<KeyRelease>", lambda _:self.suggest())
        self.dayInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="J", font=font(15), text_color=Colors.Cadet, width=40, height=30, corner_radius=10, justify=CENTER)
        self.dayInput.place(x=155, y=196)

        self.monthInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="M", font=font(15), text_color=Colors.Cadet, width=40, height=30, corner_radius=10, justify=CENTER)
        self.monthInput.place(x=206, y=196)

        self.yearInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="Année", font=font(15), text_color=Colors.Cadet, width=100, height=30, corner_radius=10, justify=CENTER)
        self.yearInput.place(x=255, y=196)

        self.hourInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="Heure", font=font(20), text_color=Colors.Cadet, width=95, height=30, corner_radius=10, justify=CENTER)
        self.hourInput.place(x=155, y=275)

        self.minuteInput = CTkEntry(self, fg_color=Colors.White, border_width=1, border_color=Colors.Cadet, placeholder_text="Minute", font=font(20), text_color=Colors.Cadet, width=95, height=30, corner_radius=10, justify=CENTER)
        self.minuteInput.place(x=260, y=275)

        CTkButton(self, text="Ajouter", text_color=Colors.White, fg_color=Colors.Mandarin, hover_color=Colors.Sepia, width=250, height=45, font=font(30), corner_radius=15, command=self.save).place(x=75, y=335)



    def fill(self, event):
        for btn in self.btns:
            if str(btn).split(".") == str(event.widget).split(".")[:-1]:
                self.patientInput.delete(0, END)
                self.patientInput.insert(0, self.btns[btn])
                self.suggestions.destroy()
                return

    def suggest(self):

        if self.patientInput.get():
            suggestionslist = [patient for patient in self.patientlist if patient[1].lower().startswith(self.patientInput.get().lower()) or patient[0].lower().startswith(self.patientInput.get().lower()) or " ".join(patient).lower().startswith(self.patientInput.get().lower())]
            if suggestionslist:
                if self.suggestions:
                    self.suggestions.destroy()
                self.suggestions = CTkFrame(self, fg_color=Colors.Coral)
                self.suggestions.place(x=155, y=147)

                self.btns = {}

                for suggestion in suggestionslist:
                    btn = CTkButton(self.suggestions, text=suggestion, text_color=Colors.White, fg_color=Colors.Coral, corner_radius=0, border_width=1, font=font(16), width=200)
                    btn.pack()

                    self.btns[btn] = suggestion

                    btn.bind("<Button-1>", self.fill)

            else:
                if self.suggestions:
                    self.suggestions.destroy()
            

        else:
            if self.suggestions:
                self.suggestions.destroy()
                self.suggestions = None

    def save(self):
        if self.dayInput.get() and self.monthInput.get() and self.yearInput.get() and self.hourInput.get() and self.minuteInput.get():
            if int(self.dayInput.get()) in range(1,32) and int(self.monthInput.get()) in range(1,13) and int(self.yearInput.get()) >= datetime.now().year and int(self.hourInput.get()) in range(1,24) and int(self.minuteInput.get()) in range(60):
                print("if")
                if self.infoAlertLabel:
                    self.infoAlertLabel.destroy()

                meetingdate = f"{self.dayInput.get()}/{self.monthInput.get()}/{self.yearInput.get()} {self.hourInput.get()}:{self.minuteInput.get()}"
                try:
                    self.curr.execute("""SELECT id FROM "patients" WHERE firstName=? AND lastName=?""", (self.patientInput.get().split()[0], self.patientInput.get().split()[1]))
                    self.patientId = self.curr.fetchone()[0]
                    if self.patientAlertLabel:
                        self.patientAlertLabel.destroy()
                        self.patientAlertLabel=None
                
                except:
                    self.patientAlertLabel = CTkLabel(self, text="Ce patient N'existe pas!", font=font(20), fg_color=Colors.Danger, text_color=Colors.White, height=30)
                    self.patientAlertLabel.place(x=0, y=390, relwidth=1)
                    return
                
                self.curr.execute("""INSERT INTO "meetings" (patientId, datetime) values (?,?)""", (self.patientId, meetingdate))
                self.conn.commit()
                self.destroy()
                DailyMeetings(self.master).place(x=0, y=0, width=400, height=682)
            
            else:
                self.infoAlertLabel= CTkLabel(self, text="veuillez entrer toutes les informations correctement!", font=font(14), fg_color=Colors.Danger, text_color=Colors.White, height=30)
                self.infoAlertLabel.place(x=0, y=390, relwidth=1)
                

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

        self.topLevel = None

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
            command=self.addMeeting,
            image=CTkImage(
                light_image=Image.open("assets/imgs/add rdv icon.png"), size=(50, 50)
            ),
        ).place(x=326)

        self.meetingsFrame = CTkFrame(self, fg_color=Colors.Cadet)
        self.meetingsFrame.place(x=0, y=75, width=400, height=607)

        self.load()

    def addMeeting(self):
        def close():
            self.topLevel.destroy()
            self.topLevel = None

        if self.topLevel:
            self.topLevel.focus()
        else:
            self.topLevel = AddMeeting(self.master)     
            self.topLevel.protocol("WM_DELETE_WINDOW", close)

    def load(self):
        clear(self.meetingsFrame)
        meetings = self.window.curr.execute(
            """SELECT patientId, datetime FROM "meetings" """
        ).fetchall()

        

        pages = []

        for patientId, dt in meetings:
            if not pages or len(pages[-1]) == 4:
                pages.append([])

            dt = strToDatetime(dt)
            if datetime.now().date() == dt.date():

                firstname, lastname = self.window.curr.execute(""" SELECT firstName, lastName FROM patients WHERE id = ?""", (patientId,)).fetchone()

                pages[-1].append((" ".join([firstname.capitalize(), lastname.capitalize()]), dt))
    
        if not any([True if page else False for page in pages]):
            CTkLabel(self, text="Aucun rendez-vous", text_color=Colors.White, font=font(24)).place(relx=0.5, rely=0.5, anchor=CENTER)
            return

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
