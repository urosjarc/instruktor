import time

from PyQt5.QtGui import QPixmap
import timeit

from src.utils import *
from PyQt5 import QtWidgets, uic, QtGui, Qt, QtCore
from src.domain import *
from pathlib import Path
import cv2

def recognizeTemplate(img_original, img_template_path, methodName) -> MatchResult:
    img_template = cv2.imread(str(img_template_path))
    result = MatchResult(0, img_original, img_template_path, methodName, None)

    image = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY) # pretvorim sliko v sivo ozadje
    template = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY) # enako za template
    method = getattr(cv2, methodName) # methodo iz stringa

    w, h = template.shape[::-1] # sirino in visino templejta

    # Apply template Matching
    res = cv2.matchTemplate(image,template,method) # izvede se matching
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) #  izvede iskanje min/max

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        result.matching = 1-min_val
    else:
        top_left = max_loc
        result.matching = max_val

    bottom_right = (top_left[0] + w, top_left[1] + h)
    result.rectangle = (top_left, bottom_right) # ((x1, y1),(x1, y1))

    return result

class TrainingSet:
    def __init__(self, path: str, anotationPath: str):
        self.path = Path(path).resolve()
        self.anotationFile = self.path.joinpath(anotationPath)

        self.trainingImgs: List[TrainingImg] = [] # primer 00897.ppm
        self.signs: List[Sign] = [] # primer 00/00001.ppm (slika znaka)

        self.__init()

    def __init(self):
        # TUKAJ NAFILAM SLIKE ZNAKOV V self.signs
        for path in self.path.iterdir():
            if path.is_dir():
                sign = Sign(path.name) # Nova slika znaka
                for imgFile in path.iterdir():
                    sign.templates.append(imgFile) # Navilam templatese znaka
                self.signs.append(sign) # Dodam v zbirko znakov

        # Sparsam iz gt.txt (vse anotatione)
        imgAnotations = {} # primer nafilanega imgAnotations['00019.ppm'] = List[Anotations]
        with self.anotationFile.open() as file:
            for line in file.readlines():
                lineArr = line.split(';')
                imgFile = lineArr[0]
                anotation = Anotation(*lineArr[1:]) # *(leftCol, topRow, rightCol, bottomRow, classID)
                if imgFile not in imgAnotations:
                    imgAnotations[imgFile] = [anotation]
                else:
                    imgAnotations[imgFile].append(anotation)

        for imgFile, anotations in imgAnotations.items():
            trainingImg = TrainingImg(self.path.joinpath(imgFile), anotations)
            self.trainingImgs.append(trainingImg)

    def findSign(self, ID):
        for s in self.signs:
            if s.info.id == ID:
                return s

    def getImage(self, imageName):
        for ti in self.trainingImgs:
            if ti.imagePath.name == imageName:
                return ti

    def recognizeImage(self, image, methodName, matchThreshold, callback=None) -> [MatchResult]:
        results = []

        for i, sign in enumerate(self.signs): # iteriram po vseh znakih

            templates: List[str] = sign.templates

            for tmp in templates: # iteriram po templejtih za znak
                callback(round(i/len(self.signs), 2))
                result: MatchResult = recognizeTemplate(image, tmp, methodName)
                result.sign = sign

                # results.append(result)
                # if len(results) == 2:
                #     return results

                if result.matching > matchThreshold:
                    results.append(result)

        callback(1)
        return results

