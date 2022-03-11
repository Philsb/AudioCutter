import sys
import os as os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
from PyQt5.QtWidgets import *
import WavCutter as wav

class MainWindow(QMainWindow):    
    settings = QSettings('Felipe Sánchez Baldi', 'Luis Diego Pacheco')
    settings.setFallbacksEnabled(False)
    version = 'V0.1'

    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)
        loadUi("cutter.ui",self)
        self.setWindowTitle("AudioCutter " + self.version)

        # Se definen las funciones asignadas a los botones

        self.audio_selec.clicked.connect(self.audio_file)
        self.text_selec.clicked.connect(self.text_file)
        self.dir_selec.clicked.connect(self.work_dir)
        self.btn_open.clicked.connect(self.init)
        self.btn_cut.clicked.connect(self.cut)
        self.generar_txt.clicked.connect(self.gen_text)
        self.cerrar.clicked.connect(self.close)

        data_dir=os.getcwd()
        self.directorio.setText(data_dir)

    
    def init(self):
        global cutter
        try:
            path = self.entry_path.text()
            cutter = wav.WavCutter(path)
        except IOError:
            self.btn_cut.setEnabled(False)
            QMessageBox.warning(self, "Alerta", "No fue posible abrir el archivo .wav")
            return
        msecs = 0
        db = 0
        try:
            msecs = int(self.entry_secs.value()) 
        except ValueError:
            msecs = 1000
            QMessageBox.warning(self, "Alerta", "Segundos no validos, 1000 por default.")
                
        try:
            db = int(self.entry_db.value()) 
        except ValueError:
            db = -45
            QMessageBox.warning(self, "Alerta", "Decibeles no validos, -45 por default.")
            
        print("Milisegs: " + str(self.entry_secs.value()) + ", Decibeles: " + str(self.entry_db.value()) )
        segmentos=cutter.defineCuts(msecs, db)
        QMessageBox.warning(self, "Alerta", "Se proceso el archivo .wav!")
        self.lcdNumber.display(segmentos)
        self.lcdNumber.update()
        self.btn_cut.setEnabled(True)

    def cut(self):
        if not os.path.exists("audios"):
            os.mkdir("audios")
            QMessageBox.warning(self, "Alerta", "Directory audios Created ")
        else:  
            QMessageBox.warning(self, "Alerta", "Directory audios already exists ")  
            
        nombre = "voluntaria1"
        try:
            nombre = str(self.entry_name.text()) 
        except ValueError:
            nombre = "voluntaria1"
            QMessageBox.warning(self, "Alerta", "Sin nombre, voluntaria1 por default.")
                
        cutter.cut(nombre)
        QMessageBox.warning(self, "Alerta", "Archivos .wav generados en la carpeta audios del mismo directorio.")
        self.generar_txt.setEnabled(True)
        return

    def gen_text(self):
        
        archivo=self.archivo_texto.text() 
        with open(archivo, 'r', encoding="utf-8") as filetext:
            datos = filetext.read()
        filetext.close()
        datos=datos.split("\n")
        name = self.entry_name.text()
        cantidad_textos=len(datos)
        print (cantidad_textos)
        j=0
        while j < cantidad_textos:
            with open(("audios/" + name + "_{:03d}".format(j))+".txt", 'w', encoding="utf-8") as fp:
                fp.write(datos[j])
                fp.close()
            j=j+1
            self.lcdNumber_2.display(j)
            self.lcdNumber.update()
            

        return

    def audio_file(self):
        data_dir=self.directorio.text()
        if data_dir=="":
            data_dir=os.getcwd()
        fname=QFileDialog.getOpenFileName(self, "Abrir Archivo", data_dir,"Archivos de audio (*.wav);;Todos (*.*)")
        self.entry_path.setText(fname[0])
        return

    def text_file(self):
        data_dir=self.directorio.text()
        if data_dir=="":
            data_dir=os.getcwd()
        textfile=QFileDialog.getOpenFileName(self, "Abrir Archivo", data_dir,"Archivos de texto (*.txt);;Todos (*.*)")
        self.archivo_texto.setText(textfile[0])
        return

    def work_dir(self):
        data_dir=self.directorio.text()
        if data_dir=="":
            data_dir=os.getcwd()
        data_dir=QFileDialog.getExistingDirectory(self,"Choose Directory",data_dir)
        self.directorio.setText(data_dir)
        os.chdir(data_dir)
        return


def main():
# main
    app = QApplication(sys.argv)
    inicio = MainWindow()
    inicio.setMinimumWidth(800)
    inicio.setMinimumHeight(650)
    inicio.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':

    main()