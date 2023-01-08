from datetime import datetime
from math import floor


def calculateAge(Bday):
    bday = datetime.strptime(Bday, "%d/%m/%Y")

    return floor((datetime.now() - bday).days/365.25)

