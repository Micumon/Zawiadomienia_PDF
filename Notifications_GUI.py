import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class NotificationsOrganizer:
    def __init__(self, root: Tk):
        root.title("Nazwy Zawiadomień")
        root.grid()
        mframe = ttk.Frame(root, padding=10, width=800, height=800, borderwidth=5, relief="solid")
        # noinspection PyTypeChecker
        mframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.receipt_path = ""
        self.notifications_path = ""

        self.label_folder_with_zw_zaw = ttk.Label(mframe,
                                                  text='Wybierz folder zawierający foldery:\n'
                                                       '"zawiadomienia" i "zwrotki":',
                                                  justify="left")
        # noinspection PyTypeChecker
        self.label_folder_with_zw_zaw.grid(column=0, columnspan=4, row=0, sticky=(N, W))

        # self.var_folder_with_zw_zaw = StringVar()
        self.button_folder_with_zw_zaw = (
            ttk.Button(mframe,
                       text="Przeglądaj...",
                       command=lambda: self.action_button_folder_with_zw_zaw(filedialog.askdirectory())))
        # noinspection PyTypeChecker
        self.button_folder_with_zw_zaw.grid(column=5, columnspan=4, row=0, sticky=(N, W))

        self.__separator_nr1 = ttk.Separator(mframe, orient="horizontal")
        # noinspection PyTypeChecker
        self.__separator_nr1.grid(row=1, columnspan=9, sticky=(N, W, E))

        self.label_zw = ttk.Label(mframe, text="Zwrotki: ")
        # noinspection PyTypeChecker
        self.label_zw.grid(column=0, columnspan=2, row=2, sticky=(N, W))

        self.button_zw = ttk.Button(mframe, text="Przeglądaj...",
                                    command=lambda: self.action_button_zw(filedialog.askdirectory()))
        # noinspection PyTypeChecker
        self.button_zw.grid(column=2, columnspan=2, row=2, sticky=(N, W))

        self.__separator_nr2 = ttk.Separator(mframe, orient="vertical")
        # noinspection PyTypeChecker
        self.__separator_nr2.grid(row=2, rowspan=5, column=4, sticky=(N, S))

        self.label_zaw = ttk.Label(mframe, text="Zawiadomienia: ")
        # noinspection PyTypeChecker
        self.label_zaw.grid(column=5, columnspan=2, row=2, sticky=(N, W))

        self.button_zaw = ttk.Button(mframe,
                                     text="Przeglądaj...",
                                     command=lambda: self.action_button_zaw(filedialog.askdirectory()))
        # noinspection PyTypeChecker
        self.button_zaw.grid(column=7, columnspan=2, row=2, sticky=(N, W))

        self.var_list_zw_list = StringVar()
        self.list_zw = Listbox(mframe, height=15, listvariable=self.var_list_zw_list)
        self.list_zw.grid(column=0, row=3, columnspan=3)
        self.scrollbar_list_zw_y = ttk.Scrollbar(mframe, orient="vertical", command=self.list_zw.yview)
        self.scrollbar_list_zw_x = ttk.Scrollbar(mframe, orient="horizontal", command=self.list_zw.xview)
        self.list_zw.configure(yscrollcommand=self.scrollbar_list_zw_y.set,
                               xscrollcommand=self.scrollbar_list_zw_x.set)
        self.scrollbar_list_zw_y.grid(column=3, row=3, sticky=(N, S, W))
        self.scrollbar_list_zw_x.grid(column=0, columnspan=3, row=4, sticky=(N, W, E))

        self.var_list_zaw_list = StringVar()
        self.list_zaw = Listbox(mframe, height=15, listvariable=self.var_list_zaw_list)
        self.list_zaw.grid(column=5, row=3, columnspan=3)
        self.scrollbar_list_zaw_y = ttk.Scrollbar(mframe, orient="vertical", command=self.list_zaw.yview)
        self.scrollbar_list_zaw_x = ttk.Scrollbar(mframe, orient="horizontal", command=self.list_zaw.xview)
        self.list_zaw.configure(yscrollcommand=self.scrollbar_list_zaw_y.set,
                                xscrollcommand=self.scrollbar_list_zaw_x.set)
        self.scrollbar_list_zaw_y.grid(column=8, row=3, sticky=(N, S, W))
        self.scrollbar_list_zaw_x.grid(column=5, columnspan=3, row=4, sticky=(N, W, E))

        self.var_explode_zaw = StringVar(value="1")
        self.check_explode_zaw = ttk.Checkbutton(mframe, text="Rozbić plik z zawiadomieniami",
                                                 variable=self.var_explode_zaw,
                                                 command=lambda: self.action_check_explode_zaw())
        self.check_explode_zaw.grid(column=5, columnspan=4, row=5, sticky=(N, W))

        self.label_explode_zaw = ttk.Label(mframe, text="Zaznacz na liście\nplik z zawiadomieniami.")
        self.label_explode_zaw.grid(column=5, columnspan=4, row=6, sticky=(N, W))

        self.var_merge = StringVar(value="0")
        self.check_merge_all = ttk.Checkbutton(mframe, text="Połączyć zawiadomienia ze zwrotkami?",
                                               variable=self.var_merge, state='disabled')
        self.check_merge_all.grid(column=0, columnspan=9, row=7, sticky=(N, W))

        self.button_execute = ttk.Button(mframe, text="Wykonaj operacje",
                                         command=lambda: self.action_execute())
        self.button_execute.grid(column=0, columnspan=3, row=8, sticky=(N, W))

        self.button_reset = ttk.Button(mframe, text="Resetuj", command=lambda: self.action_reset())
        self.button_reset.grid(column=5, columnspan=3, row=8, sticky=(N, W))

    def action_check_explode_zaw(self):
        match self.var_explode_zaw.get():
            case "1":
                self.label_explode_zaw.configure(text="Zaznacz na liście\nplik z zawiadomieniami.")
            case "0":
                self.label_explode_zaw.configure(text="\n")

    @staticmethod
    def __folder_finder(list_arg):
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
        self.button_zw.configure(state="disable")
        self.button_zaw.configure(state="disable")
        self.check_merge_all.configure(state="active")

    def action_button_zw(self, working_path):
        os.chdir(working_path)
        self.var_list_zw_list.set(os.listdir())
        self.button_zaw.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="disabled")
        self.check_explode_zaw.configure(state="disabled")

    def action_button_zaw(self, working_path):
        os.chdir(working_path)
        self.var_list_zaw_list.set(os.listdir())
        self.button_zw.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="disabled")

    def action_execute(self):
        pass

    def action_reset(self):
        self.var_explode_zaw.set("1")
        self.label_explode_zaw.configure(text="Zaznacz na liście\nplik z zawiadomieniami.")
        self.var_list_zaw_list.set("")
        self.var_list_zw_list.set("")
        self.button_zw.configure(state="active")
        self.button_zaw.configure(state="active")
        self.check_merge_all.configure(state="disabled")
        self.button_folder_with_zw_zaw.configure(state="active")
        self.check_explode_zaw.configure(state="active")