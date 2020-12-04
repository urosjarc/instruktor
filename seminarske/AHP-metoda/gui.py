from PyQt5 import QtWidgets, uic, QtGui, Qt, QtCore
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np
from main import Primerjaj, Sestavi


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.__init()

    def __init(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(dir_path + '/main.ui', self)

        self.dodajAlternativoPB.clicked.connect(self.dodajAlternativo)
        self.dodajParameterPB.clicked.connect(self.dodajParameter)
        self.izracunajPB.clicked.connect(self.izracunaj)
        self.resetPB.clicked.connect(self.reset)

        self.reset()

    def dodajAlternativo(self):
        ime = self.alternativaLE.text()
        self.alternativaLE.clear()
        self.alternative.append(ime)
        self.update_vnos_vrednostiLE()

    def dodajParameter(self):
        ime = self.parameterLE.text()
        self.vnosVrednostiKriterijevTE.clear()
        self.parameterLE.clear()
        self.parametri.append(ime)
        self.update_vnos_vrednostiLE()

        vsebino = "\t\t"
        vsebino += "\t".join(self.parametri)
        vsebino += f"\nValues:\t"
        vsebino += '\t,'*len(self.parametri)
        self.vnosVrednostiKriterijevTE.setText(vsebino)

    def update_vnos_vrednostiLE(self):
        self.vnosVrednostiTE.clear()
        vsebino = "\t\t"
        vsebino += "\t".join(self.alternative)
        vsebino += "\n"

        for i, par in enumerate(self.parametri):
            vsebino += f"{par}:\t"
            vsebino += '\t,'*len(self.alternative)
            vsebino += "\n"


        self.vnosVrednostiTE.setPlainText(vsebino)

    def sparsaj_vnosVrednostiTE(self):
        vsebino = self.vnosVrednostiTE.toPlainText()
        vrstice = vsebino.split("\n")[1:]
        self.utezi_alternativ = []
        for v in vrstice:
            v = [int(ele.replace(',', '')) for ele in v.split()[1:]]
            if len(v) == len(self.alternative):
                self.utezi_alternativ.append(v)

    def sparsaj_vnosVrednostiKriterijevTE(self):
        vsebino = self.vnosVrednostiKriterijevTE.toPlainText()
        vrstice = vsebino.split("\n")[1]
        self.utezi_parametrov = [int(ele.replace(',', '')) for ele in vrstice.split()[1:]]
        print(self.utezi_parametrov)

    def izracunaj(self):
        self.sparsaj_vnosVrednostiTE()
        self.sparsaj_vnosVrednostiKriterijevTE()

        # Sestavi slovar matrik za parametre {<para1>: np.array(<matrika>}
        slovar_matrik_utezi = {}
        for i, param in enumerate(self.parametri):
            matrika = []
            for y in range(len(self.alternative)):
                vrstica_matrike = []
                for x in range(len(self.alternative)):
                    py = self.utezi_alternativ[i][y]
                    px = self.utezi_alternativ[i][x]
                    vrstica_matrike.append(py/px)
                matrika.append(vrstica_matrike)
            slovar_matrik_utezi[param] = np.array(matrika)

        # Sestavi matriko utezi za parametre
        matrika_kriterij = []
        for y in range(len(self.parametri)):
            vrstica_matrike = []
            for x in range(len(self.parametri)):
                py = self.utezi_parametrov[y]
                px = self.utezi_parametrov[x]
                vrstica_matrike.append(py/px)
            matrika_kriterij.append(vrstica_matrike)

        # Slovar matrik primerjam
        slovar_primerjav = {}
        for parameter, array in slovar_matrik_utezi.items():
            slovar_primerjav[parameter] = Primerjaj(parameter, array, self.alternative, 3)
        otroci = slovar_primerjav.values()

        # Sestavi koncno porocilo
        for l in matrika_kriterij:
            print(l)

        stars = Primerjaj('Izbor', np.array(matrika_kriterij), self.alternative, 3)
        Sestavi('Izbor', stars, otroci).porocilo()

    def reset(self):
        self.alternative = []
        self.parametri = []
        self.utezi_alternativ = []
        self.utezi_parametrov = []
        self.vnosVrednostiTE.clear()
        self.vnosVrednostiKriterijevTE.clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
