import tkinter as tk
from msilib.schema import ListBox
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import matplotlib.animation as amines
from matplotlib import style
import time


LargeFont = ("Verdana", 12)
NormalFont = ("Verdana", 10)

def FileLocation():
    return filedialog.askopenfilename(initialdir="/", title="Select variant file", filetype=(("vcf", "*.vcf"), ("All Files", "*.*")))

class FileProcessor(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #Initailizinf tkinter
        tk.Tk.iconbitmap(self, default="iconImage_1.ico")
        tk.Tk.wm_title(self, "Visualizing vcf files")

        container = tk.Frame(self) # setting up the container for the fileProcessor
        container.pack(side="top", fill="both", expand=True) # setting the window to the screen
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for addPage in (StartPage, PageOne):
            frame = addPage(container, self)
            self.frames[addPage] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("StartingImage.PNG")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.pack()
        AddVcf = ttk.Button(self, text="Add VCF file", command=lambda: controller.show_frame(PageOne))
        AddVcf.pack()
        #startTime = time.time()  I am trying to make the start up image to disappear using a timer event instead of a submit
        #nextPage = startTime + 3
        #while True:
        #   if time.time()>nextPage:
         #     lambda: controller.show_frame(PageOne)
          #    break

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.Label = ttk.LabelFrame(self, text = "UpLoad .vcf file")
        self.Label.grid(column = 0, row = 1)
        self.FileButton()


        GeneText = ttk.Label(self, text ="Select the gene")
        GeneText.grid(column = 0, row = 2 )
        clicked = tk.StringVar()
        GeneName = ttk.OptionMenu(self, clicked, "Clicked for genes", "CYP2C9", "CYP2C19", "CYP2D6")
        GeneName.grid(column = 1, row = 2 )

        #African = ['ESN', 'GWD', 'LWK', 'MSL', 'YSL']
        #Ancestory = ['ESN', 'GWD', 'LWK', 'MSL', 'YSL']
        #EAsian = ['CDX', 'CHB', 'JPT', 'KHV', 'CHS']
        #SAsian =['BEB', 'GIH', 'PJL']
        #American = ['CLM', 'PEL', 'PUR']
        #European = ['GBR', 'FIN', 'IBS', 'PJL']
        #population =[African, Ancestory, American, EAsian, European, SAsian]

        PopuText = ttk.Label(self, text="Select the population")
        PopuText.grid(column=0, row=3)
        clicked = tk.StringVar()
        PopuName = ttk.OptionMenu(self, clicked, "Clicked for population", 'ESN', 'GWD', 'LWK', 'MSL', 'YSL', 'ESN', 'GWD', 'LWK', 'MSL', 'YSL','CDX', 'CHB', 'JPT', 'KHV', 'CHS', 'BEB', 'GIH', 'PJL', 'CLM', 'PEL', 'PUR', 'GBR', 'FIN', 'IBS', 'PJL')
        PopuName.grid(column=1, row=3)

    def FileButton(self):
        self.button = ttk.Button(self.Label, text = "Browse files", command = lambda :self.upLoadFile())
        self.button.grid(column = 1, row =1)

    def upLoadFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select variant file", filetype=(("vcf", "*.vcf"), ("All Files", "*.*")))
        self.label = ttk.Label(self, text = "File name" )
        self.label.grid(column = 2, row =1)
        self.label.configure(text=self.filename)

execute = FileProcessor()
execute.mainloop()
