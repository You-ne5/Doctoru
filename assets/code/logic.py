from datetime import datetime

def strToDatetime(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")