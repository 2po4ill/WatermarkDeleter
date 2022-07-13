from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
import shutil
import imagebuilder
from PIL import Image


def duplicatechecker(file):
    """ Функция возвращающая название файла неконфликтующее с возможными повторениями в папке """

    if os.path.exists(file):
        filetype = file[getdot(file):]
        file = file[:getdot(file)-1] + "copy." + filetype
        duplicatechecker(file)
    return file


def getdot(item):
    """ Функция возвращающая индекс нужного среза для получения формата файла по его директории """

    if isinstance(item, str):
        for i in range(1, len(item)):
            if item[-i] == ".":
                return -i+1


def getslash(item):
    """ Функция возвращающая индекс нужного среза для получения названия файла с .(формат файла) по его директории """

    if isinstance(item, str):
        for i in range(1, len(item)):
            if item[-i] == "/":
                return -i+1


class App(Tk):
    """
    Класс наследующий у tkinter'а аттрибуты, реализуется окно приложения

    аттрибуты:
    shadowlist - список директорий файлов находящихся в буферной папке
    shadow - директория буферной папки
    directory - директория папки в которую будут перенесены файлы
    filelist - список директорий файлов, выбранных пользователем
    title - название окна
    resizable - метод класса tkinter, определяющий редактирование окна в ширину и в длинну
    text - аттрибут содержащий экземпляр класса Text, определяющий размер окна

    btn_xxx - экземпляр класса Button, реализующий кнопку в окне
    xxx.pack() - метод класса tkinter, выводящий какой-либо элемент в окно приложения
    """

    def __init__(self):
        super().__init__()
        self.shadowlist = []
        self.shadow = ""
        self.directory = ""
        self.filelist = []
        self.title('Вотермарк мэйкер')
        self.resizable(width=False, height=False)
        self.text = Text(width=120, height=5)

        btn_file = Button(self, text="Выбрать файл", command=self.choose_file)
        btn_dir = Button(self, text="Выбрать папку для изображений", command=self.choose_directory)
        btn_del = Button(self, text="Убрать элемент", command=self.delete_element)
        btn_use = Button(self, text="Выполнить", command=self.use_on_btn)
        btn_clr = Button(self, text="Очистить", command=self.clear)

        btn_file.pack(padx=180, pady=10)
        btn_dir.pack(padx=180, pady=10)
        btn_del.pack(padx=180, pady=10)
        btn_use.pack(padx=180, pady=10)
        btn_clr.pack(padx=180, pady=10)
        self.list_update()

    def choose_file(self):
        """ Метод выбора файла/файлов с помощью проводника, вызывается кнопкой btn_file """

        filetypes = (("Изображение", "*.jpg *.png"), )
        os.chdir(os.getcwd())
        if not os.path.isdir("shadow"):
            os.mkdir("shadow")
            self.shadow = os.path.join(os.getcwd(), "shadow")
        else:
            self.shadow = os.path.join(os.getcwd(), "shadow")
        filename = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes, multiple=True)
        if filename != "":
            if App.confirm("Добавить выбранные файлы?"):
                for i in filename:
                    self.checkfile(i)
                self.text.delete(1.0, END)
                self.list_update()
            elif len(self.shadowlist) == 0:
                shutil.rmtree(app.shadow)
                app.shadow = ""
        else:
            shutil.rmtree(app.shadow)
            app.shadow = ""

    def choose_directory(self):
        """ Метод выбора папки с помощью проводника, вызывается кнопкой btn_dir """

        self.directory = askdirectory(title="Выбрать папку для изображений", initialdir="/")
        if self.directory != "":
            if App.confirm("Выбрать " + self.directory + " как папку с результатом?"):
                pass
            else:
                self.directory = ""
        self.text.delete(1.0, END)
        self.list_update()

    def delete_element(self):
        """ Метод выбора элемента из буферной папки, и удаление его из буферных списков, списков файлов """

        if self.shadow != "" and len(self.shadowlist) != 0:
            filetypes = (("Изображение", "*.jpg *.png"),)
            filename = askopenfilename(title="Удаление из списка", initialdir=self.shadow, filetypes=filetypes, multiple=True)
            if filename != "":
                if App.confirm("Удалить выбранные файлы?"):
                    tempos = []
                    for i in filename:
                        tempos.append(i)
                        if i in self.shadowlist:
                            os.remove(i)
                            x = self.shadowlist.index(i)
                            self.shadowlist.remove(i)
                            self.filelist.pop(x)
                        else:
                            App.show_error("Изображения не было в списке выбранных вами")
        else:
            App.show_error("Список файлов пуст, выберите что-нибудь")
        self.text.delete(1.0, END)
        self.list_update()

    def use_on_btn(self):
        """ Метод выполняющий удаление пикселей выбранных изображений сбрасывающий их копию в выбранную папку """

        if self.shadow == "" or len(self.shadowlist) == 0:
            App.show_error("Список файлов пуст, выберите что-нибудь")
        elif self.directory == "":
            App.show_error("Выберите директорию для результата")
        else:
            if App.confirm("Выполнить для выбранных файлов и директории?"):
                for file in os.listdir(self.shadow):
                    path = os.path.join(self.shadow, file)
                    if ".png" in path:
                        image = Image.open(path)
                        imagebuilder.imagereader(image)
                        result = os.path.join(self.directory, file)
                        result = duplicatechecker(result)
                        image.save(result, "png")
                    elif ".jpg" in path:
                        image = Image.open(path)
                        imagebuilder.imagereader(image)
                        result = os.path.join(self.directory, file)
                        result = duplicatechecker(result)
                        image.save(result, "png")
                App.show_info("Успешно выполнено")
                self.shadowlist.clear()
                self.filelist.clear()
                shutil.rmtree(self.shadow)
                self.shadow = ""
                self.directory = ""
                self.text.delete(1.0, END)
                self.list_update()

    def checkfile(self, filename):
        """ Метод заполняющий буферную папку и списки связанные с выбором файлов, файлами из choose_file """

        if filename in self.filelist:
            App.show_error(filename + " уже выбран")
        else:
            self.filelist.append(filename)
            temp = self.shadow + "\\" + filename[getslash(filename):]
            shutil.copyfile(filename, temp)
            tempo = ""
            for i in temp:
                if i != "\\":
                    tempo += i
                else:
                    tempo += '/'
            self.shadowlist.append(tempo)
        self.text.delete(1.0, END)
        self.list_update()

    def clear(self):
        """ Метод очистки буферной папки с связянных списков """

        if self.shadow != "":
            if App.confirm("Очистить список выбранных файлов?"):
                self.shadowlist.clear()
                self.filelist.clear()
                shutil.rmtree(self.shadow)
                self.shadow = ""
        else:
            App.show_error("Список файлов пуст, выберите что-нибудь")
        self.text.delete(1.0, END)
        self.list_update()

    def list_update(self):
        """ Метод обновляющий текстовый дисплей окна названием финальной директории и выбранных файлов """

        for element in self.filelist:
            self.text.insert(1.0, "- " + element + '\n')
        if self.directory != "":
            self.text.insert(1.0, "Выбранные изображения:" + '\n')
            self.text.insert(1.0, self.directory + " - выбранная директория" + '\n')
        self.text.pack()

    @staticmethod
    def confirm(msg):
        """ Статический метод для диалоговых окон yes, no, возвращает значение bool """

        answer = askyesno(title="Подтвердите операцию", message=msg)
        return answer

    @staticmethod
    def show_info(msg):
        """ Статический метод для окон уведомлений """

        showinfo("Информация", msg)

    @staticmethod
    def show_error(errormsg):
        """ Статический метод для окон ошибок """

        showerror("Ошибка", errormsg)


app = App()
app.mainloop()
if app.shadow != "":
    shutil.rmtree(app.shadow)
    app.shadow = ""
