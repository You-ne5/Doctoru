from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font
from PIL import Image, ImageDraw, ImageFont
from src.app import patients, navbar
from src.app import navbar
from assets.code.logic import calculateAge


class VisitBox(CTkFrame):
    def __init__(self, master: CTkFrame, patientId=None):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.window = master.window
        self.master = master

        self.patient = self.window.curr.execute("""SELECT * FROM "patients" WHERE id=?""", (patientId,)).fetchone()

        self.prescription = None
        self.medEntry=None
        self.doseEntry=None
        self.FRQ=None
        self.btnindex=0

        self.medsli=[]
        self.doseli=[]
        self.FRQli=[]
        self.prescriptionLi={}
        self.operations=None
        
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
            command = lambda:self.master.master.navBar.patientsButton.invoke()
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

        self.ordonnance_check = CTkCheckBox(
            self,
            text="Ordonnance",
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            font=font(25),
            width=25,
            height=25,
        )
        self.ordonnance_check.place(x=152, y=520)
        self.ordonnance_check.bind("<Button-1>", lambda _ : [self.load()])

        CTkButton(self, image=CTkImage(
                light_image=Image.open("assets/imgs/printer icon.png"), size=(35, 31)
            ),
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            corner_radius=35,
            text="",
            command=lambda:self.show()
            ).place(x=453, y=578, width=60, height=60)


    def logic(self):
        self.patientlist = self.window.curr.execute("""SELECT firstName, lastName FROM patients""").fetchall()

        self.suggestions = None

        self.patientEntry.bind("<KeyRelease>", lambda _: self.suggest())



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
                self.motif,
                self.taille,
                self.poids,
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

                self.refresh()
                self.load()
                
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

    def load(self):

        if not self.ordonnance_check.get():
            CTkFrame(self.master, height=680, width=680, fg_color=Colors.Coral).place(x=0,y=0)
            self.refresh()
            return


        if len(self.patientEntry.get().split())==2:
            patient = self.window.curr.execute("""SELECT * FROM "patients" WHERE firstName=? AND lastName =?""", self.patientEntry.get().split()).fetchone()
        else:
            patient=None
    
            
        self.ordImage = Image.open("assets/imgs/ordonnance.png")
        ordFont=ImageFont.truetype("assets/imgs/bold.ttf", 12)

        self.I1 = ImageDraw.Draw(self.ordImage)
        self.I1.text(xy=(295, 34), text=datetime.now().strftime("%d/%m/%Y"), fill=(11, 49, 139), font=ordFont)
        if patient:
            self.I1.text(xy=(307, 56), text=patient[1].capitalize(), fill=(11, 49, 139), font=ordFont)
            self.I1.text(xy=(325, 79), text=patient[2].capitalize(), fill=(11, 49, 139), font=ordFont)
            self.I1.text(xy=(304, 99), text=calculateAge(patient[3]), fill=(11, 49, 139), font=ordFont)


        self.ordonnance = CTkLabel(self.master, image=CTkImage(self.ordImage, size=(430,600)), text="")
        self.ordonnance.place(x=128, y=36)

        self.operations = CTkFrame(self.ordonnance, width=428, height=355, fg_color=Colors.White, corner_radius=0)
        self.operations.place(x=0, y=190)

        if not self.medsli:

            self.addMedBtn = CTkButton(
            self.operations,
            height=23,
            width=23,
            text="+",
            fg_color=Colors.Mandarin,
            text_color=Colors.White,
            bg_color=Colors.White,
            corner_radius=15,
            font=font(20),
            hover_color=Colors.Sepia,
            command = lambda: self.addmed(0)
        )
            self.addMedBtn.pack(pady=10, padx=15, side="left")

        else:
            i=1
            for med in self.medsli:
                self.addmed(med, i)
                i+=1


    def show(self):
            self.refresh()
            i=0
            for med in self.medsli:
                self.I1.text(xy=(15,206+65*i), text=str(i+1), fill=(11, 49, 139), font=ImageFont.truetype("assets/imgs/bold.ttf", 15))
                self.I1.text(xy=(32,206+65*i), text=med[0], fill=(11, 49, 139), font=ImageFont.truetype("assets/imgs/bold.ttf", 15))
                self.I1.text(xy=(196,223+65*i), text=med[1], fill=(11, 49, 139), font=ImageFont.truetype("assets/imgs/bold.ttf", 13))
                self.I1.text(xy=(372,206+65*i), text=med[2], fill=(11, 49, 139), font=ImageFont.truetype("assets/imgs/bold.ttf", 13))
                i+=1
            self.ordImage.show()

                

    def addmed(self, medsli=None, medindex=None):
        try:
            self.addMedBtn.destroy()
        except:
            pass

        med_index = len([f for f in self.operations.winfo_children() if isinstance(f, CTkFrame)])+1
        if med_index>=7:
            return

        self.prescription = CTkFrame(self.operations, fg_color=Colors.White, width=428, height=42, corner_radius=10, bg_color=Colors.White)
        self.prescription.pack(pady=2.5)

        CTkLabel(self.prescription, text=medindex if medindex else med_index, bg_color=Colors.White, text_color=Colors.ord_blue , height=14, width=14, corner_radius=15, font=font(11)).place(x=10, y=15)

        self.medEntry = CTkEntry(self.prescription, text_color=Colors.Cadet, fg_color=Colors.White, bg_color=Colors.White, corner_radius=5, width=130, height=22, placeholder_text="Madicament", placeholder_text_color=Colors.Silver, justify=CENTER)
        self.medEntry.place(x=38,y=10)

        self.doseEntry = CTkEntry(self.prescription, text_color=Colors.Cadet, fg_color=Colors.White, bg_color=Colors.White, corner_radius=5, width=130, height=22, placeholder_text="Dose", placeholder_text_color=Colors.Silver, justify=CENTER)
        self.doseEntry.place(x=177, y=10)

        self.FRQ = CTkEntry(self.prescription, text_color=Colors.Cadet, fg_color=Colors.White, bg_color=Colors.White, corner_radius=5, width=50, height=22, placeholder_text="FRQ", placeholder_text_color=Colors.Silver, justify=CENTER)
        self.FRQ.place(x=316, y=10)

        self.addMedBtn = CTkButton(self.operations,height=23,width=23,text="+",fg_color=Colors.Mandarin,text_color=Colors.White,bg_color=Colors.White,corner_radius=15, font=font(20), hover_color=Colors.Sepia, command = lambda: self.addmed(self.btnindex))
        self.addMedBtn.pack(pady=10, padx=15, side="right")


        removebtn = CTkButton(self.prescription, width=23, height=23, text="X", fg_color=Colors.Mandarin, hover_color=Colors.Sepia, bg_color=Colors.White, corner_radius=5, command=lambda:self.removemed(removebtn))
        removebtn.place(x=382, y=10)

        self.prescriptionLi[removebtn]=self.prescription

        if medsli:

            if medsli[0]:
                self.medEntry.insert(0, medsli[0])
    
            if medsli[1]:
                self.doseEntry.insert(0, medsli[1])
        
            if medsli[2]:
                self.FRQ.insert(0, medsli[2])
        
        self.refresh()



    def removemed(self, btn):

        self.refresh()

        li=[entry.get() for entry in self.prescriptionLi[btn].winfo_children() if isinstance(entry, CTkEntry)]

        if self.medsli:

            self.medsli.pop(self.medsli.index(li))

            self.load()
        else:
            self.prescriptionLi[btn].destroy()
            del self.prescriptionLi[btn]
    

    def refresh(self):
        self.medsli=[]

        for prescription in self.operations.winfo_children():
            if isinstance(prescription, CTkFrame):

                self.medsli.append([entry.get() for entry in prescription.winfo_children() if isinstance(entry, CTkEntry)])
                    



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
