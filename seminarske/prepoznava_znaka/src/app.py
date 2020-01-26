from typing import *

from PyQt5.QtWidgets import QInputDialog, QMessageBox

from src.utils import *
from PyQt5 import QtWidgets, uic, QtGui
from src.domain import *
from pathlib import Path
import cv2

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
                    sign.templates.append(cv2.imread(str(imgFile)))
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
            callback(round(i/len(self.signs), 2))

            templates = sign.templates
            maxResult = Recognitor.recognizeTemplate(image, templates[0], methodName)

            for tmp in templates[1:]:
                result = Recognitor.recognizeTemplate(image, tmp, methodName)

                if result.matching > maxResult.matching:
                    maxResult = result

            if maxResult.matching >= matching:
                results.append(maxResult)

        callback(1)
        return results

class Recognitor:
    @classmethod
    def recognizeTemplate(cls, img_original, img_template, methodName) -> MatchResult:
        result = MatchResult(0, img_original, img_template, methodName, None)

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
            result.matching = min_val
        else:
            top_left = max_loc
            result.matching = max_val

        bottom_right = (top_left[0] + w, top_left[1] + h)

        result.rectangle = (top_left, bottom_right)
        return result

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
        result = self.results[0]
        try:
            self.resultIndex += 1
        except:
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
        def callback(value):
            self.progressBar.setValue(value*100)
            self.update()

        algo = self.matchingClassCBOX.currentText()
        self.results: List[MatchResult] = self.trainingSet.recognizeImage(self.image, algo, 0.998, callback)
        self.showResult(self.results[0])

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

    def showTemplate(self, image):
        self.template = image
        image = QtGui.QImage(
            self.template.data, self.template.shape[1], self.template.shape[0], QtGui.QImage.Format_RGB888
        ).rgbSwapped()
        self.templateL.setPixmap(QtGui.QPixmap.fromImage(image))

    def showResult(self, result: MatchResult):
        self.showImage(result.img)
        self.showTemplate(result.template)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText('\n'.join([
            f'Matching: {result.matching*100}%',
            f'Method: {result.method}',
            f'Rectangle: {result.rectangle}'
        ]))
        msg.setWindowTitle("Matching result")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
