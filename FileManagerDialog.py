import subprocess
import sys
import tkinter.messagebox
from tkinter import *
import os

from FileService import FileService


class FileManagerDialog:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('Файловый менеджер')
        self.main_window.geometry("1700x820")
        self.main_window.resizable(False, False)

        self.__path_field = Entry(self.main_window)
        self.__path_field.grid(row=0, column=1, columnspan=4, sticky="nwes")

        self.__back_button = Button(self.main_window, text="Назад")
        self.__back_button.grid(row=0, column=0, sticky="nwes")
        self.__back_button.bind("<Button-1>", self.back_button_onclick)
        self.__program_info_button = Button(self.main_window, text="О программе")

        self.__forward_button = Button(self.main_window, text="Вперёд")
        self.__forward_button.grid(row=0, column=4, sticky="nwes")
        self.__forward_button.bind("<Button-1>", self.forward_button_onclick)

        self.__find_button = Button(self.main_window, text="Поиск", command=self.find_button_onclick)
        self.__find_button.grid(row=0, column=5, columnspan=1, sticky="nwes")

        self.__left_panel = Listbox(self.main_window, height=40, width=106, selectmode="single")
        self.__left_panel.grid(row=2, column=0, columnspan=3, sticky="nwes")
        self.__left_scrollbar = Scrollbar(command=self.__left_panel.yview)

        self.__right_panel = Listbox(self.main_window, height=40, width=106, selectmode="single")
        self.__right_panel.grid(row=2, column=3, columnspan=3, sticky="nwes")
        self.__right_scrollbar = Scrollbar(command=self.__right_panel.yview)

        self.__copy_button = Button(self.main_window,        text="Скопировать", width=8)
        self.__move_button = Button(self.main_window,        text="Переместить", width=8)
        self.__rename_button = Button(self.main_window,      text="Переименовать", width=8)
        self.__create_file_button = Button(self.main_window, text="Создать файл", width=8)
        self.__mkdir_button = Button(self.main_window,       text="Создать папку", width=8)
        self.__delete_button = Button(self.main_window,      text="Удалить", width=8)
        self.__info_button = Button(self.main_window,        text="Свойства", width=8)
        self.__zip_button = Button(self.main_window,         text="Архивировать", width=8)
        self.__unzip_button = Button(self.main_window,       text="Разархивировать", width=8)
        self.__soft_link_button = Button(self.main_window,   text="Создать мягкую ссылку", width=8)
        self.__hard_link_button = Button(self.main_window,   text="Создать жесткую ссылку", width=8)

        buttons = [
            self.__copy_button, self.__move_button, self.__rename_button,
            self.__create_file_button, self.__mkdir_button, self.__delete_button
        ]
        i = 0
        for button in buttons:
            button.grid(row=1, column=i, sticky="nwes")
            i += 1

        self.__info_button.grid(row=4, column=0, sticky="nwes")
        self.__zip_button.grid(row=4, column=1, sticky="nwes")
        self.__unzip_button.grid(row=4, column=2, sticky="nwes")
        self.__soft_link_button.grid(row=4, column=4, sticky="nwes")
        self.__hard_link_button.grid(row=4, column=5, sticky="nwes")

        self.__copy_button.bind("<Button-1>",        self.copy_button_onclick)
        self.__move_button.bind("<Button-1>",        self.move_button_onclick)
        self.__rename_button.bind("<Button-1>",      self.rename_button_onclick)
        self.__mkdir_button.bind("<Button-1>",       self.mkdir_button_onclick)
        self.__delete_button.bind("<Button-1>",      self.delete_button_onclick)
        self.__info_button.bind("<Button-1>",        self.info_button_onclick)
        self.__find_button.bind("<Button-1>",        self.find_button_onclick)
        self.__create_file_button.bind("<Button-1>", self.create_file_button_onclick)
        self.__zip_button.bind("<Button-1>",         self.zip_button_onclick)
        self.__unzip_button.bind("<Button-1>",       self.unzip_button_onclick)
        self.__hard_link_button.bind("<Button-1>",   self.hard_link_button_onclick)
        self.__soft_link_button.bind("<Button-1>",   self.soft_link_button_onclick)

        start_path = "/"
        self.__left_panel_path = start_path
        self.__right_panel_path = start_path

        self.__file_service = FileService(self)

        self.__last_active_panel = "l"
        self.__left_panel.bind("<Double-Button-1>", self.left_panel_on_doubleclick)
        self.__left_panel.bind("<Button-1>", self.left_panel_onclick)
        self.__right_panel.bind("<Double-Button-1>", self.right_panel_on_doubleclick)
        self.__right_panel.bind("<Button-1>", self.right_panel_onclick)

        self.update_left_panel()
        self.update_right_panel()
        self.update_path_field(start_path)

    def get_last_active_panel(self):
        return self.__last_active_panel

    def get_path_field(self):
        return self.__path_field

    def get_right_panel_path(self):
        return self.__right_panel_path

    def get_left_panel_path(self):
        return self.__left_panel_path

    def set_right_panel_path(self, path):
        self.__right_panel_path = path

    def set_left_panel_path(self, path):
        self.__left_panel_path = path

    def get_left_panel(self):
        return self.__left_panel

    def get_right_panel(self):
        return self.__right_panel

    def zip_button_onclick(self, event):
        self.__file_service.zip()
        self.__zip_button.config(relief=RAISED)

    def unzip_button_onclick(self, event):
        self.__file_service.unzip()
        self.__unzip_button.config(relief=RAISED)

    def forward_button_onclick(self, event):
        self.__file_service.forward()
        self.__forward_button.config(relief=RAISED)

    def back_button_onclick(self, event):
        self.__file_service.back()
        self.__back_button.config(relief=RAISED)

    def find_button_onclick(self, event):
        self.__file_service.find()
        self.__find_button.config(relief=RAISED)

    def copy_button_onclick(self, event):
        self.__file_service.copy()
        self.__copy_button.config(relief=RAISED)

    def move_button_onclick(self, event):
        self.__file_service.move()
        self.__move_button.config(relief=RAISED)

    def rename_button_onclick(self, event):
        self.__file_service.rename()
        self.__rename_button.config(relief=RAISED)

    def mkdir_button_onclick(self, event):
        self.__file_service.mkdir()
        self.__mkdir_button.config(relief=RAISED)

    def create_file_button_onclick(self, event):
        self.__file_service.create_file()
        self.__create_file_button.config(relief=RAISED)

    def delete_button_onclick(self, event):
        self.__file_service.delete()
        self.__delete_button.config(relief=RAISED)

    def info_button_onclick(self, event):
        self.__file_service.info()
        self.__info_button.config(relief=RAISED)

    def soft_link_button_onclick(self, event):
        self.__file_service.make_soft_link()
        self.__soft_link_button.config(relief=RAISED)

    def hard_link_button_onclick(self, event):
        self.__file_service.make_hard_link()
        self.__hard_link_button.config(relief=RAISED)

    def left_panel_on_doubleclick(self, event):
        current_path = self.__path_field.get()
        new_path = self.__left_panel.get(self.__left_panel.curselection())

        if os.path.isdir(current_path + new_path):
            self.__left_panel_path = current_path + new_path
            self.update_path_field(self.__left_panel_path)
            self.update_left_panel()
            self.update_right_panel()
        elif os.path.isfile(current_path + new_path):
            opener = "open" if sys.platform == "drawin" else "xdg-open"
            subprocess.call([opener, current_path + new_path])

    def right_panel_on_doubleclick(self, event):
        current_path = self.__path_field.get()
        new_path = self.__right_panel.get(self.__right_panel.curselection())

        if os.path.isdir(current_path + new_path):
            self.__right_panel_path = current_path + new_path
            self.update_path_field(self.__right_panel_path)
            self.update_left_panel()
            self.update_right_panel()
        elif os.path.isfile(current_path + new_path):
            opener = "open" if sys.platform == "drawin" else "xdg-open"
            subprocess.call([opener, current_path + new_path])

    def left_panel_onclick(self, event):
        if self.__last_active_panel == "r":
            self.__last_active_panel = "l"
            self.update_path_field(self.__left_panel_path)

    def right_panel_onclick(self, event):
        if self.__last_active_panel == "l":
            self.__last_active_panel = "r"
            self.update_path_field(self.__right_panel_path)

    def update_left_panel(self):
        self.__left_panel.delete(0, END)
        items = os.listdir(self.__left_panel_path)
        for item in items:
            if os.path.isdir(self.__left_panel_path + item):
                self.__left_panel.insert(END, item + "/")
            else:
                self.__left_panel.insert(END, item)

    def update_right_panel(self):
        self.__right_panel.delete(0, END)
        items = os.listdir(self.__right_panel_path)
        for item in items:
            if os.path.isdir(self.__right_panel_path + item):
                self.__right_panel.insert(END, item + "/")
            else:
                self.__right_panel.insert(END, item)

    def update_path_field(self, path):
        self.__path_field.delete(0, END)
        self.__path_field.insert(0, path)
        try:
            os.chdir(path)
        except OSError:
            tkinter.messagebox.showwarning("Ошибка", "Доступ запрещен!")
            self.__file_service.back()


if __name__ == "__main__":
    app = FileManagerDialog()
    app.main_window.mainloop()
