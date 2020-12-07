from PyQt5 import QtWidgets, uic, QtGui, Qt, QtCore
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np
from PyQt5.QtWidgets import QMessageBox

from AHP import Primerjaj, Sestavi, Node


class GUI(QtWidgets.QMainWindow):
    def __init__(self):

        self.alternative = []
        self.primerjave = {
            # 'ime_primerjave': {
            #     'parametri': ['par1', 'par2'],
            #     'kriteriji': [],
            #     'matrika': []
            # }
        }

        super(GUI, self).__init__()
        self.__init()

    def __init(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(dir_path + '/gui.ui', self)

        self.dodajPB.clicked.connect(self.dodaj)
        self.izracunajPB.clicked.connect(self.izracunaj)
        self.resetPB.clicked.connect(self.reset)

        self.reset()

    def dodaj(self):
        self.alternative = [ele.replace(' ', '') for ele in self.imeAlternativLE.text().split(",")]
        ime = self.imePrimerjaveLE.text()
        parametri = [ele.replace(' ', '') for ele in self.parametriLE.text().split(",")]
        self.primerjave[ime] = {
            'parametri': parametri,
            'kriteriji': [],
            'matrika': []
        }

        # Zbrisi vnos vrednosti in vnosnih informacij
        self.vnosVrednostiKriterijevTE.clear()
        self.imePrimerjaveLE.clear()
        self.parametriLE.clear()

        # Update
        self._update_vnos_vrednostiTE()
        self._update_vnos_VrednostiKriterijevTE()

    def izracunaj(self):
        self._sparsaj_vnosVrednostiTE()
        self._sparsaj_vnosVrednostiKriterijevTE()

        porocilo = self._sestavi_porocilo()

        # Prikazi koncno porocilo v msg-boxu
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Porocilo AHP metode")
        msg.setText(porocilo.porocilo())
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def reset(self):
        self.alternative = []
        self.primerjave = { }
        self.vnosVrednostiTE.clear()
        self.vnosVrednostiKriterijevTE.clear()


    def _ustvari_primerjalno_matriko(self, imePrimerjave, parametri):
        vsebino = f'<{imePrimerjave}> ========================\n'
        vsebino += "\t\t"
        vsebino += "\t".join(self.alternative)
        vsebino += "\n"

        for i, par in enumerate(parametri):
            vsebino += f"{par}:\t"
            vsebino += '\t,'*len(self.alternative)
            vsebino += "\n"

        vsebino += "=================================="
        return vsebino

    def _ustvari_kriterijski_vektor(self, imePrimerjave, parametri):
        vsebino = f'<{imePrimerjave}> ========================\n'
        vsebino += "\t\t"
        vsebino += "\t".join(parametri)
        vsebino += f"\nValues:\t"
        vsebino += '\t,'*len(parametri)
        vsebino += "\n========================\n"
        return vsebino

    def _update_vnos_vrednostiTE(self):
        self.vnosVrednostiTE.clear()

        vsebine = []
        for ime, vrednosti in self.primerjave.items():
            vsebine.append(self._ustvari_primerjalno_matriko(ime, vrednosti['parametri']))

        vsebino = '\n'.join(vsebine)
        self.vnosVrednostiTE.setPlainText(vsebino)

    def _update_vnos_VrednostiKriterijevTE(self):
        self.vnosVrednostiKriterijevTE.clear()

        vsebine = []
        for ime, vrednosti in self.primerjave.items():
            vsebine.append(self._ustvari_kriterijski_vektor(ime, vrednosti['parametri']))

        vsebino = '\n'.join(vsebine)
        self.vnosVrednostiKriterijevTE.setPlainText(vsebino)

    def _sparsaj_vnosVrednostiTE(self):
        vsebino = self.vnosVrednostiTE.toPlainText()
        ime = None
        matrika = None
        for line in vsebino.split('\n'):
            if line.startswith('<'):
                ime = line.split('>')[0].replace('<', '')
                matrika = []
            if ':' in line:
                vrstica = []
                for ele in line.split(':')[-1].split(','):
                    if ele!='':
                        vrstica.append(float(ele.strip()))
                matrika.append(vrstica)
            if line.startswith('==='):
                self.primerjave[ime]['matrika'] = matrika

    def _sparsaj_vnosVrednostiKriterijevTE(self):
        vsebino = self.vnosVrednostiKriterijevTE.toPlainText()
        ime = None
        for line in vsebino.split('\n'):
            if line.startswith('<'):
                ime = line.split('>')[0].replace('<', '')
            if 'Values:' in line:
                vrstica = []
                for ele in line.split(':')[-1].split(','):
                    if ele != '':
                        vrstica.append(float(ele.strip()))
                self.primerjave[ime]['kriteriji'] = vrstica

    def _ustvari_np_matriki_kriterijev_in_primerjave(self, primerjava):
        slovar_matrik_utezi = {}

        for i, param in enumerate(primerjava['parametri']):
            matrika = []
            for y in range(len(self.alternative)):
                vrstica_matrike = []
                for x in range(len(self.alternative)):
                    py = primerjava['matrika'][i][y]
                    px = primerjava['matrika'][i][x]
                    vrstica_matrike.append(py/px)
                matrika.append(vrstica_matrike)
            slovar_matrik_utezi[param] = np.array(matrika)

        matrika_kriterijev = []
        for y in range(len(self.alternative)):
            vrstica_matrike = []
            for x in range(len(self.alternative)):
                py = primerjava['kriteriji'][y]
                px = primerjava['kriteriji'][x]
                vrstica_matrike.append(py/px)
            matrika_kriterijev.append(vrstica_matrike)

        return (matrika_kriterijev, slovar_matrik_utezi)

    def _sestavi_porocilo(self):
        # Sestavi slovar matrik za parametre {<para1>: np.array(<matrika>}
        slovar_matrik_utezi = {}
        for ime, primerjava in self.primerjave.items():
            slovar_matrik_utezi[ime] = self._ustvari_np_matriki_kriterijev_in_primerjave(primerjava)

        node = self.ustvari_drevo_nodov(slovar_matrik_utezi)
        node.sestavi_primerjave(self.alternative)
        node.sestavi_porocila()
        return node.porocilo
        # Ustvari kriterijske povezave..
        # Ustvari parameterske povezave..

    def ustvari_drevo_nodov(self, slovar_matrik_utezi, part = None, node=None):
        if part is None:
            part = slovar_matrik_utezi

        for key, val in part.items():
            if node is None:
                node = Node(key, val[0])
                return self.ustvari_drevo_nodov(slovar_matrik_utezi, val[1], node)


            child= Node(key, val)
            node.child.append(child)
            child.parent = node

            for p, val_p in slovar_matrik_utezi.items():
                if p == key:
                    child.matrix = val_p[0]
                    self.ustvari_drevo_nodov(slovar_matrik_utezi, val_p[1], child)
                    break
        return node
'''

<g> ========================
		a1	a2	a3
p1:		5,	7,	8,
p2:		5,	7,	8,
p3:		5,	7,	8,
==================================
<p1> ========================
		a1	a2	a3
p11:		5,	7,	8,
p22:		5,	7,	8,
p33:		5,	7,	8,
==================================

<g> ========================
		p1	p2	p3
Values:    5, 7, 8,
========================

<p1> ========================
		p11	p22	p33
Values:    5, 7, 8,
========================

'''
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
