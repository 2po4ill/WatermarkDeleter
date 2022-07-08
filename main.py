from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
import copy


class App(Tk):
    def __init__(self):
        super().__init__()
        self.directory = None
        self.filelist = []
        btn_file = Button(self, text="Выбрать файл", command=self.choose_file)
        btn_dir = Button(self, text="Выбрать папку",command=self.choose_directory)
        btn_list = Button(self, text="Убрать элемент", command=self.show_list)
        btn_file.pack(padx=60, pady=10)
        btn_dir.pack(padx=60, pady=10)
        btn_list.pack(padx=60, pady=10)

    def choose_file(self):
        filetypes = (("Изображение", "*.jpg *.gif *.png"), )
        filename = askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes, multiple=True)
        if isinstance(filename, str):
            if filename in self.filelist:
                self.show_error(filename + " уже выбран")
            else:
                self.filelist.append(filename)
        else:
            for i in filename:
                if i in self.filelist:
                    self.show_error(i + " уже выбран")
                else:
                    self.filelist.append(i)

    def choose_directory(self):
        self.directory = askdirectory(title="Выбрать папку для изображений", initialdir="/")

    def show_error(self, errormsg):
        showerror("Ошибка", errormsg)

    def show_list(self):
        if not os.path.isdir("folder"):
            os.mkdir("folder")
        print(self.filelist)


if __name__ == "__main__":
    app = App()
    app.mainloop()
