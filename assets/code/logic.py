from datetime import datetime
from math import floor


def calculateAge(Bday):
    bday = datetime.strptime(Bday, "%d/%m/%Y")
    age = (datetime.now() - bday).days/365.25
    

    suffix = f"{'ans' if age >= 2 else 'mois'}"

    if age < 2:
        age *= 12

    return f"{floor(age)} {suffix}"


def strToDatetime(text: str) -> datetime:
    return datetime.strptime(text, "%d/%m/%Y %H:%M")