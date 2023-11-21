import PyPDF2
from pdfminer.high_level import extract_text
from tkinter import filedialog
from tkinter import messagebox
import os


def name_flipper(text):
    text_list = text.split()
    text_list[0], text_list[1] = text_list[1], text_list[0]
    text = " ".join(text_list)
    return text


def new_file_name(pdf, names, change):
    text = extract_text(pdf)
    text = text.split("Z A W I")
    text.pop(1)
    text = "".join(text)
    text = text.split(".2023r.")
    text.pop(0)
    text = "".join(text)
    text = text.strip()
    text = text.split("\n")
    text2 = text[0]
    text2 = text2.strip()
    text3 = ""
    for letter in text2:
        if letter in ("\"", "\\", "/", ":", "*", "?", "<", ">"):
            continue
        else:
            text3 += letter
    counter = 0
    if change:
        text3 = name_flipper(text3)
    while 1:
        counter += 1
        if text3 in names:
            text3 += str(counter)
        else:
            break
    names.append(text3)
    text3 += ".pdf"
    return text3


def mod_path(path):
    path = path[0:path.rfind(r"/")]
    return path


def merger(path_na, path_zw, lista_zw, names):
    all_names = zip(names, lista_zw)
    c = 1
    for m, n in all_names:
        mergerer = PyPDF2.PdfMerger()
        with open(path_na + "/" + m, 'rb') as f:
            mergerer.append(PyPDF2.PdfReader(f))
        with open(path_zw + "/" + n, 'rb') as f:
            mergerer.append(PyPDF2.PdfReader(f))
        mergerer.write(path_na + f"/{c}.pdf")
        c += 1


def spliter(path):
    reader = PyPDF2.PdfReader(path)
    path2 = mod_path(path)
    i = 1
    for page in range(len(reader.pages)):
        if page % 2 == 1:
            continue
        else:
            output = PyPDF2.PdfWriter()
            output.add_page(reader.pages[page])
            output.add_page(reader.pages[page + 1])
            with open(path2 + f"/{i}.pdf", "wb") as output_stream:
                output.write(output_stream)
            i += 1
    os.remove(path)


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
        os.rename(lista[i], new_file_name(lista[i], names, change))
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
