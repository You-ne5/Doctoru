from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font
from PIL import Image
from assets.code.logic import calculateAge, strToDatetime

class AddPatient(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)

        self.master = master
        self.window = master.window
        self.view()

    def view(self):
        title = CTkLabel(
            self,
            text="Ajouter un patient",
            font=font(45),
            fg_color=Colors.Liver,
            text_color=Colors.White,
            corner_radius=20,
            height=75,
            width=430,
        )
        title.pack(pady=15)

        addPatientCard = CTkFrame(self, corner_radius=20, fg_color=Colors.Cadet)
        addPatientCard.place(x=21, y=120, width=839, height=496)

        self.lastNameEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Nom",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.lastNameEntry.place(x=50, y=34, width=300, height=46)

        self.firstNameEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Prénom",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.firstNameEntry.place(x=50, y=129, width=300, height=46)

        self.dateOfBirthEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Date de naissance",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.dateOfBirthEntry.place(x=50, y=220, width=300, height=46)


        self.GenderEntry = CTkComboBox(
            addPatientCard,
            values= ["Genre", "Garçon", "Fille"],
            font=font(20),
            justify=CENTER,
            text_color=Colors.Cadet,
            dropdown_fg_color=Colors.Liver,
            corner_radius=14,
            fg_color=Colors.White,
            width=300,
            height=46,
            dropdown_font=font(20)
        )
        self.GenderEntry.place(x=51, y=313)


        self.maladiesChroniquesEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Maladies Chroniques",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.maladiesChroniquesEntry.place(x=480, y=34, width=300, height=46)

        self.phoneNumberEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Téléphone (optionnel)",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.phoneNumberEntry.place(x=480, y=126, width=300, height=46)

        self.keywordsEntry = CTkEntry(
            addPatientCard,
            placeholder_text="Mots clés(optionel)",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.keywordsEntry.place(x=480, y=223, width=300, height=46)

        CTkButton(
            addPatientCard,
            fg_color=Colors.Mandarin,
            corner_radius=18,
            text="Ajouter",
            font=font(25),
            hover_color=Colors.Sepia,
            command=lambda: self.logic(),
        ).place(width=255, height=67, x=290, y=400)


    def logic(self):
        def dateofBirthcheck(Bday):
            try:
                return datetime.strptime(Bday, "%d/%m/%Y")
            except:
                return None

        firstName = self.firstNameEntry.get()
        lastName = self.lastNameEntry.get()
        dateOfBirth = dateofBirthcheck(self.dateOfBirthEntry.get())
        genre = self.GenderEntry.get() if self.GenderEntry.get() in ["Fille", "Garçon"] else None
        maladiesChroniques = (self.maladiesChroniquesEntry.get() if self.maladiesChroniquesEntry.get() else None)
        phoneNumber = self.phoneNumberEntry.get() if self.phoneNumberEntry.get() else None
        keywords = self.keywordsEntry.get() if self.keywordsEntry.get() else None

        try:
            self.AlertLabel.destroy()
        except:
            pass

        if firstName and lastName and dateOfBirth and genre:
            self.window.curr.execute(
                """INSERT INTO "patients" (firstName, lastName, dateOfBirth, gender, phoneNumber, keywords, maladiesChroniques) VALUES (?,?,?,?,?,?,?)"""
                "",
                (
                    firstName,
                    lastName,
                    dateOfBirth.strftime("%d/%m/%Y"),
                    genre,
                    phoneNumber,
                    keywords,
                    maladiesChroniques,
                ),
            )
            self.window.conn.commit()

            self.AlertLabel = CTkLabel(self, text="Patient ajouté avec succes", font=font(25), fg_color=Colors.Success, text_color=Colors.White, height=45)
            self.AlertLabel.place(x=0,y=637)

        else:
            self.AlertLabel = CTkLabel(self, text="Veuillez entrer toute les informations requise correctement", font=font(25), fg_color=Colors.Danger, text_color=Colors.White, height=45)
            self.AlertLabel.place(x=0,y=637, relwidth=1)


class PatientsList(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.master = master
        self.window = master.window
        self.currentPage = 0
        self.SelectedPatient = None

        self.view()

    def view(self):
        header = CTkFrame(self, fg_color=Colors.Mandarin, corner_radius=0, height=75)
        header.pack(fill="x")

        CTkLabel(
            header, text="Liste des patients", font=font(28), text_color=Colors.White
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
                light_image=Image.open("assets/imgs/add patient icon.png"),
                size=(50, 50),
            ),
            command=lambda: [self.load(), AddPatient(self.master).place(x=400, y=0, width=880, height=680)]
        ).place(x=326)

        self.searchPatient = CTkEntry(
            self,
            placeholder_text="Rechercher un patient...",
            height=25,
            font=font(15),
            text_color=Colors.Cadet,
            fg_color=Colors.White,
            border_width=0,
            corner_radius=0,
        )
        self.searchPatient.pack(fill="x")

        self.patientsFrame = CTkFrame(self, fg_color=Colors.Cadet)
        self.patientsFrame.pack(fill="both", expand=True)

        self.load()

        for widget in self.master.window.winfo_children():
            widget.bind("<Button-1>", lambda _: self.focus())

        self.searchPatient.bind("<Key>", lambda _: self.load())

    def load(self):
        clear(self.patientsFrame)

        patients = self.master.master.window.curr.execute(
            """SELECT id, firstName, lastName, dateOfBirth FROM "patients" """
        ).fetchall()

        pages = []

        search = self.searchPatient.get().lower()

        for id, firstName, lastName, dateOfBirth in patients:
            if not pages or len(pages[-1]) == 4:
                pages.append([])
            
            if search: 
                if search in " ".join([firstName.lower(), lastName.lower()]) or search in dateOfBirth:   
                    pages[-1].append((id, firstName, lastName, dateOfBirth))
            else:
                pages[-1].append((id, firstName, lastName, dateOfBirth))

        self.patientsButtons = {}

        for id, firstName, lastName, dateOfBirth in pages[self.currentPage]:
            patientCard = CTkFrame(
                self.patientsFrame,
                width=350,
                height=100,
                corner_radius=20,
                fg_color=Colors.Coral,
            )
            patientCard.pack(pady=15)

            patientButton = CTkButton(
                patientCard,
                text=f"{firstName.capitalize()} {lastName.capitalize()}",
                font=font(30),
                corner_radius=15,
                height=41,
                width=35 * len([firstName, lastName]),
                hover_color=Colors.Cadet,
                text_color=Colors.Mandarin,
                fg_color=Colors.Coral,
                command=lambda: None,
            )
            patientButton.place(x=5, y=10)

            self.patientsButtons[patientButton] = id

            def button(event):
                for btn in self.patientsButtons:
                    if str(btn) in str(event.widget):
                        return btn, self.patientsButtons[btn]

            patientButton.bind(
                "<Button-1>",
                lambda event: [
                    self.select(button(event)[0]),
                    PatientInfos(self.master, button(event)[1]).place(
                        x=400, y=0, width=879, height=681
                    ),
                ],
            )

            CTkLabel(
                patientCard,
                text=f"Date de naissance: {dateOfBirth} ",
                font=font(20),
                text_color=Colors.White,
            ).place(x=21, y=59)

        CTkButton(
            self.patientsFrame,
            text="<",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.currentPage else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.currentPage else Colors.Silver,
            command=lambda: self.update(-1 if self.currentPage else 0),
        ).place(x=104, y=522)

        CTkLabel(
            self.patientsFrame,
            text=self.currentPage + 1,
            font=font(30),
            text_color=Colors.White,
        ).place(x=190, y=523)

        CTkButton(
            self.patientsFrame,
            text=">",
            font=font(25),
            height=40,
            width=40,
            fg_color=Colors.Mandarin if self.currentPage < len(pages) - 1 else Colors.Silver,
            corner_radius=20,
            hover_color=Colors.Sepia if self.currentPage < len(pages) - 1 else Colors.Silver,
            command=lambda: self.update(+1 if self.currentPage < len(pages) - 1 else 0),
        ).place(x=238, y=522)

    def select(self, button):
        for patientButton in self.patientsButtons:
            patientButton.configure(fg_color=Colors.Coral, text_color=Colors.Mandarin, hover=True)
        button.configure(fg_color=Colors.Mandarin, text_color=Colors.Cadet, hover=False)
        self.SelectedPatient = self.patientsButtons[button]

    def update(self, num):
        if num:
            self.currentPage += num
            self.load()
        if self.SelectedPatient:
            for patientButton in self.patientsButtons:
                if self.SelectedPatient == self.patientsButtons[patientButton]:
                    self.select(patientButton)


class PatientInfos(CTkFrame):
    def __init__(self, master: CTkFrame, patientId):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)

        self.master = master
        self.window = master.window
        self.patientId = patientId

        self.view()

    def view(self):

        id, firstName, lastName, dateOfBirth, gender, phoneNumber, keywords, maladiesChroniques = self.window.curr.execute("""SELECT * FROM patients WHERE id = ?""", (self.patientId,)).fetchone()

        CTkLabel(
            self,
            text=f"Informations de patients",
            font=font(45),
            fg_color=Colors.Liver,
            corner_radius=20,
            width=570,
            height=75,
            text_color=Colors.White,
        ).pack(pady=15)

        patientInfoCard = CTkFrame(
            self, width=393, height=560, fg_color=Colors.Cadet, corner_radius=20
        )
        patientInfoCard.place(x=20, y=106)

        infoLabel = lambda text, y: CTkLabel(
            patientInfoCard, font=font(20), text=text, text_color=Colors.White
        ).place(x=20, y=y)

        infoLabel(f"Nom: {lastName.capitalize()}", 30)
        infoLabel(f"Prénom: {firstName.capitalize()} ", 74)
        infoLabel(f"Date de naissance: {dateOfBirth}", 118)
        infoLabel(f"Genre: {gender.capitalize()}", 162)
        infoLabel(f"Age : {calculateAge(dateOfBirth)}", 206)
        infoLabel(f"Poids recent: 80kg", 250)
        infoLabel(f"Taille recente: 1m80", 294)
        infoLabel(f"IMC recent: 24.9", 338)
        infoLabel(
            f"Numero de téléphone: {phoneNumber if phoneNumber else 'Non spécifié'} ",
            382,
        )
        infoLabel(f"Derniere visite: 20/7/2021 ", 426)
        infoLabel(
            f"Mots clés: {keywords if keywords else 'Non spécifié'} ",
            470,
        )

        CTkButton(
            patientInfoCard,
            text="Modifier",
            width=240,
            height=42,
            fg_color=Colors.Mandarin,
            corner_radius=16,
            hover_color=Colors.Sepia,
            font=font(20),
            text_color=Colors.White,
        ).place(relx=0.5, y=530, anchor=CENTER)

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

        courbeDeCroissance = CTkFrame(
            self, width=375, height=370, corner_radius=20, fg_color=Colors.Cadet
        )
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

        CTkFrame(
            courbeDeCroissance, height=10, fg_color=Colors.Cadet, corner_radius=0
        ).place(x=0, y=45, relwidth=1)

        img = CTkImage(
            light_image=Image.open("assets/imgs/courbe de croissance.png"),
            size=(380, 305),
        )

        CTkLabel(courbeDeCroissance, image=img).place(x=0, y=43)


class PatientsPage(CTkFrame):
    def __init__(self, master: CTkFrame) -> None:
        clear(master)
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = master.window
        self.master = master

        self.window = master.window

        self.view()

    def view(self):
        PatientsList(self).place(x=0, y=0, width=400, height=682)
        AddPatient(self).place(x=400, y=0, width=880, height=682)
