from Notifications_functions import *
from tkinter import messagebox
import os


def organizer(receipt_path,
              notifications_path,
              notifications_file,
              only_receipt,
              only_notifications,
              explode_notifications,
              merge_rec_note,
              flip_receipt,
              flip_note,
              merge_all
              ):

    both = True if not only_receipt and not only_notifications else False
    names_receipt = []
    names_note = []

    if only_receipt or both:
        try:
            os.chdir(receipt_path)
            lista = os.listdir()
            for i in range(len(lista)):
                os.rename(lista[i], new_file_name(lista[i], names_receipt, flip_receipt, "receipt"))
        except:
            messagebox.showinfo(message='Coś poszło nie tak ze zwrotkami.\nSkonsultuj się z kimś.', icon="error")

    if only_notifications or both:
        try:
            if explode_notifications:
                spliter(notifications_file, notifications_path)
            os.chdir(notifications_path)
            lista = os.listdir()
            for i in range(len(lista)):
                os.rename(lista[i], new_file_name(lista[i], names_note, flip_note, "note"))
        except:
            messagebox.showinfo(message='Coś poszło nie tak z zawiadomieniami.\n Skonsultuj się z kimś.', icon="error")

    if merge_rec_note:
        list_note = os.listdir(notifications_path)
        try:
            list_receipt = os.listdir(receipt_path)
            merger(notifications_path, receipt_path, list_receipt, list_note)
        except:
            messagebox.showinfo(message='Coś poszło nie tak z łączeniem zwrotek i zawiadomień.\nSkonsultuj się z kimś.',
                                icon="error")

    if merge_all:
        try:
            merger_all(notifications_path)
        except:
            messagebox.showinfo(message='Coś poszło nie tak z łączeniem wszystkiego w całość.\nSkonsultuj się z kimś.',
                                icon="error")

    messagebox.showinfo(message="Skończone!")
