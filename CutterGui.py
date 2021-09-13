import tkinter as tk
from tkinter.constants import COMMAND
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Text

from matplotlib.pyplot import text
import WavCutter as wav

class Gui:
    def __init__(self):
        self.cutter = None
        self.cut_labels = []

        self.window = tk.Tk()
        self.window.minsize(300,300)
        self.window.maxsize(700,700)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        #Define los frames
        self.frame1 = tk.Frame(master=self.window, relief=tk.RAISED, bd=2,width=200, height=700, bg="azure3")
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        #-----------------------
        #boton de abrir
        self.btn_open = tk.Button(master=self.frame1,text="Abrir",command = self.init, width=10)
        self.btn_open.grid(row=0, column=0, sticky="ew",padx=5, pady=5)
        #boton de explorar
        self.btn_explorer = tk.Button(master=self.frame1,text="...",command = self.open, width=3)
        self.btn_explorer.grid(row=0, column=3, sticky="ew",padx=5, pady=5)
        #entrada de file explorer
        self.str_path = tk.StringVar() 
        self.entry_path = tk.Entry(master=self.frame1, width = 20,text="", textvariable=self.str_path)
        self.entry_path.grid(row=0, column=1, sticky="w")
        #-----------------------
        #label de segundos a esperar
         
        self.lbl_secs = tk.Label(master = self.frame1, width = 15, text = "Segundos")
        self.lbl_secs.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        #entrada de segundos a esperar
        self.seconds = tk.StringVar()
        self.entry_secs = tk.Entry(master=self.frame1, width = 20)
        self.entry_secs.grid(row=1, column=1, sticky="w")
        #-----------------------
        #label de decibeles minimos
        self.lbl_db = tk.Label(master = self.frame1, width = 15, text = "Decibeles")
        self.lbl_db.grid(row=2, column=0, sticky="w",padx=5, pady=5)
        #entrada de decibeles minimos
        self.decibels = tk.StringVar()
        self.entry_db = tk.Entry(master=self.frame1, width = 20,)
        self.entry_db.grid(row=2, column=1, sticky="w")

        #-----------------------
        #boton de cortar
        self.btn_cut = tk.Button(master=self.frame1,text="Cortar",command = self.cut, width=10)
        self.btn_cut.grid(row=3, column = 0,sticky="",padx=5, pady=5)


        self.window.mainloop()

    def open(self):
        filepath = askopenfilename(
            filetypes=[("Wav Files", "*.wav"), ("All Files", "*.*")]
        )
        self.entry_path.delete(0,tk.END)
        self.entry_path.insert(0,filepath)

    def init(self):
        path = self.str_path.get()
        self.cutter = wav.WavCutter(path)
        if self.cutter != None:
            cuts = self.cutter.defineCuts(500, -45.0)

            tk.messagebox.showinfo(title=None, message="Se abrio archivo")
        else: ""

    def cut(self):
        self.cutter.cut()
        print("cortar")

    def on_closing(self): 
        self.window.destroy()
        self.window.quit()


window = Gui()