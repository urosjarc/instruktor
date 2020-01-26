from src.app import *
from src.utils import *
import sys
from PyQt5 import QtWidgets


TRAINING_SET_PATH = getDir(__file__, '../FullIJCNN2013')
ANOTATION_PATH = 'gt.txt'

if __name__ == '__main__':
    ts = TrainingSet(TRAINING_SET_PATH, ANOTATION_PATH)

    app = QtWidgets.QApplication(sys.argv)
    window = GUI(ts)
    window.show()
    sys.exit(app.exec_())
