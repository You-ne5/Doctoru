from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font
from src.app import navbar
from PIL import Image
from src.app.logic import calculateAge, wait
import asyncio

class AddPatient(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.master = master
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

        add_patient_card = CTkFrame(self, corner_radius=20, fg_color=Colors.Cadet)
        add_patient_card.place(x=21, y=120, width=839, height=496)

        self.firstName = CTkEntry(
            add_patient_card,
            placeholder_text="Nom",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.firstName.place(x=50, y=34, width=300, height=46)

        self.lastName = CTkEntry(
            add_patient_card,
            placeholder_text="Prénom",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.lastName.place(x=50, y=129, width=300, height=46)

        self.dateOfBirth = CTkEntry(
            add_patient_card,
            placeholder_text="Date de naissance",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.dateOfBirth.place(x=50, y=220, width=300, height=46)


        self.Genre = CTkComboBox(
            add_patient_card,
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
        self.Genre.place(x=51, y=313)


        self.maladie_chronique = CTkEntry(
            add_patient_card,
            placeholder_text="Maladies Chroniques",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.maladie_chronique.place(x=480, y=34, width=300, height=46)

        self.phoneNumber = CTkEntry(
            add_patient_card,
            placeholder_text="Téléphone (optionnel)",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.phoneNumber.place(x=480, y=126, width=300, height=46)

        self.keywords = CTkEntry(
            add_patient_card,
            placeholder_text="Mots clés(optionel)",
            justify=CENTER,
            font=font(23),
            placeholder_text_color=Colors.Silver,
            text_color=Colors.Cadet,
            corner_radius=14,
            fg_color=Colors.White,
        )
        self.keywords.place(x=480, y=223, width=300, height=46)

        CTkButton(
            add_patient_card,
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

        firstName = self.firstName.get()
        lastName = self.lastName.get()
        dateOfBirth = dateofBirthcheck(self.dateOfBirth.get())
        genre = self.Genre.get() if self.Genre.get() in ["Fille", "Garçon"] else None
        maladieChronique = (self.maladie_chronique.get() if self.maladie_chronique.get() else None)
        phoneNumber = self.phoneNumber.get() if self.phoneNumber.get() else None
        keywords = self.keywords.get() if self.keywords.get() else None

        if firstName and lastName and dateOfBirth and genre:
            self.master.window.curr.execute(
                """INSERT INTO "patients" (firstName, lastName, dateOfBirth, gender, phoneNumber, keywords, maladieChronique) VALUES (?,?,?,?,?,?,?)"""
                "",
                (
                    firstName,
                    lastName,
                    dateOfBirth,
                    genre,
                    phoneNumber,
                    keywords,
                    maladieChronique,
                ),
            )
            self.master.window.conn.commit()

            self.successframe = CTkLabel(self, text="Patient Ajouté avec succes", font=font(25), fg_color=Colors.Success, text_color=Colors.White)
            self.successframe.place(x=0, y=640, width=880, height=45)

        else:
            self.errorframe = CTkLabel(self, text="Veuillez entrer toute les informations requise correctement", font=font(25), fg_color=Colors.Danger, text_color=Colors.White)
            self.errorframe.place(x=0, y=640, width=880, height=45)


            


class PatientsList(CTkFrame):
    def __init__(self, master: CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)

        self.master = master
        self.page = 0
        self.button = None
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
            command=lambda: AddPatient(self.master).place(
                x=400, y=0, width=880, height=680
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

    def select(self, button):
        for btn in self.btns:
            btn.configure(fg_color=Colors.Coral)
        button.configure(fg_color=Colors.Mandarin)
        self.button = button

    def load(self):
        clear(self.patientsframe)

        pages = []
        patients = self.master.master.window.curr.execute(
            """SELECT * FROM "patients" """
        ).fetchall()

        for patient in patients:
            if not pages or len(pages[-1]) == 4:
                pages.append([])
            pages[-1].append(patient)

        self.btns = {}

        for patientInfo in pages[self.page]:
            patientcard = CTkFrame(
                self.patientsframe,
                width=350,
                height=100,
                corner_radius=20,
                fg_color=Colors.Coral,
            )
            patientcard.pack(pady=15)

            patient_select = CTkButton(
                patientcard,
                text=" ".join([patientInfo[1], patientInfo[2]]),
                font=font(30),
                height=41,
                width=35 * len([patientInfo[1], patientInfo[2]]),
                hover_color=Colors.Mandarin,
                fg_color=Colors.Coral,
                command=lambda: None,
            )
            patient_select.place(x=17, y=11)

            self.btns[patient_select] = patientInfo

            def button(event):
                for btn in self.btns:

                    if str(btn) == "." + ".".join(str(event.widget).split(".")[1:-1]):
                        return btn, self.btns[btn]

            patient_select.bind(
                "<Button-1>",
                lambda event: [
                    self.select(button(event)[0]),
                    SelectedPageFrame(self.master, button(event)[1]).place(
                        x=399, y=0, width=879, height=681
                    ),
                ],
            )

            CTkLabel(
                patientcard,
                text=f"Date de naissance: {patientInfo[3]} ",
                font=font(20),
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
        if self.button:
            self.select(self.button)


class SelectedPageFrame(CTkFrame):
    def __init__(self, master: CTkFrame, patientInfo):
        self.patientInfo = patientInfo
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

        info = lambda text, y: CTkLabel(
            patientInfo, font=font(20), text=text, text_color=Colors.White
        ).place(x=20, y=y)
        not_specified = "Non spécifié"

        info(f"Nom: {self.patientInfo[1]}", 30)
        info(f"Prénom: {self.patientInfo[2]} ", 74)
        info(f"Date de naissance: {self.patientInfo[3]}", 118)
        info(f"Genre: {self.patientInfo[4]}", 162)
        info(f"Age : {calculateAge(self.patientInfo[3])}", 206)
        info(f"Poids recent: 80  ", 250)
        info(f"Taille recente: 1m80", 294)
        info(f"IMC recent: 24.9 ", 338)
        info(
            f"Numero de téléphone: {self.patientInfo[5] if self.patientInfo[5] else not_specified} ",
            382,
        )
        info(f"Derniere visite: 20/7/2021 ", 426)
        info(
            f"Mots clés: {self.patientInfo[6] if self.patientInfo[6] else not_specified} ",
            470,
        )

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
    def __init__(self, master: CTk) -> None:
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = master.window
        self.master = master
        
        self.view()

    def view(self):
        PatientsList(self).place(x=0, y=0, width=400, height=682)
        AddPatient(self).place(x=400, y=0, width=880, height=682)
