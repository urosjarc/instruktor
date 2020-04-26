from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, \
    QInputDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QTransform, QColor, QPainter
from PyQt5 import uic
import sys
import math


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.startingClick = []
        self.geoReference = []
        self.geoCordinates = []
        self.geoRotate = []

        self.pixmap = []
        self.pixmap_end = []
        self.pixmapMerged = None

        self.imageL.mousePressEvent = self.mouseStartPosition
        self.imageL.mouseReleaseEvent = self.mouseEndPosition

        self.selectImg()
        self.show()

    def selectImg(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '../data/', "Image files (*.jpg *.gif *.png)")
        self.pixmap.append(QPixmap(fname[0]))
        self.imageL.setPixmap(self.pixmap[-1])
        self.resizeWindow(self.pixmap[-1].width(), self.pixmap[-1].height())

    def mouseStartPosition(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)
        if len(self.startingClick) < 3:
            self.startingClick.append([x, y])
        elif len(self.geoReference) < 2:
            print('geo reference')
            self.geoReference.append([x, y])
            self.geoCordinates.append([
                self.getDouble("Set cordinates", "Enter x:"),
                self.getDouble("Set cordinates", "Enter y:")
            ])
        else:
            dXCor = self.geoCordinates[1][0] - self.geoCordinates[0][0]
            dYCor = self.geoCordinates[1][1] - self.geoCordinates[0][1]
            dX = self.geoReference[1][0] - self.geoReference[0][0]
            dY = self.geoReference[1][1] - self.geoReference[0][1]

            XCor = dXCor/dX * (x - self.geoReference[0][0]) + self.geoCordinates[0][0]
            YCor = dYCor/dY * (y - self.geoReference[0][1]) + self.geoCordinates[0][1]

            msg = QMessageBox()
            msg.setWindowTitle("Cordinates")
            msg.setText(f"Chosen cordinates: x={round(XCor,2)} y={round(YCor,2)}")
            msg.exec_()

    def getDouble(self, title, question):
        d, okPressed = QInputDialog.getDouble(self, title, question)
        if okPressed:
            return d

    def mouseEndPosition(self, event):
        if len(self.startingClick) > 3:
            return None

        # GETTING 2 VECTOR
        V2x = event.pos().x() - self.startingClick[-1][0]
        V2y = event.pos().y() - self.startingClick[-1][1]
        V2len = (V2x ** 2 + V2y ** 2) ** 0.5

        # GETTING 1 VECTOR
        V1x = 1
        V1y = 0
        V1len = (V1x ** 2 + V1y ** 2) ** 0.5

        # CALCULATING DEG
        deg = math.degrees(math.acos((V1x * V2x + V1y * V2y) / (V1len * V2len)))

        if len(self.pixmap_end) == 0:
            self.makeEndPixmap(deg)
            self.drawImage()
            self.selectImg()
        elif len(self.startingClick) < 3:
            self.makeEndPixmap(deg)
            self.drawImage()
            self.mergeEndPixmaps()
        else:
            tran = QTransform()
            tran.rotate(deg)
            pix = self.pixmapMerged.transformed(tran)
            self.imageL.setPixmap(pix)

    def drawImage(self):
        self.imageL.setPixmap(self.pixmap_end[-1])
        self.resizeWindow(self.pixmap_end[-1].width(), self.pixmap_end[-1].height())

    def makeEndPixmap(self, d):
        p = self.pixmap[-1]
        pix = QPixmap(p.width() * 2, p.height() * 2)
        pix.fill(QColor("transparent"))
        painter = QPainter(pix)
        painter.drawPixmap(pix.width() / 2 - self.startingClick[-1][0],
                           pix.height() / 2 - self.startingClick[-1][1], p)
        painter.end()
        tran = QTransform()
        tran.rotate(d)
        pix = pix.transformed(tran)
        self.pixmap_end.append(pix)

    def mergeEndPixmaps(self):
        p0 = self.pixmap_end[0]
        p1 = self.pixmap_end[1]
        p = QPixmap(p0.width(), p0.height())
        p.fill(QColor("transparent"))
        painter = QPainter(p)
        painter.drawPixmap(0, 0, p0.width(), p0.height(), p0)
        painter.drawPixmap((p0.width() - p1.width()) // 2, (p0.height() - p1.height()) // 2, p1)
        painter.end()

        self.imageL.setPixmap(p)
        self.resizeWindow(p.width(), p.height())
        self.pixmapMerged = p

    def resizeWindow(self, w, h):
        QApplication.processEvents()
        self.resize(w, h)
        QApplication.processEvents()
        self.resize(w, h)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
