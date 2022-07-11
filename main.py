from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
import shutil


def getslash(item):
    if isinstance(item, str):
        for i in range(3, len(item)):
            if item[-i] == "/":
                return -i+1


class App(Tk):
    def __init__(self):
        super().__init__()
        self.shadowlist = []
        self.shadow = ""
        self.directory = ""
        self.filelist = []
        btn_file = Button(self, text="Выбрать файл", command=self.choose_file)
        btn_dir = Button(self, text="Выбрать папку для изображений", command=self.choose_directory)
        btn_del = Button(self, text="Убрать элемент", command=self.delete_element)
        btn_use = Button(self, text="Выполнить", command=self.use_on_btn)
        btn_file.pack(padx=60, pady=10)
        btn_dir.pack(padx=60, pady=10)
        btn_del.pack(padx=60, pady=10)
        btn_use.pack(padx=60, pady=10)

    def choose_file(self):
        filetypes = (("Изображение", "*.jpg *.png"), )
        os.chdir(os.getcwd())
        if not os.path.isdir("shadow"):
            os.mkdir("shadow")
            self.shadow = os.path.join(os.getcwd(), "shadow")
        else:
            self.shadow = os.path.join(os.getcwd(), "shadow")
        filename = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes, multiple=True)
        for i in filename:
            self.checkfile(i)

    def choose_directory(self):
        self.directory = askdirectory(title="Выбрать папку для изображений", initialdir="/")

    @staticmethod
    def show_error(errormsg):
        showerror("Ошибка", errormsg)

    def delete_element(self):
        filetypes = (("Изображение", "*.jpg *.png"),)
        filename = askopenfilename(title="Выберите файл для удаления", initialdir=self.shadow, filetypes=filetypes, multiple=True)
        print(filename)
        tempos = []
        for i in filename:
            tempos.append(i)
            print(tempos)
            if i in self.shadowlist:
                x = self.shadowlist.index(i)
                self.shadowlist.remove(i)
                self.filelist.pop(x)
            else:
                App.show_error("Изображение не было выбрано")

    def use_on_btn(self):
        pass

    def checkfile(self, filename):
        if filename in self.filelist:
            App.show_error(filename + " уже выбран")
        else:
            self.filelist.append(filename)
            temp = self.shadow + "\ " + filename[getslash(filename):]
            print(self.shadow)
            shutil.copyfile(filename, temp)
            self.shadowlist.append(temp)
            print(self.shadowlist)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    os.rmdir(os.path.join(os.getcwd(), 'shadow'))

