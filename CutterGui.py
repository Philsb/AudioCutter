from logging import setLoggerClass
import tkinter as tk
from tkinter.constants import COMMAND
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Text
import os as os

from matplotlib.pyplot import text
import WavCutter as wav

global cutter

def open():
    filepath = askopenfilename(
        filetypes=[("Wav Files", "*.wav"), ("All Files", "*.*")]
    )

    entry_path.delete(0,tk.END)
    entry_path.insert(0,filepath)

def init():

    try:
        path = str_path.get()
        #fix: variable global de parche
        global cutter 
        cutter = wav.WavCutter(path)
    except IOError:
        btn_cut.configure(state=tk.DISABLED)
        tk.messagebox.showinfo(title=None, message="No fue posible abrir el archivo .wav =(")
        return
    
    msecs = 0
    db = 0
    try:
        msecs = int(mseconds.get()) 
    except ValueError:
        msecs = 1000
        tk.messagebox.showinfo(title=None, message="Segundos no validos, 1000 por default.")
    
    try:
        db = int(decibels.get()) 
    except ValueError:
        db = -45
        tk.messagebox.showinfo(title=None, message="Decibeles no validos, -45 por default.")

    
    print("Milisegs: " + mseconds.get() + ", Decibeles: " + decibels.get())
    cutter.defineCuts(msecs, db)
    tk.messagebox.showinfo(title=None, message="Se proceso el archivo .wav!")
    btn_cut.configure(state=tk.ACTIVE)

def cut():
    if not os.path.exists("audios"):
        os.mkdir("audios")
        print("Directory " , "audios" ,  " Created ")
    else:    
        print("Directory " , "audios" ,  " already exists")
    cutter.cut()
    tk.messagebox.showinfo(title=None, message="Archivos .wav generados en la carpeta audios del mismo directorio.")

def on_closing(): 
    window.destroy()
    window.quit()


#----------Crea UI ----------------------

#Define marcos
window = tk.Tk()
window.title("Audio Cutter")
window.minsize(300,300)
window.maxsize(400,400)
window.protocol("WM_DELETE_WINDOW", on_closing)


#Define los frames
frame1 = tk.Frame(master=window, relief=tk.RAISED, bd=2,width=200, height=700, bg="azure3")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

#-----------------------
#label de archivo
lbl_arch = tk.Label(master = frame1, width = 15, text = "Archivo")
lbl_arch.grid(row=0, column=0, sticky="w", padx=5, pady=5)
#boton de explorar
btn_explorer = tk.Button(master=frame1,text="...",command = open, width=3)
btn_explorer.grid(row=0 , column=2,sticky="ew",padx=5, pady=5)
#entrada de file explorer
str_path = tk.StringVar() 
entry_path = tk.Entry(master=frame1, width = 20,text="", textvariable=str_path)
entry_path.grid(row=0, column=1,sticky="ew")
#-----------------------
#label de segundos a esperar
    
lbl_secs = tk.Label(master = frame1, width = 15, text = "Milisegs del silencio")
lbl_secs.grid(row=1, column=0, sticky="w", padx=5, pady=5)
#entrada de segundos a esperar
mseconds = tk.StringVar()
entry_secs = tk.Entry(master=frame1, width = 20, textvariable=mseconds)
entry_secs.grid(row=1, column=1, sticky="w")
entry_secs.delete(0,tk.END)
entry_secs.insert(0,"1000")
#-----------------------
#label de decibeles minimos
lbl_db = tk.Label(master = frame1, width = 15, text = "Decibeles del silencio")
lbl_db.grid(row=2, column=0, sticky="w",padx=5, pady=5)
#entrada de decibeles minimos
decibels = tk.StringVar()
entry_db = tk.Entry(master=frame1, width = 20,textvariable=decibels)
entry_db.grid(row=2, column=1, sticky="w")
entry_db.delete(0,tk.END)
entry_db.insert(0,"-45")

#-----------------------
#boton de abrir
btn_open = tk.Button(master=frame1,text="Procesar",command = init, width=10)
btn_open.grid(row=3, column=0 ,sticky="",padx=5, pady=5)

#boton de cortar
btn_cut = tk.Button(master=frame1,text="Generar .wavs", state=tk.DISABLED,command = cut, width=10)
btn_cut.grid(row=3, column = 1,sticky="",padx=5, pady=5)

#ejecuta ventana
window.mainloop()

