from datetime import datetime
from customtkinter import *
from assets.code.ui import clear, Colors, font
from PIL import Image


class VisitBox(CTkFrame):
    def __init__(self, master:CTkFrame):
        super().__init__(master, corner_radius=0, fg_color=Colors.Cadet)
        self.view()

    def view(self):
        title = CTkLabel(self, text="Ajouter une visite", fg_color=Colors.Liver, corner_radius=20, font=font(30))
        title.place(x=85, y=30, height=76, width=430)

        inpt = lambda txt, y: CTkEntry(self, placeholder_text=txt, fg_color=Colors.White, text_color=Colors.Cadet, corner_radius=16, justify=CENTER, font=font(23)).place(x=151, y=y, height=45, width=300)

        inpt("Patient", 125)
        CTkButton(self, height=30, width=30, text="+", fg_color=Colors.Mandarin, text_color=Colors.White, corner_radius=15, font=font(20)).place(x=465, y=130)
        CTkEntry(self, placeholder_text= "Poids", fg_color=Colors.White, text_color=Colors.Cadet, corner_radius=16, justify=CENTER, font=font(23)).place(x=150, y=190, height=45, width=140)
        CTkEntry(self, placeholder_text="Taille", fg_color=Colors.White , text_color=Colors.Cadet, corner_radius=16, justify=CENTER, font=font(23)).place(x=310, y=190, height=45, width=140)
        inpt("Motif", 255)
        inpt("Conclusion", 320)
        inpt("Montant", 385)
        inpt("DEP", 450)

        CTkButton(self, fg_color=Colors.Mandarin, text="Ajouter", corner_radius=20, font=font(30), hover_color=Colors.Sepia).place(x=175, y=578, width=250, height=60)
    
        CTkCheckBox(self, text="Ordonnance", fg_color=Colors.Mandarin, hover_color=Colors.Sepia, font=font(25), width=25, height=25).place(x=152, y=520)
        




class VisitsPage(CTkFrame):
    def __init__(self, master: CTkFrame) -> None:
        clear(master)
        super().__init__(master, corner_radius=0, fg_color=Colors.Coral)
        self.pack(fill="both", expand=True)

        self.window = master.window
        self.master = master

        self.window = master.window

        self.view()

    def view(self):
        VisitBox(self).place(x=680, y=0, height=682, width=600)