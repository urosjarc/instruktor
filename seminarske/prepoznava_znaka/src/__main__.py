from src.app import *
from src.utils import *
import sys
from PyQt5 import QtWidgets


TRAINING_SET_PATH = getDir(__file__, '../FullIJCNN2013')
ANOTATION_PATH = 'gt.txt'

RECOGNIZE_METHOD = [
    'TM_CCOEFF',
    'TM_CCOEFF_NORMED',
    'TM_CCORR',
    'TM_CCORR_NORMED',
    'TM_SQDIFF',
    'TM_SQDIFF_NORME'
]

if __name__ == '__main__':
    ts = TrainingSet(TRAINING_SET_PATH, ANOTATION_PATH)

    app = QtWidgets.QApplication(sys.argv)
    window = GUI(ts)
    window.show()
    sys.exit(app.exec_())

# CV_TM_CCORR or CV_TM_CCOEFF
# if __name__ == '__main__':
#     for i in range(4, 10):
#         result = ts.recognizeTrainingImg(i, RECOGNIZE_METHOD[3], 0.999)
#         for r in result:
#             ts.plotResult(r)
