from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font, center
from PIL import Image
from assets.code.logic import calculateAge, strToDatetime
from src.app import visits

class confirm(CTkToplevel):
    def __init__(self, patientname, patientid, master):
        super().__init__(fg_color = Colors.Cadet)

        self.master  =  master
        self.patientname  =  patientname
        self.patientid  =  patientid

        self.title("Confirmation de patient")

        self.resizable(False, False)
        center(477, 200, self)

        self.view()

    def close(self):
            self.destroy()
            self.master.verif  =  None 

    def view(self):
        CTkLabel(
            self, 
            text  =  "Ce Patient existe deja!",
            text_color  =  Colors.White,
            font  =  font(28),
            corner_radius  =  10,
            fg_color  =  Colors.Liver, 
        ).place(x =  64, y =  20, height =  45, width =  350)

        CTkLabel(
            self, 
            text  =  f"Le pateint {self.patientname} existe deja!",
            text_color  =  Colors.White,
            font  =  font(16)
        ).place(x =  125,y =  75)
        
        CTkLabel(
            self, 
            text  =  f"""voulez vous continuer quand-meme?""", 
            text_color  =  Colors.White,
            font  =  font(16), 
        ).place(x =  93,y =  95)

        CTkButton(
            self, 
            text = "Continuer", 
            font  =  font(18), 
            corner_radius  =  18, 
            fg_color  =  Colors.Danger, 
            hover_color  =  Colors.Warning, 
            command  =  lambda: [self.master.add_patient(), self.close()]
        ).place(x =  340, y =  135, height =  50, width =  120)

        CTkButton(
            self, 
            text  =  "Acceder au patient", 
            font  =  font(12),
            corner_radius  =  16,
            fg_color  =  Colors.Mandarin, 
            hover_color  =  Colors.Sepia, 
            command  =  lambda : [self.close(), PatientsList(self.master.master).patient_infos(self.patientid)]
        ).place(x =  170, y =  135, height =  50, width =  154)

        CTkButton(
            self,
            text  =  "Annuler",
            font  =  font(18), 
            corner_radius  =  18,
            fg_color  =  Colors.Silver, 
            hover_color  =  Colors.Warning, 
            command  =  self.close
        ).place(x =  15, y =  135, height =  50, width =  100)


