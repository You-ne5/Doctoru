from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font, center
from PIL import Image, ImageDraw, ImageFont
from src.app import patients, navbar

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
            command = lambda:self.master.master.nav_bar.patientsButton.invoke()
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
            self.refresh()
            self.window.curr.execute("""INSERT INTO "visits" (patientId, datetime, reason, height, weight, conclusion, montant, DEP, medsli) VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                self.patientid,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                self.motif,
                self.taille,
                self.poids,
                self.conclution,
                self.montant,
                self.DEP,
                str(self.medsli)
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
        ordFont=ImageFont.truetype("assets/fonts/bold.ttf", 12)

        self.I1 = ImageDraw.Draw(self.ordImage)
        self.I1.text(xy=(295, 34), text=datetime.now().strftime("%d/%m/%Y"), fill=(11, 49, 139), font=ordFont)
        if patient:
            self.I1.text(xy=(307, 56), text=patient[2].capitalize(), fill=(11, 49, 139), font=ordFont)
            self.I1.text(xy=(325, 79), text=patient[1].capitalize(), fill=(11, 49, 139), font=ordFont)
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
                details = f"{med[2]} pendant {med[1]}"
                self.I1.text(xy=(50,206+65*i), text=str(i+1), fill=(11, 49, 139), font=ImageFont.truetype("assets/fonts/bold.ttf", 20))
                self.I1.text(xy=(67,206+65*i), text=med[0], fill=(11, 49, 139), font=ImageFont.truetype("assets/fonts/bold.ttf", 20))
                self.I1.text(xy=(91,242+65*i), text = f"- {details}", fill=(11, 49, 139), font=ImageFont.truetype("assets/fonts/TT Norms Pro Regular.otf", 17))
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

        self.prescriptionLi[removebtn] = self.prescription

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
        if self.operations:
            for prescription in self.operations.winfo_children():
                if isinstance(prescription, CTkFrame):

                    self.medsli.append([entry.get() for entry in prescription.winfo_children() if isinstance(entry, CTkEntry)])
                    

class VisitInfo(CTkFrame):
    def __init__(self, master: CTkFrame, visitId):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)

        self.window = master.window
        self.master = master
        self.visitId = visitId
        self.editvisit=None

        id , self.patientid, self.datetime, self.reason, self.height, self.weight, self.conclusion, self.montant, self.DEP, medsli = self.window.curr.execute("""SELECT * FROM "visits" WHERE id=?""",(self.visitId,)).fetchone()
        self.medsli = eval(medsli)

        self.view()

    def view(self):
        title = CTkLabel(self, text="Informations de visite", fg_color=Colors.Liver, text_color=Colors.White, font=font(38), height=76, width=430, corner_radius=15)
        title.place(x=200, y=12)

        self.visit_info_card = CTkFrame(self, fg_color=Colors.Cadet, bg_color=Colors.Coral, corner_radius=16, width=336, height=425)
        self.visit_info_card.place(x=39 if self.medsli else 272, y=116)
        #visit infos
        CTkLabel(self.visit_info_card, text=f"Date: {str(self.datetime).split()[0]}", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=30)
        CTkLabel(self.visit_info_card, text=f"Heure: {str(self.datetime).split()[1]}", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=75)
        CTkLabel(self.visit_info_card, text=f"Motif: {self.reason}", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=120)
        CTkLabel(self.visit_info_card, text=f"Poids: {self.weight}kg", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=165)
        CTkLabel(self.visit_info_card, text=f"Taille: {self.height}cm", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=210)
        CTkLabel(self.visit_info_card, text=f"Conclusion: {self.conclusion}", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=255)
        CTkLabel(self.visit_info_card, text=f"Montant: {self.montant}DA", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=300)
        CTkLabel(self.visit_info_card, text=f"DEP: {self.DEP}", font=font(16), text_color=Colors.White, bg_color=Colors.Cadet).place(x=20, y=345)
        
        edit_visit_button = CTkButton(self.visit_info_card, text="Modifier", fg_color=Colors.Mandarin, bg_color=Colors.Cadet, corner_radius=12, text_color=Colors.White, hover_color=Colors.Sepia, height=36, width=192, font=font(20), command=lambda:self.editview())
        edit_visit_button.place(x=72, y=378)

        delete_visit_button = CTkButton(self, text="Supprimer la visite", fg_color=Colors.Danger, bg_color=Colors.Coral, corner_radius=12, text_color=Colors.White, hover_color=Colors.Sepia, height=61, width=336, font=font(20), command=lambda:self.delete_visit())
        delete_visit_button.place(x=40, y=570)

        if self.medsli:
            first_name, last_name, date_of_birth = self.window.curr.execute("""SELECT firstName, lastName, dateOfBirth from "patients" WHERE id=?""", (self.patientid,)).fetchone()

            self.ordImage = Image.open("assets/imgs/ordonnance.png")
            ordFont=ImageFont.truetype("assets/fonts/bold.ttf", 12)
            ORDBLUE = (11, 49, 139)

            self.I1 = ImageDraw.Draw(self.ordImage)
            self.I1.text(xy=(295, 34), text=self.datetime.split()[0], fill=ORDBLUE, font=ordFont)

            self.I1.text(xy=(307, 56), text=last_name.capitalize(), fill=ORDBLUE, font=ordFont)
            self.I1.text(xy=(325, 79), text=first_name.capitalize(), fill=ORDBLUE, font=ordFont)
            self.I1.text(xy=(304, 99), text=calculateAge(date_of_birth), fill=ORDBLUE, font=ordFont)
            
            med_index=0
            for med_name, med_dose, med_frq in self.medsli:
                details = f"{med_frq} pendant {med_dose}"
                distance_between_meds = 70

                #med number
                self.I1.text(
                    xy=(25, 206 + distance_between_meds * med_index), 
                    text=str(med_index+1)+"- ", 
                    fill=ORDBLUE, 
                    font=ImageFont.truetype("assets/fonts/bold.ttf", 20)
                    )
                #med name
                self.I1.text(
                    xy=(42, 206 + distance_between_meds * med_index), 
                    text=med_name, 
                    fill=ORDBLUE, 
                    font=ImageFont.truetype("assets/fonts/bold.ttf", 20)
                    )
                #med med infos
                self.I1.text(
                    xy=(91, 235 + distance_between_meds * med_index), 
                    text = f"- {details}", 
                    fill=ORDBLUE, 
                    font=ImageFont.truetype("assets/fonts/TT Norms Pro Regular.otf", 17)
                    )
                
                med_index+=1

            self.ordonnance = CTkLabel(self, image=CTkImage(self.ordImage, size=(360,507)), text="")
            self.ordonnance.place(x=440, y=100)

    def editview(self):
        def close():
            self.editvisit.destroy()
            self.editvisit = None

        if self.editvisit:
            self.editvisit.focus()
        else:
            self.editvisit = CTkToplevel(fg_color=Colors.Cadet)
            self.editvisit.resizable(False, False)

            self.editvisit.title("Modifier la visite")

            self.editvisit.protocol("WM_DELETE_WINDOW", lambda: close())
            
            center(400, 500, self.editvisit)

            CTkLabel(
                self.editvisit,
                text="Modifier la visite",
                fg_color=Colors.Liver,
                text_color=Colors.White,
                font=font(22),
                corner_radius=15,
            ).place(x=82, y=16, height=51, width=246)

            CTkLabel(self.editvisit, text="Date:", text_color=Colors.White, font=font(17)).place(x=110, y=90)
            CTkLabel(self.editvisit, text="Heure:", text_color=Colors.White, font=font(17)).place(x=110, y=134)
            CTkLabel(self.editvisit, text="Motif:", text_color=Colors.White, font=font(17)).place(x=110, y=178)
            CTkLabel(self.editvisit, text="Poids:", text_color=Colors.White, font=font(17)).place(x=110, y=222)
            CTkLabel(self.editvisit, text="Taille:", text_color=Colors.White, font=font(17)).place(x=110, y=265)
            CTkLabel(self.editvisit, text="Conclusion:", text_color=Colors.White, font=font(17)).place(x=100, y=310)
            CTkLabel(self.editvisit, text="DEP:", text_color=Colors.White, font=font(17)).place(x=110, y=350)
            CTkLabel(self.editvisit, text="Montant:", text_color=Colors.White, font=font(17)).place(x=110, y=390)

            self.DateEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.DateEntry.place(x=215, y=90, width=140, height=26)
            self.DateEntry.insert(0, str(self.datetime).split()[0])

            self.TimeEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.TimeEntry.place(x=215, y=134, width=140, height=26)
            self.TimeEntry.insert(0, str(self.datetime).split()[1])
            
            self.MotifEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.MotifEntry.place(x=215, y=178, width=140, height=26)
            self.MotifEntry.insert(0, self.reason)

            self.weightEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.weightEntry.place(x=215, y=222, width=140, height=26)
            self.weightEntry.insert(0, self.weight)

            self.heightEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.heightEntry.place(x=215, y=266, width=140, height=26)
            self.heightEntry.insert(0, self.height)

            self.conclusionEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.conclusionEntry.place(x=215, y=310, width=140, height=26)
            self.conclusionEntry.insert(0, self.conclusion)

            self.DEPEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.DEPEntry.place(x=215, y=354, width=140, height=26)
            self.DEPEntry.insert(0, self.DEP)

            self.montantEntry = CTkEntry(
                self.editvisit,
                fg_color=Colors.White,
                corner_radius=10,
                placeholder_text="",
                text_color=Colors.Cadet,
            )
            self.montantEntry.place(x=215, y=398, width=140, height=26)
            self.montantEntry.insert(0, self.montant)
            


            self.confirm = CTkButton(self.editvisit, text="Sauvegarder", text_color=Colors.White, fg_color=Colors.Silver, hover_color=Colors.Sepia, state=False, font=font(16), command=lambda: self.edit())
            self.confirm.place(x=193, y=445, width=150, height=42)

            self.cancel = CTkButton(self.editvisit, text="Annuler", fg_color=Colors.Silver, font=font(16), hover_color=Colors.Mandarin, command=close)
            self.cancel.place(x=34, y=445, width=120, height=42)


            entrys = [wdj for wdj in self.editvisit.winfo_children() if isinstance(wdj, CTkEntry)]    
            for entry in entrys:
                entry.bind("<KeyRelease>", lambda event:check())
            
            def check():

                checks = {
                    self.DateEntry.get() : str(self.datetime).split()[0],
                    self.TimeEntry.get(): str(self.datetime).split()[1],
                    self.MotifEntry.get() : str(self.reason),
                    self.weightEntry.get() : str(self.weight),
                    self.heightEntry.get() : str(self.height),
                    self.DEPEntry.get() : str(self.DEP),
                    self.montantEntry.get() : str(self.montant),
                    self.conclusionEntry.get() : str(self.conclusion)
                    }
                
                changed = any(i!=checks[i] for i in checks)
                if changed:
                    self.confirm.configure(fg_color=Colors.Mandarin)
                    self.confirm.configure(state=NORMAL)
                else:
                    self.confirm.configure(fg_color=Colors.Silver)
                    self.confirm.configure(state=False)
                
    def edit(self):
            def dateofBirthcheck(Bday):
                try:
                    if Bday:
                        return datetime.strptime(Bday, "%d/%m/%Y")
                    else:
                        return None
                except:
                    return "problem"
                
            verification = True
            New_infos = {"date" : dateofBirthcheck(self.DateEntry.get()),
                        "time" : self.TimeEntry.get(),
                        "reason" : self.MotifEntry.get(),
                        "height" : float(self.heightEntry.get()),
                        "weight" : float(self.weightEntry.get()),
                        "montant" : int(self.montantEntry.get()),
                        "conclusion" : self.conclusionEntry.get(),
                        "DEP" : int(self.DEPEntry.get()),

                        }
            if any((not info or info=="problem") for info in list(New_infos.values())[:-1]):
                verification = False
            try:
                New_infos["height"] = float(New_infos["height"])
                New_infos["weight"] = float(New_infos["weight"])
                New_infos["montant"] = int(New_infos["montant"])
                New_infos["DEP"] = int(New_infos["DEP"])
            except:
                verification = False

            if verification:

                self.window.curr.execute("""UPDATE "visits" SET 
                datetime=?, 
                reason=?, 
                height=?, 
                weight=?, 
                conclusion=?, 
                montant=?,
                DEP=?
                WHERE id=?""",
                (
                f"{New_infos['date'].strftime('%d/%m/%Y')} {New_infos['time']}", 
                New_infos["reason"], 
                New_infos["height"], 
                New_infos["weight"],
                New_infos["conclusion"], 
                New_infos["montant"], 
                New_infos["DEP"], 
                self.visitId
                )
                )
                self.window.conn.commit()

                self.editvisit.destroy()

                VisitInfo(self.master, self.visitId).place(x=400, y=0, width=879, height=681)
            else:
                self.AlertLabel = CTkLabel(self.editvisit, text="Veuillez entrer toute les informations requise correctement" if New_infos["date"]!="problem" else "Veuillez entrer la date dans le bon format ex: 15/11/2006", font=font(12), fg_color=Colors.Danger, text_color=Colors.White, height=20)
                self.AlertLabel.place(x=0,y=483, relwidth=1)
    
    def delete_visit(self):
        self.del_visit_window  =  CTkToplevel(fg_color = Colors.Coral)
        self.del_visit_window.resizable(False, False)
        center(574, 245, self.del_visit_window)

        def close():
            self.del_visit_window.destroy()

        def delete():
            self.window.curr.execute("""DELETE FROM "visits" WHERE id = ?""", (self.visitId,))
            self.window.conn.commit()

            close()
            CTkFrame(self.master, height=682, width=879, fg_color=Colors.Coral).place(x=401, y=0)
            VisitsHistoryList(self.master, self.patientid).place(x = 0, y = 0, width = 400, height = 682)

        CTkLabel(self.del_visit_window, text = "Supprimer le patient", fg_color = Colors.Liver, font = font(25), text_color = Colors.White, corner_radius = 15).place(x = 124, y = 34, width = 320, height = 70)
        CTkLabel(self.del_visit_window, text = f"Étes vous sure de vouloir supprimer cette visite?", font = font(16), text_color = Colors.White).place(relx = 0.5, rely = 0.51, anchor = CENTER)

        CTkButton(self.del_visit_window, text = "Supprimer", fg_color = Colors.Danger, text_color = Colors.White, hover_color = Colors.Danger_hover, command = delete, font = font(15)).place(x = 308, y = 178, width = 130, height = 50)
        CTkButton(self.del_visit_window, text = "Annuler", fg_color = Colors.Silver, text_color = Colors.White, hover_color = Colors.Mandarin, command = close, font = font(15)).place(x = 140, y = 178, width = 130, height = 50)



class VisitsHistoryList(CTkFrame):
    def __init__(self, master:CTkFrame, patientId):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.window = master.window
        self.master = master
        self.patientId = patientId
        self.currentpage = 0
        self.Selectedvisit=None
        self.patient = self.window.curr.execute("""SELECT * FROM "patients" WHERE id=?""", (self.patientId,)).fetchone()

        self.view()
        self.load()

    def view(self):
        header = CTkFrame(self, fg_color=Colors.Mandarin, corner_radius=0, height=75)
        header.pack(fill="x")

        CTkLabel(
            header, text=f"historique des visites", font=font(23), text_color=Colors.White
        ).place(x=55, y=10)
        CTkLabel(
            header, text=f"{str(self.patient[1]).capitalize()} {str(self.patient[2]).capitalize()}", font=font(23), text_color=Colors.Coral
        ).place(x=72, y=41)

        CTkButton(
            header,
            fg_color=Colors.Mandarin,
            hover_color=Colors.Sepia,
            corner_radius=0,
            width=75,
            height=74,
            text="",
            image=CTkImage(
                light_image=Image.open("assets/imgs/add visit icon.png"),
                size=(50, 50),
            ),
            command=lambda: VisitsPage(self.master.master.master).place(x=0, y=150, width=1280, height=682)
        ).place(x=326)

        self.searchvisit = CTkEntry(
            self,
            placeholder_text="Rechercher une visite...",
            height=25,
            font=font(15),
            text_color=Colors.Cadet,
            fg_color=Colors.White,
            border_width=0,
            corner_radius=0,
        )
        self.searchvisit.pack(fill="x")

        self.visitsFrame = CTkFrame(self, fg_color=Colors.Cadet)
        self.visitsFrame.pack(fill="both", expand=True)

        self.load()

        self.searchvisit.bind("<Key>", lambda _: self.load())
        self.searchvisit.bind("<Return>", lambda _: self.load())


    def historiquevisites(self, visitid):
        VisitInfo(self.master, visitid).place(
                        x=400, y=0, width=879, height=681
                    ),

    def load(self):
        clear(self.visitsFrame)

        visits = self.master.master.window.curr.execute(
            """SELECT id, datetime FROM "visits" WHERE patientId=?""",(self.patientId,)
        ).fetchall()

        pages = []

        search = self.searchvisit.get().lower()
        if not visits:
            CTkLabel(self, text="Aucune visite", text_color=Colors.White, font=font(24)).place(relx=0.5, rely=0.5, anchor=CENTER)
            return

        for id, datetime in visits:
            if not pages or len(pages[-1]) == 4:
                pages.append([])
            
            if search: 
                if str(datetime).startswith(search):   
                    pages[-1].append((id, datetime))
            else:
                pages[-1].append((id, datetime))

        self.visitsButtons = {}

        for id, datetime in pages[self.currentpage]:
            visitCard = CTkFrame(
                self.visitsFrame,
                width=350,
                height=100,
                corner_radius=20,
                fg_color=Colors.Coral,
            )
            visitCard.pack(pady=15)

            visitsButton = CTkButton(
                visitCard,
                text=f"{str(datetime).split()[0]}",
                font=font(30),
                corner_radius=15,
                height=41,
                width=20 * len(str(datetime).split()[0]),
                hover_color=Colors.Cadet,
                text_color=Colors.Mandarin,
                fg_color=Colors.Coral,
                command=lambda :None
            )
            visitsButton.place(x=5, y=10)

            self.visitsButtons[visitsButton] = id
            visitsButton.bind("<Button-1>", lambda _:[
                    self.select(button(_)[0]),
                    self.historiquevisites(button(_)[1])
                ])

            def button(event):
                for btn in self.visitsButtons:
                    if str(btn) in str(event.widget):
                        return btn, self.visitsButtons[btn]

            CTkLabel(
                visitCard,
                text=f"{str(datetime).split()[1]} ",
                font=font(20),
                text_color=Colors.White,
            ).place(x=21, y=59)

        CTkButton(
            self.visitsFrame,
            text="<",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.currentpage else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.currentpage else Colors.Silver,
            command=lambda: self.update(-1 if self.currentpage else 0),
        ).place(x=104, y=522)
 
        CTkLabel(
            self.visitsFrame,
            text=self.currentpage + 1,
            font=font(30),
            text_color=Colors.White,
        ).place(x=190, y=523)

        CTkButton(
            self.visitsFrame,
            text=">",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.currentpage < len(pages) - 1 else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.currentpage < len(pages) - 1 else Colors.Silver,
            command=lambda: self.update(+1 if self.currentpage < len(pages) - 1 else 0),
        ).place(x=238, y=522)

    def select(self, button):
        for visit_button in self.visitsButtons:
            visit_button.configure(fg_color=Colors.Coral, text_color=Colors.Mandarin, hover=True)

        button.configure(fg_color=Colors.Mandarin, text_color=Colors.Cadet, hover=False)
        self.Selectedvisit = self.visitsButtons[button]

    def update(self, num):
        if num:
            self.currentpage += num
            self.load()
            
        if self.Selectedvisit:
            for visit_button in self.visitsButtons:
                if self.Selectedvisit == self.visitsButtons[visit_button]:
                    self.select(visit_button)
 

class VisitsPage(CTkFrame):
    def __init__(self, master: CTkFrame, patientId=None, historiquedesvisites=False) -> None:
        clear(master)
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.patientId = patientId
        self.historique = historiquedesvisites
        self.window = master.window
        self.master = master

        self.view()

    def view(self):
        if not self.historique:
            VisitBox(self, self.patientId).place(x=680, y=0, height=682, width=600)
        else:
            VisitsHistoryList(self, self.patientId).place(x=0, y=0, width=400, height=682)
