from tkinter import filedialog
from tkinter import messagebox
from Notifications_functions import *
import os


explode = messagebox.askyesno(title="Rozbić?", message="Rozbić plik z zawiadomieniami?\nTak - Wskaż plik do robicia "
                                                       "jeżeli.\nNie - wskaż folder z zawiadomieniami.")

if explode:
    path = filedialog.askopenfilename()
    spliter(path)
    path = mod_path(path)
else:
    path = filedialog.askdirectory()

names = []
try:
    os.chdir(path)
    lista = os.listdir(path)
    change = messagebox.askyesno(title="Zamienić", message="Czy zamienić miejscami imię z nazwiskiem?\nUWAGA!! Nazwy "
                                                           "instytucji też zmienią pierwszy człon")
    for i in range(len(lista)):
        os.rename(lista[i], new_file_name(lista[i], names, change, "note"))
except:
    messagebox.showinfo(message='Coś poszło nie tak. Skonsultuj się z kimś.', icon="error")

messagebox.showinfo(message="Skończone!")
merge = messagebox.askyesno(title="Zamienić", message="Czy chcesz złączyć ze zwrotkami?\nJeżeli tak to "
                                                      "wskaż folder")
if merge:
    names_pdf = os.listdir(path)
    try:
        path_zw = filedialog.askdirectory()
        lista_zw = os.listdir(path_zw)
        merger(path, path_zw, lista_zw, names_pdf)
    except:
        messagebox.showinfo(message='Coś poszło nie tak. Skonsultuj się z kimś.', icon="error")
messagebox.showinfo(message="Skończone!")