class AddPatient(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius = 0, fg_color = Colors.Coral)

        self.master  =  master
        self.window  =  master.window

        self.verif  =  None

        self.view()

    def view(self):
        title  =  CTkLabel(
            self,
            text = "Ajouter un patient",
            font = font(45),
            fg_color = Colors.Liver,
            text_color = Colors.White,
            corner_radius = 20,
            height = 75,
            width = 430,
        )
        title.pack(pady = 15)

        add_patient_card  =  CTkFrame(self, corner_radius = 20, fg_color = Colors.Cadet)
        add_patient_card.place(x = 21, y = 120, width = 839, height = 496)

        self.lastNameEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Nom",
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            font  =  font(23),
            corner_radius  =  14,
            fg_color  =  Colors.White,
            justify  =  CENTER,
        )
        self.lastNameEntry.place(x = 50, y = 34, width = 300, height = 46)

        self.firstNameEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Prénom",
            justify = CENTER,
            font = font(23),
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            corner_radius = 14,
            fg_color = Colors.White,
        )
        self.firstNameEntry.place(x = 50, y = 129, width = 300, height = 46)

        self.dateOfBirthEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Date de naissance",
            justify = CENTER,
            font = font(23),
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            corner_radius = 14,
            fg_color = Colors.White,
        )
        self.dateOfBirthEntry.place(x = 50, y = 220, width = 300, height = 46)


        self.gender_entry  =  CTkComboBox(
            add_patient_card,
            values =  ["Genre", "Garçon", "Fille"],
            font = font(20),
            justify = CENTER,
            text_color = Colors.Cadet,
            dropdown_fg_color = Colors.Liver,
            corner_radius = 14,
            fg_color = Colors.White,
            width = 300,
            height = 46,
            dropdown_font = font(20)
        )
        self.gender_entry.place(x = 51, y = 313)


        self.maladiesChroniquesEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Maladies Chroniques",
            justify = CENTER,
            font = font(23),
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            corner_radius = 14,
            fg_color = Colors.White,
        )
        self.maladiesChroniquesEntry.place(x = 480, y = 34, width = 300, height = 46)

        self.phoneNumberEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Téléphone (optionnel)",
            justify = CENTER,
            font = font(23),
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            corner_radius = 14,
            fg_color = Colors.White,
        )
        self.phoneNumberEntry.place(x = 480, y = 126, width = 300, height = 46)

        self.keywordsEntry  =  CTkEntry(
            add_patient_card,
            placeholder_text = "Mots clés(optionel)",
            justify = CENTER,
            font = font(23),
            placeholder_text_color = Colors.Silver,
            text_color = Colors.Cadet,
            corner_radius = 14,
            fg_color = Colors.White,
        )
        self.keywordsEntry.place(x = 480, y = 223, width = 300, height = 46)

        CTkButton(
            add_patient_card,
            fg_color = Colors.Mandarin,
            corner_radius = 18,
            text = "Ajouter",
            font = font(25),
            hover_color = Colors.Sepia,
            command = lambda: self.logic(),
        ).place(width = 255, height = 67, x = 290, y = 400)


    def logic(self):
        
        def dateofBirthcheck(Bday):
            try:
                if Bday:
                    return datetime.strptime(Bday, "%d/%m/%Y")
                else:
                    return None
            except:
                return "problem"

        self.firstName  =  self.firstNameEntry.get()
        self.lastName  =  self.lastNameEntry.get()
        self.dateOfBirth  =  dateofBirthcheck(self.dateOfBirthEntry.get())
        self.genre  =  self.gender_entry.get() if self.gender_entry.get() in ["Fille", "Garçon"] else None
        self.maladiesChroniques  =  (self.maladiesChroniquesEntry.get() if self.maladiesChroniquesEntry.get() else None)
        self.phoneNumber  =  self.phoneNumberEntry.get() if self.phoneNumberEntry.get() else None
        self.keywords  =  self.keywordsEntry.get() if self.keywordsEntry.get() else None

        if not self.firstName and not self.lastName and not self.dateOfBirth and not self.genre and not self.maladiesChroniques and not self.phoneNumber and not self.keywords:
            return

        if self.firstName and self.lastName and self.dateOfBirth!= "problem" and self.dateOfBirth and self.genre:
            self.window.curr.execute("""SELECT id FROM patients WHERE firstName = ? AND lastName = ?""", (self.firstName, self.lastName,))
            id  =  self.window.curr.fetchone()
            if id:
                self.verification(" ".join([self.firstName, self.lastName]), id[0])
            else:
                self.add_patient()
        else:
            self.AlertLabel  =  CTkLabel(self, text = "Veuillez entrer toute les informations requise correctement" if self.dateOfBirth!= "problem" else "Veuillez entrer la date dans le bon format ex: 15/11/2006", font = font(20), fg_color = Colors.Danger, text_color = Colors.White, height = 45)
            self.AlertLabel.place(x = 0,y = 637, relwidth = 1)


    def verification(self, patientname, patientid):
        
        if self.verif:
            self.verif.focus()
        else:
            self.verif  =  confirm(patientname, patientid, self)
            self.verif.protocol("WM_DELETE_WINDOW", self.verif.close)
        


    def add_patient(self):
        
        self.window.curr.execute(
            """INSERT INTO "patients" (firstName, lastName, dateOfBirth, gender, phoneNumber, keywords, maladiesChroniques) VALUES (?,?,?,?,?,?,?)"""
            "",
            (
                self.firstName,
                self.lastName,
                self.dateOfBirth.strftime("%d/%m/%Y"),
                self.genre,
                self.phoneNumber,
                self.keywords,
                self.maladiesChroniques,
            ),
        )  
        
        self.window.conn.commit()

        pateintid  =  self.window.curr.execute("""SELECT id FROM patients""").fetchall()[-1][0]
        
        PatientsList(self.master).place(x = 0, y = 0, width = 400, height = 682)

        self.firstNameEntry.delete(0, END)
        self.lastNameEntry.delete(0, END)
        self.dateOfBirthEntry.delete(0, END)
        if self.phoneNumberEntry.get():
            self.phoneNumberEntry.delete(0, END)

        if self.keywordsEntry.get():
            self.keywordsEntry.delete(0, END)

        if self.maladiesChroniquesEntry.get():
            self.maladiesChroniquesEntry.delete(0, END)


        self.AlertLabel  =  CTkLabel(self, text = "Patient ajouté avec succes!", font = font(20), fg_color = Colors.Success, text_color = Colors.White, height = 45)
        self.AlertLabel.place(x = 0,y = 637, relwidth = 1)


        CTkButton(self.AlertLabel, fg_color = Colors.Success, corner_radius = 10, text = "Acceder" , font = font(20), hover_color = "#0F5132",
        command = lambda: PatientInfos(self.master, int(pateintid)).place(x = 400, y = 0, width = 879, height = 681)
        ).place(width = 100, height = 35, x = 770, y = 5)



