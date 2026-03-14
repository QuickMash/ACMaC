# Will be deprecated in favor of electron app, but this is easier for now.
# TODO: Deprecate this in favor of electron app
import tkinter as tk
from tkinter import messagebox

def show_dialog(title, message, type='okcancel'):
    root = tk.Tk()
    root.withdraw()
    if type == 'okcancel':
        result = messagebox.askokcancel(title, message)
    elif type == 'yesno':
        result = messagebox.askyesno(title, message)
    root.destroy()
    return result