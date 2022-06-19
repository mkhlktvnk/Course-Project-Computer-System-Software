import subprocess
import tkinter.messagebox
from tkinter import *
from tkinter import messagebox as mb, simpledialog
import time
import os


class FileService:
    def __init__(self, parent):
        self.__parent = parent

    def zip(self):
        item = ""
        zip_name = simpledialog.askstring("Архивация", "Введите имя архива: ")
        if not zip_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели!")
            return
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.__last_active_panel == "r":
            item = self.__parent.get_right_panel().get(self.__parent.get_right_panel().curselection())
        if zip_name.endswith(".tar.gz"):
            process = subprocess.Popen(["tar", "-cvf", zip_name, item], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                tkinter.messagebox.showwarning("Ошибка при архивации", "Произошла ошибка или у вас недостаточно прав!")
                return
        else:
            tkinter.messagebox.showwarning("Ошибка", "Поддерживаются только tar.gz архивы")
            return
        tkinter.messagebox.showinfo("Архивация", "Архив успешно создан!")
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_left_panel()
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_right_panel()

    def unzip(self):
        zip_name = ""
        if self.__parent.get_last_active_panel() == "l":
            zip_name = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.get_last_active_panel() == "r":
            zip_name = self.__parent.get_right_panel().get(self.__parent.get_right_panel().curselection())
        process = subprocess.Popen(["tar", "-xvf", zip_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            tkinter.messagebox.showwarning("Ошибка", "Поддерживается только формат tar.gz")
            return
        tkinter.messagebox.showinfo("Разархивация", "Архив успешно разархивирован!")
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_left_panel()
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_right_panel()

    def forward(self):
        if not os.path.isdir(self.__parent.__path_field.get()):
            return
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.set_left_panel_path(self.__parent.__path_field.get())
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.set_right_panel_path(self.__parent.__path_field.get())
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_left_panel()
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_right_panel()

    def back(self):
        s_path = self.__parent.get_path_field().get().split("/")
        new_path = "/".join(s_path[:-2]) + "/"
        self.__parent.update_path_field(new_path)
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.set_left_panel_path(new_path)
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.set_right_panel_path(new_path)
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_left_panel()
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_right_panel()

    def find(self):
        current_dir = "/"
        item_to_find = self.__parent.get_path_field().get()
        if item_to_find == current_dir:
            return
        if self.__parent.get_last_active_panel() == "l":
            # self.__parent.get_right_panel_path().delete(0, END)
            self.__parent.get_right_panel().delete(0, END)
        elif self.__parent.get_last_active_panel() == "r":
            # self.__parent.get_left_panel_path().delete(0, END)
            self.__parent.get_left_panel().delete(0, END)
        # self.__parent.get_path_field().delete(0, END)
        is_found = False
        for address, directories, files in os.walk(current_dir):
            for file in files:
                if file == item_to_find:
                    if self.__parent.get_last_active_panel() == "l":
                        self.__parent.get_right_panel().insert(0, os.path.join(address, file))
                    elif self.__parent.get_last_active_panel() == "r":
                        self.__parent.get_left_panel().insert(0, os.path.join(address, file))
                    is_found = True
            for directory in directories:
                if directory == item_to_find:
                    if self.__parent.get_last_active_panel() == "l":
                        self.__parent.get_right_panel().insert(0, os.path.join(address, directory))
                    elif self.__parent.get_last_active_panel() == "r":
                        self.__parent.get_left_panel().insert(0, os.path.join(address, directory))
                    is_found = True
        if not is_found:
            tkinter.messagebox.showwarning("Предупреждение", "Объектов с именем " + item_to_find + " не найдено!\n")
            self.__parent.update_left_panel()
            self.__parent.update_right_panel()

    def copy(self):
        item_path = ""
        path_to_copy = simpledialog.askstring("Перемещение", "Введите путь по которому вы хотите скопировать: ")
        if not path_to_copy:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели")
            return
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
            item_path = self.__parent.get_left_panel_path() + item
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel().get(self.__parent.get_right_panel().curselection())
            item_path = self.__parent.get_right_panel_path() + item
        if mb.askyesno("Копирование", "\nСкопировать из " + item_path + "\n В " + path_to_copy):
            if os.path.isdir(item_path):
                process = subprocess.Popen(["cp", "-R", item_path, path_to_copy])
            else:
                process = subprocess.Popen(["cp", item_path, path_to_copy],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                tkinter.messagebox.showwarning("Проблема при копировании", "Произошла ошибка или у вас недостаточно "
                                                                           "прав")
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def move(self):
        new_path = simpledialog.askstring("Перемещение",
                                          "Введите полный путь до директории, в которую хотите переместить:")
        if not os.path.isdir(new_path):
            tkinter.messagebox.showwarning("Ошибка", "Путь не указывает на директорию!")
            return
        item_path = ""
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
            if not item:
                tkinter.messagebox.showwarning("Ошибка", "Вы не выбрали элемент для перемещения")
                return
            item_path = self.__parent.get_left_panel_path() + item
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel_path().get(self.__parent.get_right_panel().curselection())
            if not item:
                tkinter.messagebox.showwarning("Ошибка", "Вы не выбрали элемент для перемещения")
                return
            item_path = self.__parent.get_right_panel_path() + item
        process = subprocess.Popen(["mv", item_path, new_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            tkinter.messagebox.showwarning("Проблема при перемещении", "Произошла ошибка или у вас недостаточно прав!")
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def rename(self):
        new_name = simpledialog.askstring("Переименование", "Введите новое имя: ")
        if not new_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели!")
            return
        item_path = ""
        target_path = ""
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
            item_path = self.__parent.get_left_panel_path() + item
            target_path = self.__parent.get_left_panel_path() + new_name
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel().get(self.__parent.get_right_panel().curselection())
            item_path = self.__parent.get_right_panel_path() + item
            target_path = self.__parent.get_right_panel_path() + new_name
        process = subprocess.Popen(["mv", item_path, target_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            tkinter.messagebox.showwarning("Проблема при переименовании", "Произошла ошибка или вас недостаточно прав!")
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def mkdir(self):
        path_to_create = ""
        dir_name = simpledialog.askstring("Создание директории", "Введите имя новой директории: ")
        if not dir_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели!")
            return
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_path_field(self.__parent.get_left_panel_path())
            path_to_create = self.__parent.get_left_panel_path() + dir_name
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_path_field(self.__parent.get_right_panel_path())
            path_to_create = self.__parent.get_right_panel_path() + dir_name
        if os.path.isdir(path_to_create) or os.path.isfile(path_to_create):
            tkinter.messagebox.showwarning(title="Предупреждение", message="Объект по выбранному пути уже существует!")
            return
        if mb.askyesno(title="Создать папку?", message=dir_name):
            os.makedirs(path_to_create)
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def create_file(self):
        file_name = simpledialog.askstring("Создание файла", "Введите имя файла: ")
        path_to_create = ""
        if not file_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели!")
            return
        if self.__parent.get_last_active_panel() == "l":
            self.__parent.update_path_field(self.__parent.get_left_panel_path())
            path_to_create = self.__parent.get_left_panel_path() + file_name
        elif self.__parent.get_last_active_panel() == "r":
            self.__parent.update_path_field(self.__parent.get_right_panel_path())
            path_to_create = self.__parent.get_right_panel_path() + file_name
        if os.path.exists(path_to_create):
            tkinter.messagebox.showwarning(title="Предупреждение", message="Объект по заданному пути уже существует!")
            return
        if mb.askyesno(title="Создать файл?", message=path_to_create):
            process = subprocess.Popen(["touch", path_to_create], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                tkinter.messagebox.showwarning("Проблема при создании файла", "Произошла ошибка или у вас "
                                                                              "недостаточно прав!")
            if self.__parent.get_last_active_panel() == "l":
                self.__parent.update_left_panel()
            elif self.__parent.get_last_active_panel() == "r":
                self.__parent.update_left_panel()

    def delete(self):
        full_path = ""
        if self.__parent.get_last_active_panel() == "l":
            full_path = self.__parent.get_path_field().get() + \
                        self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.get_last_active_panel() == "r":
            full_path = self.__parent.get_path_field().get() + \
                        self.__parent.get_right_panel().get(self.__parent.get_right_panel().curselection())
        if mb.askyesno("Удаление", "Вы уверены, что хотите удалить " + full_path + "?"):
            if os.path.isdir(full_path):
                process = subprocess.Popen(["rm", "-rf", full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(["rm", full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if error:
                tkinter.messagebox.showwarning("Проблема при удалении", "Произошла ошибка либо у вас недостаточно прав!")
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def info(self):
        item = ""
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel.get(self.__parent.get_right_panel().curselection())
        full_path = self.__parent.get_path_field().get() + item
        size = os.path.getsize(full_path)
        last_m_time = os.path.getmtime(full_path)
        c_time = os.path.getctime(full_path)
        message = f"Размер: {size} байт\n" + f"Последнее изменение: {time.ctime(last_m_time)}\n" \
                  + f"Дата создания: {time.ctime(c_time)}"
        tkinter.messagebox.showinfo("Информация", message)

    def make_soft_link(self):
        link_name = simpledialog.askstring("Создание ссылки", "Введите имя ссылки:")
        if not link_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели")
            return
        item = ""
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel.get(self.__parent.get_right_panel().curselection())
        full_path = self.__parent.get_path_field().get() + item
        process = subprocess.Popen(["ln", "-s", full_path, link_name])
        output, error = process.communicate()
        if error:
            tkinter.messagebox.showwarning("Ошибка", "Произошла ошибка при создании ссылки!")
            return
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

    def make_hard_link(self):
        link_name = simpledialog.askstring("Создание ссылки", "Введите имя ссылки:")
        if not link_name:
            tkinter.messagebox.showwarning("Ошибка", "Вы ничего не ввели")
            return
        item = ""
        if self.__parent.get_last_active_panel() == "l":
            item = self.__parent.get_left_panel().get(self.__parent.get_left_panel().curselection())
        elif self.__parent.get_last_active_panel() == "r":
            item = self.__parent.get_right_panel.get(self.__parent.get_right_panel().curselection())
        full_path = self.__parent.get_path_field().get() + item
        process = subprocess.Popen(["ln", full_path, link_name])
        output, error = process.communicate()
        if error:
            tkinter.messagebox.showwarning("Ошибка", "Произошла ошибка при создании ссылки!")
            return
        self.__parent.update_left_panel()
        self.__parent.update_right_panel()

