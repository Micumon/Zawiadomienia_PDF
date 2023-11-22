from tkinter import filedialog
from tkinter import messagebox
from Notifications_functions import *
import os


try:
    dir_name = filedialog.askdirectory()
    os.chdir(dir_name)
    lista = os.listdir(dir_name)
    for i in range(len(lista)):
        os.rename(lista[i], new_file_name(lista[i], [], 0, "receipt"))
except:
    messagebox.showinfo(message='Coś poszło nie tak. Skonsultuj się z kimś.', icon="error")
messagebox.showinfo(message="Skończone!")
