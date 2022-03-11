from pydub import AudioSegment
from pydub import silence

class WavCutter:
    def __init__(self, pathToWav):
        self.wav = AudioSegment.from_file(pathToWav, format="wav")
        self.cuts = []
    
    def defineCuts (self, silentSeconds, dbTreshold):
        segmentos=0 # Se añadió el contador de segmentos
        timestamp1 = 0
        timestamp2 = 0
        silenceNum = 0
        milli = 0
        self.cuts.append(0)
        while milli < len(self.wav):
            if self.wav[milli].dBFS < dbTreshold:
                if silenceNum == 0:
                    timestamp1 = milli
                silenceNum += 1
            else: 
                if silenceNum != 0:
                    timestamp2 = milli
                if silenceNum > silentSeconds:
                    cut = (timestamp2 - timestamp1 )/2 + timestamp1
                    self.cuts.append(cut)
                    segmentos=segmentos+1 # Contando los segmentos
                    print("Segmento #" + str(segmentos) +" Cut: " + str(timestamp1) + "-->" + str(int(cut))) #  se modifica la impresión
                    
                silenceNum = 0

            milli += 1
        #apend el cut del final
        self.cuts.append(milli)
        #return self.cuts
        return segmentos+1 #Se devuelve el número de segmentos encontrado

    def cut(self, name):
        cuttedAudio = []
        for i in range(len(self.cuts) - 1):
            cuttedAudio.append([self.cuts[i], self.cuts[i+1]])

        j=0
        for audio in cuttedAudio:
            chunk = self.wav[audio[0]:audio[1]]
            f = open(("audios/" + name + "_{:03d}".format(j))+".wav", "wb")
            chunk.export(f, format = "wav")
            f.close()
        # Archivo de texto vacío
        #    with open(("audios/" + name + "_{:03d}".format(j))+".txt", 'w') as fp:
        #        pass
            j += 1