"""
Модуль реализации интерфейса приложения добавления/удаления вотермарки
"""
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
import shutil
import imagebuilder
import imagebuilderjpg
import watermarkadder
from PIL import Image


def duplicatechecker(img):
    """ Функция возвращающая название файла неконфликтующее с возможными повторениями в папке """

    index = getdot(img)
    while os.path.exists(img[:index] + "png") or os.path.exists(img[:index] + "jpg"):
        filetype = img[index:]
        img = img[:index - 1] + "copy." + filetype
    return img


def getdot(item):
    """ Функция возвращающая индекс нужного среза для получения формата файла по его директории """

    if isinstance(item, str):
        for i in range(1, len(item)):
            if item[-i] == ".":
                return -i+1


def getslash(item):
    """
    Функция возвращающая индекс среза для получения названия файла по его директории
    """

    if isinstance(item, str):
        for i in range(1, len(item)):
            if item[-i] == "/" or item[-i] == "\\":
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
        self.text = Text(width=60, height=5)
        self.bckgrimage = ""
        self.shadowbckgrn = ""

        self.btn_wtrmrkdel = Button(self, text="Удалить вотермарку", command=self.wtrmrkdel)
        self.btn_wtrmrkmk = Button(self, text="Добавить вотермарку", command=self.wtrmrkmk)


        self.btn_img = Button(self, text="Выбрать изображения", command=self.chs_img)
        self.btn_dir = Button(self, text="Выбрать папку для изображений", command=self.chs_dir)
        self.btn_del = Button(self, text="Убрать элемент", command=self.delete_element)
        self.btn_clr = Button(self, text="Очистить", command=self.clear)
        self.btn_back = Button(self, bg='red', text="Назад", command=self.rollback)

        # удаление вотермарки
        self.btn_usedel = Button(self, text="Выполнить", command=self.usedel_on_btn)

        #добавление вотермарки
        self.btn_background = Button(self, text="Выбрать фон", command=self.background)
        self.btn_usemake = Button(self, text="Выполнить", command=self.usemake_on_btn)

        self.btn_wtrmrkdel.pack(padx=180, pady=10)
        self.btn_wtrmrkmk.pack(padx=180, pady=10)
        self.list_update()

    def chs_img(self):
        """ Метод выбора файла/файлов с помощью проводника, вызывается кнопкой btn_file """

        filetypes = (("Изображение", "*.jpg *.png"), )
        os.chdir(os.getcwd())
        if not os.path.isdir("shadow"):
            os.mkdir("shadow")
            self.shadow = os.path.join(os.getcwd(), "shadow")
        else:
            self.shadow = os.path.join(os.getcwd(), "shadow")
        filename = askopenfilename(title="Открыть файл", initialdir="/",
                                   filetypes=filetypes, multiple=True)
        if filename != "":
            if App.confirm("Добавить выбранные файлы?"):
                for i in filename:
                    self.checkfile(i)
                self.text.delete(1.0, END)
                self.list_update()
            elif len(self.shadowlist) == 0:
                shutil.rmtree(self.shadow)
                self.shadow = ""
                self.shadowlist = []
                self.filelist = []
        else:
            shutil.rmtree(self.shadow)
            self.shadow = ""
            self.shadowlist = []
            self.filelist = []

    def chs_dir(self):
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
        """
        Метод выбора элемента из буферной папки, и удаление его из буферных списков, списков файлов
        """

        if self.shadow != "" and len(self.shadowlist) != 0:
            filetypes = (("Изображение", "*.jpg *.png"),)
            title = "Сбросить выбранные изображения"
            filename = askopenfilename(title=title, initialdir=self.shadow,
                                       filetypes=filetypes, multiple=True)
            if filename != "":
                if App.confirm("Сбросить выбранные файлы?"):
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

    def usedel_on_btn(self):
        """
        Метод выполняющий удаление пикселей выбранных
        изображений сбрасывающий их копию в выбранную папку
        """

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
                        imagebuilderjpg.imagereader(image)
                        result = os.path.join(self.directory, file[:getdot(file)] + 'png')
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

    def usemake_on_btn(self):
        if self.shadow == "" or len(self.shadowlist) == 0:
            App.show_error("Список файлов пуст, выберите что-нибудь")
        elif self.directory == "":
            App.show_error("Выберите директорию для результата")
        elif self.bckgrimage == "":
            App.show_error("Выберите изображение для фона")
        else:
            if App.confirm("Выполнить для выбранных файлов и директории?"):
                for file in os.listdir(self.shadow):
                    path = os.path.join(self.shadow, file)
                    image = Image.open(path)
                    result = os.path.join(self.directory, file)
                    result = duplicatechecker(result)
                    watermark = os.path.join(self.shadowbckgrn, os.listdir(self.shadowbckgrn)[0])
                    watermarkadder.imagereader(image, watermark, result)
                App.show_info("Успешно выполнено")
                self.shadowlist.clear()
                self.filelist.clear()
                shutil.rmtree(self.shadow)
                shutil.rmtree(self.shadowbckgrn)
                self.shadowbckgrn = ''
                self.shadow = ""
                self.directory = ""
                self.bckgrimage = ""
                self.text.delete(1.0, END)
                self.list_update()

    def checkfile(self, filename):
        """ 
        Метод заполняющий буферную папку и списки связанные с выбором файлов, файлами из choose_file
        """

        if filename in self.filelist:
            App.show_error(filename + " уже выбран")
        elif filename == self.bckgrimage:
            App.show_error(filename + " уже выбран как фон")
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
        """ Метод очистки буферной папки и связянных списков """

        if self.shadow != "" or self.directory != '' or self.bckgrimage != '':
            if App.confirm("Очистить список выбранных файлов?"):
                if self.shadow != "":
                    self.shadowlist.clear()
                    self.filelist.clear()
                    shutil.rmtree(self.shadow)
                    self.shadow = ""
                self.directory = ""
                self.bckgrimage = ""
        else:
            App.show_error("Список файлов пуст, выберите что-нибудь")
        self.text.delete(1.0, END)
        self.list_update()

    def rollback(self):
        if len(self.shadowlist) != 0 or self.directory != '' or self.bckgrimage != '':
            if App.confirm('Ваши выбранные файлы и директории будут сброшенны, вы уверены?'):
                if len(self.shadowlist) != 0:
                    self.shadowlist.clear()
                    self.filelist.clear()
                    shutil.rmtree(self.shadow)
                    self.shadow = ""
                if self.shadowbckgrn != '':
                    shutil.rmtree(self.shadowbckgrn)
                    self.shadowbckgrn = ''
                self.directory = ''
                self.bckgrimage = ''

        self.btn_img.pack_forget()
        self.btn_dir.pack_forget()
        self.btn_background.pack_forget()
        self.btn_del.pack_forget()
        self.btn_usedel.pack_forget()
        self.btn_usemake.pack_forget()
        self.btn_clr.pack_forget()
        self.btn_back.pack_forget()
        self.text.pack_forget()

        self.btn_wtrmrkdel.pack(padx=180, pady=10)
        self.btn_wtrmrkmk.pack(padx=180, pady=10)
        self.text.delete(1.0, END)
        self.list_update()

    def background(self):
        filetypes = (("Изображение", "*.jpg *.png"),)
        os.chdir(os.getcwd())
        if not os.path.isdir("shadowbckgrn"):
            os.mkdir("shadowbckgrn")
            self.shadowbckgrn = os.path.join(os.getcwd(), "shadowbckgrn")
        self.bckgrimage = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
        if self.bckgrimage != '' and self.bckgrimage not in self.filelist:
            if App.confirm('Вы хотите выбрать ' + self.bckgrimage + ' как фон для изображений?'):
                if self.shadowbckgrn != "":
                    for i in os.listdir(self.shadowbckgrn):
                        os.remove(os.path.join(self.shadowbckgrn, i))
                temp = self.shadowbckgrn + "\\" + self.bckgrimage[getslash(self.bckgrimage):]
                shutil.copyfile(self.bckgrimage, temp)
            else:
                shutil.rmtree(self.shadowbckgrn)
                self.shadowbckgrn = ""
                self.bckgrimage = ""
        elif self.bckgrimage in self.filelist:
            msg = 'Ваш фон уже добавлен как изображение, удалите изображение из списка файлов'
            App.show_error(msg)
            self.bckgrimage = ""
            shutil.rmtree(self.shadowbckgrn)
            self.shadowbckgrn = ""
        else:
            shutil.rmtree(self.shadowbckgrn)
            self.shadowbckgrn = ""
        self.text.delete(1.0, END)
        self.list_update()

    def list_update(self):
        """
        Метод обновляющий текстовый дисплей окна названием финальной директории и выбранных файлов
        """

        for element in self.filelist:
            self.text.insert(1.0, "- " + element + '\n')
        if self.directory != "":
            self.text.insert(1.0, "Выбранные изображения:" + '\n')
            self.text.insert(1.0, self.directory + " - выбранная директория" + '\n')
        if self.bckgrimage != "":
            self.text.insert(1.0, self.bckgrimage + " - выбранный фон" + '\n')
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

    def wtrmrkdel(self):
        self.btn_wtrmrkdel.pack_forget()
        self.btn_wtrmrkmk.pack_forget()
        self.text.pack_forget()

        self.btn_img.pack(padx=180, pady=10)
        self.btn_dir.pack(padx=180, pady=10)
        self.btn_del.pack(padx=180, pady=10)
        self.btn_usedel.pack(padx=180, pady=10)
        self.btn_clr.pack(padx=180, pady=10)
        self.btn_back.pack(padx=180, pady=10)

        self.list_update()

    def wtrmrkmk(self):
        self.btn_wtrmrkdel.pack_forget()
        self.btn_wtrmrkmk.pack_forget()
        self.text.pack_forget()

        self.btn_img.pack(padx=180, pady=10)
        self.btn_background.pack(padx=180, pady=10)
        self.btn_dir.pack(padx=180, pady=10)
        self.btn_del.pack(padx=180, pady=10)
        self.btn_usemake.pack(padx=180, pady=10)
        self.btn_clr.pack(padx=180, pady=10)
        self.btn_back.pack(padx=180, pady=10)

        self.list_update()


app = App()
app.mainloop()
if os.path.isdir("shadow"):
    shutil.rmtree(os.path.join(os.getcwd(), "shadow"))
if os.path.isdir("shadowbckgrn"):
    shutil.rmtree(os.path.join(os.getcwd(), "shadowbckgrn"))
