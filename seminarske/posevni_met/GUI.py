import sys
from math import tan, cos, sin

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget

import pyqtgraph as pg

m = 0.4
g = 9.81
r = 0.1
Cv = 0.47
rho = 1.2
pi = 3.146

def upor(v): #Zaviralni pospesek vetra
    return (- 1/2 * Cv * rho * v**2 * pi * r**2)/m

def simulacija_meta(dt, vx0, vy0, x0, y0):
    '''
    Izračun diferencialne enačbe leta izstrelka z upoštevanjem zračnega upora.
    Funkcija vrne vrednosti x in y koordinat izstrelka med letom vektorja hitrosti v smeri x in y ter časovne vrednosti
    pri koraku dt. Reševanje diferencialne enačbe zaključimo, ko je višina izstrelka negativna.

    Argumenti:

    dt:  korak časa, ki ga iteracija uporabi za nov izračun
    vx0: začetna hitrost v x smeri
    vy0: začetna hitrost v y smeri
    x0:  začetna vrednost x (začnemo v izhodišču koordinatnega sistema)
    y0:  začetna vrednost y (začnemo v izhodišču koordinatnega sistema)


    '''

    # Lista izracunov
    vx = [vx0]
    vy = [vy0]
    x = [x0]
    y = [y0]
    t = [0]

    # Numericno resevanje
    while True:
        alfa = tan(vy[-1]/vx[-1]) # Naklon smeri hitrosti
        v = (vx[-1]**2 + vy[-1]**2)**0.5 # Vsota vektorja hitrosti
        u = upor(v) # Izracun upora vetra
        uX = u*cos(alfa) # Upor po x
        uY = u*sin(alfa) # Upor po y
        vx.append(vx[-1] + uX*dt) # Izracun nove hitrosti vetra po x
        vy.append(vy[-1] -g*dt + uY*dt) # Izracun nove hitrosti vetra po y
        x.append(x[-1] + vx[-1]*dt) # Izracun novih kordinat
        y.append(y[-1] + vy[-1]*dt) # Izracun novih kordinat
        t.append(t[-1]+dt)
        if y[-1]<0:
            return t, x, y, vx, vy


class Slider(QWidget):
    def __init__(self, minimum, maximum, text, parent=None):
        super(Slider, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label_title = QLabel(self)
        self.label_title.setText(text)
        self.verticalLayout.addWidget(self.label_title)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.minimum = minimum
        self.maximum = maximum
        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
                self.maximum - self.minimum)
        self.label.setText("{0:.4g} m/s".format(self.x))


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.horizontalLayout = QHBoxLayout(self)

        self.w4 = Slider(100, 200, "Vy")
        self.w3 = Slider(500, 2000, "Vx")
        self.horizontalLayout.addWidget(self.w4)
        self.horizontalLayout.addWidget(self.w3)

        self.win = pg.GraphicsWindow(title="Prikaz meta z uporom")
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot()
        self.p6.showGrid(x = True, y = True)
        self.p6.setRange(xRange=[0,220], yRange=[0,38])
        self.curve = self.p6.plot(pen='r')
        self.update_plot()

        self.w4.slider.valueChanged.connect(self.update_plot)
        self.w3.slider.valueChanged.connect(self.update_plot)

    def update_plot(self):
        vy0 = self.w4.x
        vx0 = self.w3.x
        tN, x, y, vxN,vyN = simulacija_meta(0.001, vx0, vy0, 0, 0)
        self.p6.setLabel('left', f"višina [m] ({round(max(y),1)} m)")# units='A')
        self.p6.setLabel('bottom', f"domet [m] ({round(max(x), 1)} m)") #, units='s')
        self.p6.setTitle(f"Posevni met z uporom (cas potovanja = {round(tN[-1],1)} s)")
        self.curve.setData(x, y)

def main():
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
