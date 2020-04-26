from PyQt5.QtCore import QEventLoop, QTimer
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
        self.pixmap = []
        self.pixmap_end = []
        self.pixmap1_done = False

        self.image1PB.clicked.connect(self.selectImg1)
        self.image2PB.clicked.connect(self.selectImg2)

        self.imageL.mousePressEvent = self.startingPosition
        self.imageL.mouseReleaseEvent = self.endingPosition

        self.selectImg1()
        self.show()

    def selectImg1(self):
        self.pixmap.append(QPixmap('../data/slika1.png'))
        self.imageL.setPixmap(self.pixmap[-1])
        self.resizeWindow(self.pixmap[-1].width(), self.pixmap[-1].height())

    def selectImg2(self):
        self.pixmap.append(QPixmap('../data/slika1R.png'))
        self.imageL.setPixmap(self.pixmap[-1])
        self.resizeWindow(self.pixmap[-1].width(), self.pixmap[-1].height())

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
        deg = math.degrees(math.acos((V1x*V2x + V1y*V2y)/(V1len*V2len)))

        if len(self.pixmap_end) == 0:
            self.makeEndPixmap(deg)
            self.drawImage()
            self.sleep()
            self.selectImg2()
        else:
            self.makeEndPixmap(deg)
            self.drawImage()
            self.sleep()
            self.merge()

    def drawImage(self):
        self.imageL.setPixmap(self.pixmap_end[-1])
        self.resizeWindow(900,900)

    def makeEndPixmap(self, d):
        p = self.pixmap[-1]
        siz = 600
        pixmap3=QPixmap(siz,siz)
        pixmap3.fill(QColor("transparent"))
        painter= QPainter(pixmap3)
        painter.drawPixmap(siz/2-self.startingClick[-1][0], siz/2-self.startingClick[-1][1], p)
        painter.end()
        tran = QTransform()
        tran.rotate(d)
        pixmap3 = pixmap3.transformed(tran)
        self.pixmap_end.append(pixmap3)

    def sleep(self):
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()

    def merge(self):
        pixmap3=QPixmap(900,900)
        pixmap3.fill(QColor("transparent"))
        painter= QPainter(pixmap3)
        for i, p in enumerate(self.pixmap_end):
            painter.drawPixmap(0,0, p.width(), p.height(), p)
        painter.end()

        self.imageL.setPixmap(pixmap3)
        self.resizeWindow(pixmap3.width(), pixmap3.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())