import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Notifications_organizer import organizer


class NotificationsOrganizer:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Nazwy Zawiadomień")
        self.root.grid()
        mframe = ttk.Frame(self.root, padding=10, width=800, height=800, borderwidth=5, relief="solid")
        mframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.progress_window = ""
        self.var_receipt_path = ""
        self.var_notifications_path = ""
        self.var_only_receipt = False
        self.var_only_notifications = False

        # Folder selection for both options
            # Label
        self.label_folder_with_zw_zaw = ttk.Label(mframe,
                                                  text='Wybierz folder zawierający foldery:\n'
                                                       '"zawiadomienia" i "zwrotki":',
                                                  justify="left")
        self.label_folder_with_zw_zaw.grid(column=0, columnspan=4, row=0, sticky=(N, W))
            # Button
        self.button_folder_with_zw_zaw = (
            ttk.Button(mframe,
                       text="Przeglądaj...",
                       command=lambda: self.action_button_folder_with_zw_zaw(filedialog.askdirectory())))
        self.button_folder_with_zw_zaw.grid(column=5, columnspan=4, row=0, sticky=(N, W))

        # Separator
        self.__separator_nr1 = ttk.Separator(mframe, orient="horizontal")
        self.__separator_nr1.grid(row=1, columnspan=9, sticky=(N, W, E))

        # Only receipts
        self.label_zw = ttk.Label(mframe, text="Zwrotki: ")
        self.label_zw.grid(column=0, columnspan=2, row=2, sticky=(N, W))

        self.button_zw = ttk.Button(mframe, text="Przeglądaj...",
                                    command=lambda: self.action_button_zw(filedialog.askdirectory()))
        self.button_zw.grid(column=2, columnspan=2, row=2, sticky=(N, W))

        self.__separator_nr2 = ttk.Separator(mframe, orient="vertical")
        self.__separator_nr2.grid(row=2, rowspan=6, column=4, sticky=(N, S))

        # Only Notes
        self.label_zaw = ttk.Label(mframe, text="Zawiadomienia: ")
        self.label_zaw.grid(column=5, columnspan=2, row=2, sticky=(N, W))

        self.button_zaw = ttk.Button(mframe,
                                     text="Przeglądaj...",
                                     command=lambda: self.action_button_zaw(filedialog.askdirectory()))

        self.button_zaw.grid(column=7, columnspan=2, row=2, sticky=(N, W))

        # Listbox for receipts
        self.var_list_zw_list = StringVar()
        self.list_zw = Listbox(mframe, height=15, listvariable=self.var_list_zw_list)
        self.list_zw.grid(column=0, row=3, columnspan=3)
        self.scrollbar_list_zw_y = ttk.Scrollbar(mframe, orient="vertical", command=self.list_zw.yview)
        self.scrollbar_list_zw_x = ttk.Scrollbar(mframe, orient="horizontal", command=self.list_zw.xview)
        self.list_zw.configure(yscrollcommand=self.scrollbar_list_zw_y.set,
                               xscrollcommand=self.scrollbar_list_zw_x.set)
        self.scrollbar_list_zw_y.grid(column=3, row=3, sticky=(N, S, W))
        self.scrollbar_list_zw_x.grid(column=0, columnspan=3, row=4, sticky=(N, W, E))

        # Listbox for notifications
        self.var_list_zaw_list = StringVar()
        self.list_zaw = Listbox(mframe, height=15, listvariable=self.var_list_zaw_list)
        self.list_zaw.grid(column=5, row=3, columnspan=3)
        self.scrollbar_list_zaw_y = ttk.Scrollbar(mframe, orient="vertical", command=self.list_zaw.yview)
        self.scrollbar_list_zaw_x = ttk.Scrollbar(mframe, orient="horizontal", command=self.list_zaw.xview)
        self.list_zaw.configure(yscrollcommand=self.scrollbar_list_zaw_y.set,
                                xscrollcommand=self.scrollbar_list_zaw_x.set)
        self.scrollbar_list_zaw_y.grid(column=8, row=3, sticky=(N, S, W))
        self.scrollbar_list_zaw_x.grid(column=5, columnspan=3, row=4, sticky=(N, W, E))

        # Checkboxes
        self.var_explode_zaw = StringVar(value="1")
        self.check_explode_zaw = ttk.Checkbutton(mframe, text="Rozbić plik z zawiadomieniami",
                                                 variable=self.var_explode_zaw,
                                                 command=lambda: self.action_check_explode_zaw())
        self.check_explode_zaw.grid(column=5, columnspan=4, row=5, sticky=(N, W))

        self.label_explode_zaw = ttk.Label(mframe, text="Zaznacz na liście\nplik z zawiadomieniami.")
        self.label_explode_zaw.grid(column=5, columnspan=4, row=6, sticky=(N, W))

        self.var_flip_names_zw = StringVar(value="0")
        self.check_flip_names_zw = ttk.Checkbutton(mframe, text="Zamień imię z nazwiskiem",
                                                   variable=self.var_flip_names_zw, state='disabled')
        self.check_flip_names_zw.grid(column=0, columnspan=4, row=7, sticky=(N, W))

        self.var_flip_names_zaw = StringVar(value="0")
        self.check_flip_names_zaw = ttk.Checkbutton(mframe, text="Zamień imię z nazwiskiem",
                                                   variable=self.var_flip_names_zaw, state='disabled')
        self.check_flip_names_zaw.grid(column=5, columnspan=4, row=7, sticky=(N, W))

        self.var_merge = StringVar(value="0")
        self.check_merge_all = ttk.Checkbutton(mframe, text="Połączyć zawiadomienia ze zwrotkami?",
                                               variable=self.var_merge, state='disabled',
                                               command=lambda: self.action_check_merge())
        self.check_merge_all.grid(column=0, columnspan=9, row=8, sticky=(N, W))

        self.var_merge_merged = StringVar(value="0")
        self.check_merge_merged = ttk.Checkbutton(mframe, text="Połączyć wynik?",
                                                  variable=self.var_merge_merged, state='disabled')
        self.check_merge_merged.grid(column=0, columnspan=9, row=9, sticky=(N, W))

        # Execute
        self.button_execute = ttk.Button(mframe, text="Wykonaj operacje",
                                         command=lambda: self.action_execute())
        self.button_execute.grid(column=0, columnspan=3, row=10, sticky=(N, W))

        # Reset
        self.button_reset = ttk.Button(mframe, text="Resetuj", command=lambda: self.action_reset())
        self.button_reset.grid(column=5, columnspan=3, row=10, sticky=(N, W))

    def __default_note_file(self):
        self.list_zaw.selection_set(0,0)

    def action_check_explode_zaw(self):
        match self.var_explode_zaw.get():
            case "1":
                self.label_explode_zaw.configure(text="Zaznacz na liście\nplik z zawiadomieniami.")
            case "0":
                self.label_explode_zaw.configure(text="\n")

    def __folder_finder(self, list_arg):
        result_receipt = ""
        result_notifications = ""


        notifications_list = ("zawiadomienia", "Zawiadomienia", "ZAWIADOMIENIA", "ZAW", "zaw", "Zaw")
        for note in notifications_list:
            if note in list_arg:
                result_notifications = note + "\\"

        receipt_list = ("Zwrotki", "ZWROTKI", "zwrotki", "zw", "ZW", "Zw", "zwr", "Zwr", "ZWR")
        for note in receipt_list:
            if note in list_arg:
                result_receipt = note + "\\"

        self.var_receipt_path = os.getcwd() + "\\" + result_receipt
        self.var_notifications_path = os.getcwd() + "\\" + result_notifications

        if result_notifications == "":
            new_dir = os.getcwd()+r"\Zawiadomienia"
            os.mkdir(new_dir)
            result_notifications = "Zawiadomienia\\"
            with open(new_dir + "\\Najpierw przygotuj zawiadomienia", "w") as file:
                file.write("Pacan!")

        if result_receipt == "":
            new_dir = os.getcwd() + r"\Zwrotki"
            os.mkdir(new_dir)
            result_receipt = "Zwrotki\\"
            with open(new_dir + "\\Najpierw przygotuj zwrotki", "w") as file:
                file.write("Pacan!")

        return result_receipt, result_notifications

    def action_button_folder_with_zw_zaw(self, working_path):
        os.chdir(working_path)
        folder_list = os.listdir()
        receipt_dir_name, notifications_dir_name = self.__folder_finder(folder_list)
        self.var_list_zaw_list.set(os.listdir(notifications_dir_name))
        self.var_list_zw_list.set(os.listdir(receipt_dir_name))
        self.__default_note_file()
        self.button_zw.configure(state="disable")
        self.button_zaw.configure(state="disable")
        self.check_merge_all.configure(state="active")
        self.check_flip_names_zaw.configure(state="active")
        self.check_flip_names_zw.configure(state="active")

    def action_button_zw(self, working_path):
        os.chdir(working_path)
        self.var_receipt_path = os.getcwd() + "\\"
        self.var_list_zw_list.set(os.listdir())
        self.var_list_zaw_list.set(["---"])
        self.__default_note_file()
        self.button_zaw.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="disabled")
        self.check_explode_zaw.configure(state="disabled")
        self.var_only_receipt = True
        self.check_flip_names_zw.configure(state="active")

    def action_button_zaw(self, working_path):
        os.chdir(working_path)
        self.var_notifications_path = os.getcwd() + "\\"
        self.var_list_zaw_list.set(os.listdir())
        self.__default_note_file()
        self.button_zw.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="disabled")
        self.var_only_notifications = True
        self.check_flip_names_zaw.configure(state="active")

    def action_check_merge(self):
        match self.var_merge.get():
            case "1":
                self.check_merge_merged.configure(state="active")
            case "0":
                self.check_merge_merged.configure(state="disable")

    def action_execute(self):
        if self.var_notifications_path != "":
            note_file = self.var_notifications_path + self.list_zaw.get(self.list_zaw.curselection()[0])
        else:
            note_file = ""

        organizer(receipt_path=self.var_receipt_path,
                  notifications_path=self.var_notifications_path,
                  notifications_file=note_file,
                  only_receipt=self.var_only_receipt,
                  only_notifications=self.var_only_notifications,
                  explode_notifications=bool(int(self.var_explode_zaw.get())),
                  merge_rec_note=bool(int(self.var_merge.get())),
                  flip_receipt=bool(int(self.var_flip_names_zaw.get())),
                  flip_note=bool(int(self.var_flip_names_zw.get())),
                  merge_all=bool(int(self.var_merge_merged.get()))
                  )

    def action_reset(self):
        self.var_notifications_path = ""
        self.var_receipt_path = ""
        self.var_only_receipt = False
        self.var_only_notifications = False
        self.var_explode_zaw.set("1")
        self.var_merge_merged.set("0")
        self.label_explode_zaw.configure(text="Zaznacz na liście\nplik z zawiadomieniami.")
        self.var_list_zaw_list.set("")
        self.var_list_zw_list.set("")
        self.button_zw.configure(state="active")
        self.button_zaw.configure(state="active")
        self.check_merge_all.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="active")
        self.check_explode_zaw.configure(state="active")
        self.check_flip_names_zaw.configure(state="disabled")
        self.check_flip_names_zw.configure(state="disabled")
        self.check_merge_merged.configure(state="disabled")
        self.var_merge.set("0")
        self.var_flip_names_zaw.set("0")
        self.var_flip_names_zw.set("0")
