class Colors:
    Mandarin = "#EF8354"
    Sepia = "#794412"
    Liver = "#644F4F"
    
    White = "#FFFFFF"
    Silver = "#BFC0C0"
    Coral = "#4F5D75"
    Cadet = "#2D3142"

    Success     = "#198754"
    Warning     = "#EED202"
    Danger      = "#FF002D"
    
def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def center(w, h, frame):
    ws = frame.winfo_screenwidth()
    hs = frame.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    frame.geometry("%dx%d+%d+%d" % (w, h, x, y))
    clear(frame)