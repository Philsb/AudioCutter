from logging import setLoggerClass
import tkinter as tk
from tkinter.constants import COMMAND
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Text
import os as os

from matplotlib.pyplot import text
import WavCutter as wav

class Gui:
    def __init__(self):
        self.cutter = None

        self.window = tk.Tk()
        self.window.title("Audio Cutter")
        self.window.minsize(300,300)
        self.window.maxsize(400,400)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        #Define los frames
        self.frame1 = tk.Frame(master=self.window, relief=tk.RAISED, bd=2,width=200, height=700, bg="azure3")
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        #-----------------------
        #label de archivo
        self.lbl_arch = tk.Label(master = self.frame1, width = 15, text = "Archivo")
        self.lbl_arch.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        #boton de explorar
        self.btn_explorer = tk.Button(master=self.frame1,text="...",command = self.open, width=3)
        self.btn_explorer.grid(row=0 , column=2,sticky="ew",padx=5, pady=5)
        #entrada de file explorer
        self.str_path = tk.StringVar() 
        self.entry_path = tk.Entry(master=self.frame1, width = 20,text="", textvariable=self.str_path)
        self.entry_path.grid(row=0, column=1,sticky="ew")
        #-----------------------
        #label de segundos a esperar
         
        self.lbl_secs = tk.Label(master = self.frame1, width = 15, text = "Milisegs del silencio")
        self.lbl_secs.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        #entrada de segundos a esperar
        self.mseconds = tk.StringVar()
        self.entry_secs = tk.Entry(master=self.frame1, width = 20, textvariable=self.mseconds)
        self.entry_secs.grid(row=1, column=1, sticky="w")
        self.entry_secs.delete(0,tk.END)
        self.entry_secs.insert(0,"1000")
        #-----------------------
        #label de decibeles minimos
        self.lbl_db = tk.Label(master = self.frame1, width = 15, text = "Decibeles del silencio")
        self.lbl_db.grid(row=2, column=0, sticky="w",padx=5, pady=5)
        #entrada de decibeles minimos
        self.decibels = tk.StringVar()
        self.entry_db = tk.Entry(master=self.frame1, width = 20,textvariable=self.decibels)
        self.entry_db.grid(row=2, column=1, sticky="w")
        self.entry_db.delete(0,tk.END)
        self.entry_db.insert(0,"-45")

        #-----------------------
        #boton de abrir
        self.btn_open = tk.Button(master=self.frame1,text="Procesar",command = self.init, width=10)
        self.btn_open.grid(row=3, column=0 ,sticky="",padx=5, pady=5)

        #boton de cortar
        
        self.btn_cut = tk.Button(master=self.frame1,text="Generar .wavs", state=tk.DISABLED,command = self.cut, width=10)
        self.btn_cut.grid(row=3, column = 1,sticky="",padx=5, pady=5)


        self.window.mainloop()

    def open(self):
        filepath = askopenfilename(
            filetypes=[("Wav Files", "*.wav"), ("All Files", "*.*")]
        )

        self.entry_path.delete(0,tk.END)
        self.entry_path.insert(0,filepath)

    def init(self):

        try:
            path = self.str_path.get()
            self.cutter = wav.WavCutter(path)
        except IOError:
            self.btn_cut.configure(state=tk.DISABLED)
            tk.messagebox.showinfo(title=None, message="No fue posible abrir el archivo .wav =(")
            return
        
        msecs = 1000
        db = -45
        try:
            msecs = int(self.mseconds.get()) 
        except ValueError:
            msecs = 1000
            tk.messagebox.showinfo(title=None, message="Segundos no validos, 1000 por default.")
        
        try:
            db = int(self.decibels.get()) 
        except ValueError:
            db = -45
            tk.messagebox.showinfo(title=None, message="Decibeles no validos, -45 por default.")

        
        print("Milisegs: " + self.mseconds.get() + ", Decibeles: " + self.decibels.get())
        self.cutter.defineCuts(msecs, db)
        tk.messagebox.showinfo(title=None, message="Se proceso el archivo .wav!")
        self.btn_cut.configure(state=tk.ACTIVE)

    def cut(self):
        if not os.path.exists("audios"):
            os.mkdir("audios")
            print("Directory " , "audios" ,  " Created ")
        else:    
            print("Directory " , "audios" ,  " already exists")
        self.cutter.cut()
        tk.messagebox.showinfo(title=None, message="Archivos .wav generados en la carpeta audios del mismo directorio.")

    def on_closing(self): 
        self.window.destroy()
        self.window.quit()


window = Gui()