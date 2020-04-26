from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QTransform, QColor, QPainter
from PyQt5 import uic
import sys
import math


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.startingClick = []
        self.pixmap1 = None
        self.pixmap1_done = False
        self.pixmap2 = None

        self.image1PB.clicked.connect(self.selectImg1)
        self.image2PB.clicked.connect(self.selectImg2)

        self.imageL.mousePressEvent = self.startingPosition
        self.imageL.mouseReleaseEvent = self.endingPosition

        self.selectImg1()
        self.show()

    def selectImg1(self):
        self.pixmap1 = QPixmap('../data/slika1.png')
        self.imageL.setPixmap(self.pixmap1)
        self.resizeWindow(self.pixmap1.width(), self.pixmap1.height())
        print("select img 1")

    def selectImg2(self):
        self.pixmap2 = QPixmap('../data/slika1R.png')
        self.imageL.setPixmap(self.pixmap2)
        self.resizeWindow(self.pixmap2.width(), self.pixmap2.height())
        print("select img 2")

    def startingPosition(self , event):
        self.startingClick.append([
            event.pos().x(),
            event.pos().y()
        ])

    def resizeWindow(self, w, h):
        QApplication.processEvents()
        self.resize(w, h)
        QApplication.processEvents()
        self.resize(w, h)
        QApplication.processEvents()

    def endingPosition(self , event):
        # GETTING 2 VECTOR
        V2x = event.pos().x() - self.startingClick[-1][0]
        V2y = event.pos().y() - self.startingClick[-1][1]
        V2len = (V2x**2 + V2y**2) ** 0.5

        # GETTING 1 VECTOR
        V1x = 1
        V1y = 0
        V1len = (V1x**2 + V1y**2) ** 0.5

        # CALCULATING DEG
        deg = math.acos((V1x*V2x + V1y*V2y)/(V1len*V2len))

        tra = QTransform()
        # tra.translate(-V2x, -V2y)
        # tra.rotate(math.degrees(deg))

        if not self.pixmap1_done:
            self.pixmap1 = self.pixmap1.transformed(tra)
            self.pixmap1_done = True
            self.selectImg2()
        else:
            self.pixmap2 = self.pixmap2.transformed(tra)
            self.merge()

    def merge(self):
        pixmap3=QPixmap(self.pixmap2.width()*2, self.pixmap2.height()*2)
        pixmap3.fill(QColor("transparent"))
        painter= QPainter(pixmap3)
        dx = self.startingClick[1][0] - self.startingClick[0][0]
        dy = self.startingClick[1][1] - self.startingClick[0][1]
        painter.drawPixmap(-dx, -dy, self.pixmap2.width(), self.pixmap2.height(), self.pixmap2)
        painter.drawPixmap(0,0, self.pixmap1.width(), self.pixmap1.height(), self.pixmap1)
        painter.end()

        self.imageL.setPixmap(pixmap3)
        self.resizeWindow(pixmap3.width(), pixmap3.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())