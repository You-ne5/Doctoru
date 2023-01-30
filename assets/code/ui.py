from customtkinter import CTkFont


class Colors:
    Mandarin = "#EF8354"
    Sepia = "#794412"
    Liver = "#644F4F"

    White = "#FFFFFF"
    Silver = "#BFC0C0"
    Coral = "#4F5D75"
    Cadet = "#2D3142"

    Success = "#198754"
    Warning = "#EED202"
    Danger = "#FF002D"
    Danger_hover = "#B3001F"

    Danger_hover = "#B3001F"
    ord_blue = "#0B3187"

def font(size: int) -> CTkFont:
    return CTkFont(family="Roboto", size=size, weight="bold")


def clear(frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()


def center(w, h, frame) -> None:
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    frame.geometry("%dx%d+%d+%d" % (w, h, x, y))
    clear(frame)
