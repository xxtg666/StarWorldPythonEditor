import tkinter 

def base64_tkinter(base64:bytes):
    return tkinter.PhotoImage(data=base64)

ice_cube = b"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"