class PatientsList(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius = 0, fg_color = Colors.Cadet)

        self.master  =  master
        self.window  =  master.window
        self.currentPage  =  0
        self.SelectedPatient  =  None

        self.view()

    def view(self):
        header  =  CTkFrame(self, fg_color = Colors.Mandarin, corner_radius = 0, height = 75)
        header.pack(fill = "x")

        CTkLabel(
            header, text = "Liste des patients", font = font(28), text_color = Colors.White
        ).place(x = 25, y = 20)

        CTkButton(
            header,
            fg_color = Colors.Mandarin,
            hover_color = Colors.Sepia,
            corner_radius = 0,
            width = 75,
            height = 74,
            text = "",
            image = CTkImage(
                light_image = Image.open("assets/imgs/add patient icon.png"),
                size = (50, 50),
            ),
            command = lambda: [self.load(), AddPatient(self.master).place(x = 400, y = 0, width = 880, height = 680)]
        ).place(x = 326)

        self.searchPatient  =  CTkEntry(
            self,
            placeholder_text = "Rechercher un patient...",
            height = 25,
            font = font(15),
            text_color = Colors.Cadet,
            fg_color = Colors.White,
            border_width = 0,
            corner_radius = 0,
        )
        self.searchPatient.pack(fill = "x")

        self.patientsFrame  =  CTkFrame(self, fg_color = Colors.Cadet)
        self.patientsFrame.pack(fill = "both", expand = True)

        self.load()

        

        self.searchPatient.bind("<Key>", lambda _: self.load())
        self.searchPatient.bind("<Return>", lambda _: self.load())


    def patient_infos(self, patientid):
        PatientInfos(self.master, patientid).place(
                        x = 400, y = 0, width = 879, height = 681
                    ),

    def load(self):
        clear(self.patientsFrame)

        patients  =  self.master.master.window.curr.execute(
            """SELECT id, firstName, lastName, dateOfBirth FROM "patients" """
        ).fetchall()

        pages  =  []

        search  =  self.searchPatient.get().lower()
        if not patients:
            CTkLabel(self, text = "Aucun patient", text_color = Colors.White, font = font(24)).place(relx = 0.5, rely = 0.5, anchor = CENTER)
            return

        for id, firstName, lastName, dateOfBirth in patients:
            if not pages or len(pages[-1]) == 4:
                pages.append([])
            
            if search: 
                if search in " ".join([firstName.lower(), lastName.lower()]) or search in dateOfBirth:   
                    pages[-1].append((id, firstName, lastName, dateOfBirth))
            else:
                pages[-1].append((id, firstName, lastName, dateOfBirth))

        self.patientsButtons  =  {}

        for id, firstName, lastName, dateOfBirth in pages[self.currentPage]:
            patientCard  =  CTkFrame(
                self.patientsFrame,
                width = 350,
                height = 100,
                corner_radius = 20,
                fg_color = Colors.Coral,
            )
            patientCard.pack(pady = 15)

            patientButton  =  CTkButton(
                patientCard,
                text = f"{firstName.capitalize()} {lastName.capitalize()}",
                font = font(30),
                corner_radius = 15,
                height = 41,
                width = 35 * len([firstName, lastName]),
                hover_color = Colors.Cadet,
                text_color = Colors.Mandarin,
                fg_color = Colors.Coral,
                command = lambda: None,
            )
            patientButton.place(x = 5, y = 10)

            self.patientsButtons[patientButton]  =  id

            def button(event):
                for btn in self.patientsButtons:
                    if str(btn) in str(event.widget):
                        return btn, self.patientsButtons[btn]

            patientButton.bind(
                "<Button-1>",
                lambda event: [
                    self.select(button(event)[0]),
                    self.patient_infos(button(event)[1])
                ],
            )

            CTkLabel(
                patientCard,
                text = f"Date de naissance: {dateOfBirth} ",
                font = font(20),
                text_color = Colors.White,
            ).place(x = 21, y = 59)

        CTkButton(
            self.patientsFrame,
            text = "<",
            font = font(25),
            height = 40,
            width = 40,
            fg_color = Colors.Mandarin if self.currentPage else Colors.Silver,
            corner_radius = 20,
            hover_color = Colors.Sepia if self.currentPage else Colors.Silver,
            command = lambda: self.update(-1 if self.currentPage else 0),
        ).place(x = 104, y = 522)

        CTkLabel(
            self.patientsFrame,
            text = self.currentPage + 1,
            font = font(30),
            text_color = Colors.White,
        ).place(x = 190, y = 523)

        CTkButton(
            self.patientsFrame,
            text = ">",
            font = font(25),
            height = 40,
            width = 40,
            fg_color = Colors.Mandarin if self.currentPage < len(pages) - 1 else Colors.Silver,
            corner_radius = 20,
            hover_color = Colors.Sepia if self.currentPage < len(pages) - 1 else Colors.Silver,
            command = lambda: self.update(+1 if self.currentPage < len(pages) - 1 else 0),
        ).place(x = 238, y = 522)

    def select(self, button):
        for patientButton in self.patientsButtons:
            patientButton.configure(fg_color = Colors.Coral, text_color = Colors.Mandarin, hover = True)
        button.configure(fg_color = Colors.Mandarin, text_color = Colors.Cadet, hover = False)
        self.SelectedPatient = self.patientsButtons[button]

    def update(self, num):
        if num:
            self.currentPage +=  num
            self.load()
        if self.SelectedPatient:
            for patientButton in self.patientsButtons:
                if self.SelectedPatient == self.patientsButtons[patientButton]:
                    self.select(patientButton)


