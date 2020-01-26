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

    image = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY)
    method = getattr(cv2, methodName)

    w, h = template.shape[::-1]

    # Apply template Matching
    res = cv2.matchTemplate(image,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        result.matching = 1-min_val
    else:
        top_left = max_loc
        result.matching = max_val

    bottom_right = (top_left[0] + w, top_left[1] + h)

    result.rectangle = (top_left, bottom_right)
    return result

class TrainingSet:
    def __init__(self, path: str, anotationPath: str):
        self.path = Path(path).resolve()
        self.anotationFile = self.path.joinpath(anotationPath)

        self.trainingImgs: List[TrainingImg] = []
        self.signs: List[Sign] = []

        self.__init()

    def __init(self):
        for path in self.path.iterdir():
            if path.is_dir():
                sign = Sign(path.name)
                for imgFile in path.iterdir():
                    sign.templates.append(imgFile)
                self.signs.append(sign)

        imgAnotations = {}
        with self.anotationFile.open() as file:
            for line in file.readlines():
                lineArr = line.split(';')
                imgFile = lineArr[0]
                anotation = Anotation(*lineArr[1:])
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

    def recognizeImage(self, image, methodName, matching, callback=None) -> [MatchResult]:
        results = []

        for i, sign in enumerate(self.signs):

            templates: List[str] = sign.templates

            for tmp in templates[1:]:
                callback(round(i/len(self.signs), 2))
                result = recognizeTemplate(image, tmp, methodName)
                result.sign = sign

                # results.append(result)
                # if len(results) == 2:
                #     return results

                if result.matching > matching:
                    results.append(result)

        callback(1)
        return results

class GUI(QtWidgets.QMainWindow):
    def __init__(self, trainingSet: TrainingSet):
        super(GUI, self).__init__()

        self.trainingSet = trainingSet
        self.resultIndex = 0
        self.results = []

        self.__init()

    def __init(self):
        uic.loadUi('app.ui', self)

        self.nextResultBTN.clicked.connect(self.nextResult)
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

    def selectCustomImg(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setDirectory(getDir(__file__))
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            self.showImage(cv2.imread(dialog.selectedFiles()[0]))

    def match(self):

        self.numImg = 0
        def callback(value):
            self.matchInfoL.setText(f'Current iteration: {self.numImg}')
            self.numImg += 1
            self.progressBar.setValue(int(value*100))
            self.update()
            self.repaint()

        algo = self.matchingClassCBOX.currentText()
        t0= time.clock()
        self.results: List[MatchResult] = self.trainingSet.recognizeImage(self.image, algo, 0.90, callback)
        t1 = time.clock() - t0
        tdiff = t1-t0
        self.showResult(self.results[0])
        self.matchInfoL.setText(f'Checked {self.numImg} images in {round(tdiff, 2)} sec. Iteration speed: {round(tdiff/self.numImg, 5)} sec/template!')

    def trainingImgChanged(self, value):
        if isinstance(value, str):
            img = self.trainingSet.getImage(value)
            value = cv2.imread(img.getImagePath())
        self.showImage(value)

    def showImage(self, image):
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
        trainigImg = self.trainingSet.getImage(self.trainingImgCBOX.currentText())

        img = result.img.copy()

        for ano in trainigImg.anotations:
            rectangle = ((ano.leftCol, ano.topRow), (ano.rightCol, ano.bottomRow))
            img = cv2.rectangle(img, *rectangle, (255, 0, 0), 5)

        img = cv2.rectangle(img, *result.rectangle, (0, 0, 255), 2)

        self.showImage(img)
        self.showTemplate(result.template_path)

        self.templateInfoL.setText('\n'.join([
            result.sign.info.name,
            f'Matching: {round(result.matching*100, 2)}%',
            f'Method: {result.method}',
            f'Rectangle: {result.rectangle}',
        ]))
