from pdfminer.high_level import extract_text
from tkinter import filedialog
from tkinter import messagebox
import os


def new_file_name(path):
    text = extract_text(path)
    print(text)
    index1 = text.find("Nazwa") + 11
    index2 = text.find("Nazwa cd")
    text2 = ""
    for i in range(index1, index2):
        text2 += text[i]
    text2 = text2.lstrip()
    text2 = text2.rstrip()
    c = int(len(text2) / 2)
    text3 = ""
    for i in range(c):
        text3 += text2[i]
    text3 += ".pdf"
    return text3

try:
    dirname = filedialog.askdirectory()
    os.chdir(dirname)
    lista = os.listdir(dirname)
    for i in range(len(lista)):
        os.rename(lista[i], new_file_name(lista[i]))
except:
    messagebox.showinfo(message='Coś poszło nie tak. Skonsultuj się z kimś.', icon="error")
messagebox.showinfo(message="Skończone!")