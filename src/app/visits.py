from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font
from PIL import Image
from src.app import patients, navbar

class VisitBox(CTkFrame):
    def __init__(self, master: CTkFrame, patientId=None):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.window = master.window
        self.master = master

        self.patient = self.window.curr.execute("""SELECT * FROM "patients" WHERE id=?""", (patientId,)).fetchone()

        self.view()
        self.logic()
        

    def view(self):
        title = CTkLabel(
            self,
            text="Ajouter une visite",
            fg_color=Colors.Liver,
            corner_radius=20,
            font=font(30),
        )
        title.place(x=85, y=30, height=76, width=430)

        self.patientEntry = CTkEntry(
            self,
            placeholder_text="Patient",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.patientEntry.place(x=151, y=125, height=45, width=300)
        if self.patient:
            self.patientEntry.insert(0, " ".join([self.patient[1], self.patient[2]]))
    
        self.poidsEntry=CTkEntry(
            self,
            placeholder_text="Poids(kg)",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.poidsEntry.place(x=150, y=190, height=45, width=140)

        self.tailleEntry=CTkEntry(
            self,
            placeholder_text="Taille(cm)",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.tailleEntry.place(x=310, y=190, height=45, width=140)

        self.motif_entry = CTkEntry(
            self,
            placeholder_text="Motif",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.motif_entry.place(x=150, y=255, height=45, width=300)

        self.conclutionEntry = CTkEntry(
            self,
            placeholder_text="Conclution",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.conclutionEntry.place(x=150, y=320, height=45, width=300)

        self.montantEntry = CTkEntry(
            self,
            placeholder_text="Montant",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.montantEntry.place(x=150, y=385, height=45, width=300)

        self.DEPentry = CTkEntry(
            self,
            placeholder_text="DEP",
            fg_color=Colors.White,
            text_color=Colors.Cadet,
            corner_radius=16,
            justify=CENTER,
            font=font(23),
        )
        self.DEPentry.place(x=150, y=450, height=45, width=300)

        CTkButton(
            self,
            height=30,
            width=30,
            text="+",
            fg_color=Colors.Mandarin,
            text_color=Colors.White,
            corner_radius=15,
            font=font(20),
            hover_color=Colors.Sepia,
            command = lambda:navbar.NavBar(self.master.master).patientsButton.invoke()
        ).place(x=465, y=130)

        CTkButton(
            self,
            fg_color=Colors.Mandarin,
            text="Ajouter",
            corner_radius=20,
            font=font(30),
            hover_color=Colors.Sepia,
            command=self.addvisit
        ).place(x=175, y=578, width=250, height=60)

        CTkCheckBox(
            self,
            text="Ordonnance",
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            font=font(25),
            width=25,
            height=25,
        ).place(x=152, y=520)

        CTkButton(self, image=CTkImage(
                light_image=Image.open("assets/imgs/printer icon.png"), size=(35, 31)
            ),
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            corner_radius=35,
            text=""
            ).place(x=453, y=578, width=60, height=60)


    def logic(self):
        self.patientlist = self.window.curr.execute("""SELECT firstName, lastName FROM patients""").fetchall()

        self.suggestions = None

        self.patientEntry.bind("<KeyRelease>", lambda _: self.suggest())

        self.patientEntry.bind("<Return>", lambda _: self.suggest())


    def addvisit(self):
        patient=self.patientEntry.get().split()
        if patient:
            self.patientid = self.window.curr.execute("""SELECT id FROM  "patients" WHERE firstName=? AND lastName=?""", (patient[0], patient[1])).fetchone()[0]
        else:
            self.patientid = None
        self.poids = self.poidsEntry.get()
        self.taille = self.tailleEntry.get()
        self.motif = self.motif_entry.get()
        self.conclution = self.conclutionEntry.get()
        self.montant = self.montantEntry.get()
        self.DEP = self.DEPentry.get() if self.DEPentry.get() else None

        try:
            int(self.poids)
        except:
            self.poids=None
        try:
            int(self.taille)
        except:
            self.taille=None
        try:
            int(self.montant)
        except:
            self.montant=None
        try:
            if self.DEP:
                int(self.DEP)
        except:
            self.DEP="problem"




        if self.patientid and self.poids and self.taille and self.motif and self.conclution and self.montant and self.DEP!="problem":
            self.window.curr.execute("""INSERT INTO "visits" (patientId, datetime, reason, height, weight, conclusion, montant, DEP) VALUES (?,?,?,?,?,?,?,?)""",
            (
                self.patientid,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                self.poids,
                self.taille,
                self.motif,
                self.conclution,
                self.montant,
                self.DEP,
            )
            )
            self.window.conn.commit()
            CTkLabel(self, fg_color=Colors.Success, text="Visite ajoutée avec succes", text_color=Colors.White, font=font(23)).place(x=0, y=647, relwidth=1, height=34)
        else:
            CTkLabel(self, fg_color=Colors.Danger, text="Veuillez entrer toute les informations correctement", text_color=Colors.White, font=font(20)).place(x=0, y=647, relwidth=1, height=34)
            
    def fill(self, event):
        for btn in self.btns:
            if str(btn).split(".") == str(event.widget).split(".")[:-1]:
                self.patientEntry.delete(0, END)
                self.patientEntry.insert(0, self.btns[btn])
                self.suggestions.destroy()
                return

    def suggest(self):

        if self.patientEntry.get():
            suggestionslist = [patient for patient in self.patientlist if patient[1].lower().startswith(self.patientEntry.get().lower()) or patient[0].lower().startswith(self.patientEntry.get().lower()) or " ".join(patient).lower().startswith(self.patientEntry.get().lower())]
            if suggestionslist:
                if self.suggestions:
                    self.suggestions.destroy()
                self.suggestions = CTkFrame(self, fg_color=Colors.Coral)
                self.suggestions.place(x=150, y=170)

                self.btns = {}

                for suggestion in suggestionslist:
                    btn = CTkButton(self.suggestions, text=suggestion, text_color=Colors.White, fg_color=Colors.Coral, corner_radius=0, border_width=1, width=300, font=font(20))
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

class VisitsPage(CTkFrame):
    def __init__(self, master: CTkFrame, patientId=None) -> None:
        clear(master)
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.patientId = patientId

        self.window = master.window
        self.master = master


        self.view()

    def view(self):
        VisitBox(self, self.patientId).place(x=680, y=0, height=682, width=600)