class PatientInfos(CTkFrame):
    def __init__(self, master: CTkFrame, patientId):
        super().__init__(master, corner_radius = 0, fg_color = Colors.Coral)

        self.master = master
        self.window = master.window
        self.patientId  =  patientId
        self.editpatient  =  None

        self.view()


    def view(self):

        id, self.firstName, self.lastName, self.dateOfBirth, self.gender, self.phoneNumber, self.keywords, self.maladiesChroniques, self.dateOfCreation  =  self.window.curr.execute("""SELECT * FROM patients WHERE id  =  ?""", (self.patientId,)).fetchone()
        hwList  =  self.window.curr.execute("""SELECT height, weight FROM "visits" WHERE patientId  =  ?""", (int(self.patientId),)).fetchall()
        if hwList:
            self.height, self.weight  =  hwList[-1]
        else:
            self.height, self.weight = None, None

        if not self.keywords:
            self.keywords = None

        CTkLabel(
            self,
            text = f"Informations de patients",
            font = font(45),
            fg_color = Colors.Liver,
            corner_radius = 20,
            width = 570,
            height = 75,
            text_color = Colors.White,
        ).pack(pady = 15)

        self.patientInfoCard  =  CTkFrame(
            self, width = 393, height = 560, fg_color = Colors.Cadet, corner_radius = 20
        )
        self.patientInfoCard.place(x = 20, y = 106)

        infoLabel  =  lambda text, y: CTkLabel(
            self.patientInfoCard, font = font(15), text = text, text_color = Colors.White
        ).place(x = 20, y = y)

        infoLabel(f"Nom: {self.lastName.capitalize()}", 30)
        infoLabel(f"Prénom: {self.firstName.capitalize()} ", 74)
        infoLabel(f"Date de naissance: {self.dateOfBirth}", 118)
        infoLabel(f"Genre: {self.gender.capitalize()}", 162)
        infoLabel(f"Age : {calculateAge(self.dateOfBirth)}", 206)
        infoLabel(f"Poids recent: {str(self.weight)+'kg' if self.weight else 'Non spécifié'}", 250)
        infoLabel(f"Taille recente: {str(self.height)+'cm' if self.height else 'Non spécifié'}", 294)
        infoLabel(f"IMC recent: {round(self.weight/(self.height/100)**2, 1) if self.weight else 'Non spécifié'}", 338)
        infoLabel(
            f"Numero de téléphone: {self.phoneNumber if self.phoneNumber else 'Non spécifié'} ",
            382,
        )
        infoLabel(f"Maladies Chroniques: {self.maladiesChroniques if self.maladiesChroniques else 'Non spécifié'}", 426)
        infoLabel(
            f"Mots clés: {self.keywords if self.keywords else 'Non spécifié'} ",
            470,
        )

        CTkButton(
            self.patientInfoCard,
            text = "Modifier",
            width = 240,
            height = 42,
            fg_color = Colors.Mandarin,
            corner_radius = 16,
            hover_color = Colors.Sepia,
            font = font(20),
            text_color = Colors.White,
            command = self.editview
        ).place(relx = 0.5, y = 530, anchor = CENTER)

        CTkButton(
            self,
            text = "Historique des visites",
            font = font(26),
            fg_color = Colors.Cadet,
            width = 380,
            height = 72,
            corner_radius = 20,
            hover_color = "#10162b",
            text_color = Colors.Mandarin,
            command = lambda: visits.VisitsPage(self.master, self.patientId, True)
        ).place(x = 433, y = 494)

        CTkButton(
            self,
            text = "Ajouter une visite",
            font = font(20),
            fg_color = Colors.Mandarin,
            corner_radius = 20,
            hover_color = Colors.Sepia,
            text_color = Colors.White,
            command = lambda:visits.VisitsPage(self.master.master, self.patientId).place(x = 0, y = 150, width = 1280, height = 682)
        ).place(x = 650, y = 585, height = 72, width = 200)

        CTkButton(
            self,
            text = "Supprimer ce patient",
            font = font(16),
            fg_color = Colors.Danger,
            corner_radius = 20,
            hover_color = "#8b0000",
            text_color = Colors.White,
            command = lambda: self.deletepatient()
            ).place(x = 430, y = 585, height = 72, width = 200)



        courbeDeCroissance  =  CTkFrame(
            self, width = 375, height = 370, corner_radius = 20, fg_color = Colors.Cadet
        )
        courbeDeCroissance.place(x = 433, y = 109, width = 375, height = 370)

        CTkButton(
            courbeDeCroissance,
            text = "Courbes de croissance",
            fg_color = Colors.Cadet,
            text_color = Colors.White,
            height = 55,
            width = 375,
            corner_radius = 10,
            font = font(28),
            hover_color = Colors.Mandarin,
            bg_color = Colors.Coral,
        ).place(x = 0, y = 0)

        CTkFrame(
            courbeDeCroissance, height = 10, fg_color = Colors.Cadet, corner_radius = 0
        ).place(x = 0, y = 45, relwidth = 1)

        img  =  CTkImage(
            light_image = Image.open("assets/imgs/courbe de croissance.png"),
            size = (380, 305),
        )

        CTkLabel(courbeDeCroissance, image = img).place(x = 0, y = 43)


    def editview(self):
        def close():
            self.editpatient.destroy()
            self.editpatient = None

        if self.editpatient:
            self.editpatient.focus()
        else:
            self.editpatient  =  CTkToplevel(fg_color = Colors.Cadet)
            self.editpatient.protocol("WM_DELETE_WINDOW", lambda: close())
            self.editpatient.resizable(False, False)
            self.editpatient.title("Modifier le patient")
            center(400, 460, self.editpatient)

            CTkLabel(
                self.editpatient,
                text = "Modifier le patient",
                fg_color = Colors.Liver,
                text_color = Colors.White,
                font = font(22),
                corner_radius = 15,
            ).place(x = 82, y = 16, height = 51, width = 246)

            CTkLabel(self.editpatient, text = "Nom:", text_color = Colors.White, font = font(17)).place(x = 160, y = 90)
            CTkLabel(self.editpatient, text = "Prénom:", text_color = Colors.White, font = font(17)).place(x = 132, y = 134)
            CTkLabel(self.editpatient, text = "Date de naissance:", text_color = Colors.White, font = font(17)).place(x = 45, y = 178)
            CTkLabel(self.editpatient, text = "Genre:", text_color = Colors.White, font = font(17)).place(x = 147, y = 222)
            CTkLabel(self.editpatient, text = "Numero de téléphone:", text_color = Colors.White, font = font(17)).place(x = 20, y = 265)
            CTkLabel(self.editpatient, text = "Maladies chroniques:", text_color = Colors.White, font = font(17)).place(x = 25, y = 310)
            CTkLabel(self.editpatient, text = "mots clés:", text_color = Colors.White, font = font(17)).place(x = 117, y = 350)


            self.firstnameEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,
            )
            self.firstnameEntry.place(x = 215, y = 91, width = 140, height = 26)
            self.firstnameEntry.insert(0, self.firstName)
            

            self.lastNameEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,
            )
            self.lastNameEntry.place(x = 215, y = 134, width = 140, height = 26)
            self.lastNameEntry.insert(0, self.lastName)


            self.dateOfbirthEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,
            )
            self.dateOfbirthEntry.place(x = 215, y = 179, width = 140, height = 26)
            self.dateOfbirthEntry.insert(0, self.dateOfBirth)


            self.gender_entry  =  CTkComboBox(
                self.editpatient,
                values =  ["Genre", "garçon", "fille"],
                font = font(15),
                text_color = Colors.Cadet,
                dropdown_fg_color = Colors.Liver,
                corner_radius = 10,
                fg_color = Colors.White,
                dropdown_font = font(15),
                command = lambda event: check()
            )
            self.gender_entry.place(x = 215, y = 222, width = 140, height = 26)
            self.gender_entry.set(self.gender)


            self.phonenumberEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,

            )
            self.phonenumberEntry.place(x = 215, y = 265, width = 140, height = 26)
            if self.phoneNumber:
                self.phonenumberEntry.insert(0, self.phoneNumber)
            
            self.maladiesChroniquesEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,

            )
            self.maladiesChroniquesEntry.place(x = 215, y = 310, width = 140, height = 26)
            if self.maladiesChroniques:
                self.maladiesChroniquesEntry.insert(0, self.maladiesChroniques)
            

            self.keywordsEntry  =  CTkEntry(
                self.editpatient,
                fg_color = Colors.White,
                corner_radius = 10,
                placeholder_text = "",
                text_color = Colors.Cadet,
            )
            self.keywordsEntry.place(x = 215, y = 350, width = 140, height = 26)
            if self.keywords:
                self.keywordsEntry.insert(0, self.keywords)


            self.confirm  =  CTkButton(self.editpatient, text = "Sauvegarder", text_color = Colors.White, fg_color = Colors.Silver, hover_color = Colors.Sepia, state = False, font = font(16), command = lambda: self.edit())
            self.confirm.place(x = 193, y = 400, width = 150, height = 42)

            self.cancel  =  CTkButton(self.editpatient, text = "Annuler", fg_color = Colors.Silver, font = font(16), hover_color = Colors.Mandarin, command = close)
            self.cancel.place(x = 34, y = 400, width = 120, height = 42)


            self.firstnameEntry.bind("<KeyRelease>", lambda event:check())
            self.lastNameEntry.bind("<KeyRelease>", lambda event:check())
            self.dateOfbirthEntry.bind("<KeyRelease>", lambda event: check())
            self.phonenumberEntry.bind("<KeyRelease>", lambda event:check())
            self.maladiesChroniquesEntry.bind("<KeyRelease>", lambda event:check())
            self.keywordsEntry.bind("<KeyRelease>", lambda event:check())
            
            def check():

                keywords = self.keywordsEntry.get() if self.keywordsEntry.get() else None
                phoneNumber = self.phonenumberEntry.get() if self.phonenumberEntry.get() else None
                maladieschroniques = self.maladiesChroniquesEntry.get() if self.maladiesChroniquesEntry.get() else None

                checks = {
                    self.firstnameEntry.get() : str(self.firstName),
                    self.lastNameEntry.get(): str(self.lastName),
                    self.dateOfbirthEntry.get() : str(self.dateOfBirth),
                    self.gender_entry.get() : str(self.gender),
                    phoneNumber : str(self.phoneNumber),
                    keywords : self.keywords,
                    maladieschroniques: str(self.maladiesChroniques),
                    }
                
                changed = any(i!=checks[i] for i in checks)

                if  changed:
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

            new_first_name  =  self.firstnameEntry.get()
            new_last_name  =  self.lastNameEntry.get()
            new_date_of_birth  =  dateofBirthcheck(self.dateOfbirthEntry.get())
            new_gender  =  self.gender_entry.get() if self.gender_entry.get() in ["Fille", "Garçon", "fille", "garcon", "garçon"] else None
            new_phone_number  =  self.phonenumberEntry.get() if self.phonenumberEntry.get() else None
            new_maladieschroniques = self.maladiesChroniquesEntry.get() if self.maladiesChroniquesEntry.get() else None
            new_keywords  =  self.keywordsEntry.get() if self.keywordsEntry.get() else None

            new_infos = [new_first_name,
                        new_last_name,
                        new_date_of_birth,
                        new_gender, 
                        new_phone_number,
                        new_maladieschroniques,
                        new_keywords
                        ]
            print(new_infos)
            if any(not info or info=="problem" for info in new_infos[:4]):
                verification = False
            else:
                verification = True

            if verification:
                self.window.curr.execute("""UPDATE "patients" SET 
                firstName = ?, 
                lastName = ?, 
                dateOfBirth = ?, 
                gender = ?, 
                phoneNumber = ?, 
                maladiesChroniques = ?,
                keywords = ?
                WHERE id = ?""",
                (new_first_name, new_last_name, new_date_of_birth.strftime("%d/%m/%Y"), new_gender, new_phone_number, new_maladieschroniques, new_keywords, self.patientId))

                self.window.conn.commit()

                self.editpatient.destroy()

                PatientInfos(self.master, self.patientId).place(x = 400, y = 0, width = 879, height = 681)
            else:
                self.AlertLabel  =  CTkLabel(
                    self.editpatient, 
                    text = "Veuillez entrer toute les informations requise correctement" if self.dateOfBirth!= "problem" else "Veuillez entrer la dade dans le bon format ex: 15/11/2006", 
                    font = font(20), 
                    fg_color = Colors.Danger, 
                    text_color = Colors.White, 
                    height = 45
                    )
                
                self.AlertLabel.place(x= 0, y= 483, relwidth= 1)

            
    def deletepatient(self):

        
        self.toplevel  =  CTkToplevel(fg_color = Colors.Coral)
        self.toplevel.resizable(False, False)
        center(574, 245, self.toplevel)

        def close():
            self.toplevel.destroy()

        def delete():
            self.window.curr.execute("""DELETE FROM patients WHERE id = ?""", (self.patientId,))
            close()
            self.window.conn.commit()
            AddPatient(self.master).place(x = 400, y = 0, width = 880, height = 682)
            PatientsList(self.master).place(x = 0, y = 0, width = 400, height = 682)

        CTkLabel(self.toplevel, text = "Supprimer le patient", fg_color = Colors.Liver, font = font(25), text_color = Colors.White, corner_radius = 15).place(x = 124, y = 34, width = 320, height = 70)
        CTkLabel(self.toplevel, text = f"Étes vous sure de vouloir supprimer le patient :", font = font(16), text_color = Colors.White).place(relx = 0.5, rely = 0.51, anchor = CENTER)
        CTkLabel(self.toplevel, text = f"{self.firstName} {self.lastName}", font = font(16), text_color = Colors.Mandarin).place(relx = 0.5, rely = 0.6, anchor = CENTER)

        CTkButton(self.toplevel, text = "Supprimer", fg_color = Colors.Danger, text_color = Colors.White, hover_color = Colors.Danger_hover, command = delete, font = font(15)).place(x = 308, y = 178, width = 130, height = 50)
        CTkButton(self.toplevel, text = "Annuler", fg_color = Colors.Silver, text_color = Colors.White, hover_color = Colors.Mandarin, command = close, font = font(15)).place(x = 140, y = 178, width = 130, height = 50)

        


class PatientsPage(CTkFrame):
    def __init__(self, master: CTkFrame) -> None:
        clear(master)
        super().__init__(master, corner_radius = 0, fg_color = Colors.Coral)
        self.pack(fill = "both", expand = True)

        self.window  =  master.window
        self.master  =  master

        self.window  =  master.window

        self.view()

    def view(self):
        PatientsList(self).place(x = 0, y = 0, width = 400, height = 682)
        AddPatient(self).place(x = 400, y = 0, width = 880, height = 682)
