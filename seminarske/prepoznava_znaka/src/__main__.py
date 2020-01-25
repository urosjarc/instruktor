from src.app import TrainingSet
from src.domain import *
from src.utils import *

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
# CV_TM_CCORR or CV_TM_CCOEFF
if __name__ == '__main__':
    ts = TrainingSet(TRAINING_SET_PATH, ANOTATION_PATH)
    for i in range(4, 10):
        result = ts.recognizeAnotation(i, RECOGNIZE_METHOD[3], 0.999)
        for r in result:
            ts.plotResult(r)