# https://stackoverflow.com/questions/57204782/show-an-opencv-image-with-pyqt5
class GUI(QtWidgets.QMainWindow):
    def __init__(self, trainingSet: TrainingSet):
        super(GUI, self).__init__()

        self.trainingSet = trainingSet
        self.resultIndex = 0
        self.results = []

        self.__init()

    def __init(self):
        uic.loadUi('app.ui', self)

        # Povezava klika z metodo self.nextResult
        self.nextResultBTN.clicked.connect(self.nextResult)
        self.prevResultBTN.clicked.connect(self.prevResult)

        self.trainingImgCBOX.currentTextChanged.connect(self.trainingImgChanged)
        self.selectCustomImgBTN.clicked.connect(self.selectCustomImg)
        self.matchBTN.clicked.connect(self.match)

        self.trainingImgCBOX.clear()
        for timg in self.trainingSet.trainingImgs:
            self.trainingImgCBOX.addItem(timg.imagePath.name)

    def nextResult(self):
        self.resultIndex += 1

        if self.resultIndex >= len(self.results):
            self.resultIndex = 0

        result = self.results[self.resultIndex]
        self.showResult(result)

    def prevResult(self):
        self.resultIndex -= 1

        if self.resultIndex < 0:
            self.resultIndex = len(self.results) - 1

        result = self.results[self.resultIndex]
        self.showResult(result)

    def selectCustomImg(self):
        # Stack owerflow code :) https://stackoverflow.com/questions/44075694/file-dialog-not-working-with-pyqt5
        dialog = QtWidgets.QFileDialog(self)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setDirectory(getDir(__file__))
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            self.image_path = dialog.selectedFiles()[0]
            self.showImage(self.image_path)
            self.match(showAnotations=True)

    def match(self, showAnotations=False):
        self.numImg = 0
        def callback(value):
            self.matchInfoL.setText(f'Current iteration: {self.numImg}')
            self.numImg += 1
            self.progressBar.setValue(int(value*100))

            # specificno za pyqt5 (da se gui osvezuje)
            self.update()
            self.repaint()

        algo = self.matchingClassCBOX.currentText()
        threshold = self.thresholdSBOX.value()
        t0 = time.clock()
        self.results: List[MatchResult] = self.trainingSet.recognizeImage(self.image, algo, threshold, callback)

        if not showAnotations:
            for r in self.results:
                r.show_anotations = True
        else:
            for r in self.results:
                r.show_anotations = False

        t1 = time.clock() - t0
        tdiff = t1-t0
        # https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
        self.results.sort(key=lambda x: x.matching, reverse=True)
        self.showResult(self.results[0])
        self.matchInfoL.setText(f'Checked {self.numImg} templates in {round(tdiff, 2)} sec... Found {len(self.results)} matches... Iteration speed: {round(tdiff/self.numImg, 5)} sec/template!')

    def trainingImgChanged(self, value):
        if isinstance(value, str):
            img = self.trainingSet.getImage(value)
            value = cv2.imread(img.getImagePath())
        self.showImage(value)

    def showImage(self, image):
        if isinstance(image, str):
            self.image = cv2.imread(image)
            pixmap = QPixmap(image)
            self.imageL.setPixmap(pixmap)
            return

        self.image = image
        image = QtGui.QImage(
            self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        self.imageL.setPixmap(QtGui.QPixmap.fromImage(image))

    def showTemplate(self, image_path):
        pixmap = QPixmap(str(image_path))
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.templateL.setPixmap(pixmap)

    def showResult(self, result: MatchResult):
        img = result.img.copy() # Preprecim da bi se naslikali rectangly od vseh resultov

        # Narise rectangle za anotejsne (z modro)
        if result.show_anotations:
            trainigImg = self.trainingSet.getImage(self.trainingImgCBOX.currentText())
            for ano in trainigImg.anotations:
                rectangle = ((ano.leftCol, ano.topRow), (ano.rightCol, ano.bottomRow))
                img = cv2.rectangle(img, *rectangle, (255, 0, 0), 5)

        # Prikaze rectangle za trenutni aktivni rezultat
        img = cv2.rectangle(img, *result.rectangle, (0, 0, 255), 2)

        self.showImage(img)
        self.showTemplate(result.template_path)

        self.templateInfoL.setText('\n'.join([
            result.sign.info.name,
            f'Matching: {round(result.matching*100, 2)}%',
            f'Method: {result.method}',
            f'Rectangle: {result.rectangle}',
        ]))
