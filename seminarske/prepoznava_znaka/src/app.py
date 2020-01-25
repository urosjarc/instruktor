from typing import *
from matplotlib import pyplot as plt
from .domain import *
from pathlib import Path
import cv2

class TrainingSet:
    def __init__(self, path: str, anotationPath: str):
        self.path = Path(path).resolve()
        self.anotationPath = self.path.joinpath(anotationPath)

        self.anotations: List[Anotation] = []
        self.signs: List[Sign] = []

        self.__init()

    def __init(self):
        with self.anotationPath.open() as file:
            for line in file.readlines():
                lineArr = line.split(';')
                lineArr[0] = self.path.joinpath(lineArr[0])
                self.anotations.append(Anotation(*lineArr))

        for path in self.path.iterdir():
            if path.is_dir():
                sign = Sign(path.name)
                for imgPath in path.iterdir():
                    sign.templates.append(cv2.imread(str(imgPath), cv2.IMREAD_GRAYSCALE))
                self.signs.append(sign)

    def findSign(self, ID):
        for s in self.signs:
            if s.cls.id == ID:
                return s

    def test_recognizeAnotation(self, index, methodName) -> [Anotation, MatchResult]:
        anotation: Anotation = self.anotations[index]
        image = cv2.imread(anotation.getImagePath(), 0)

        templates = self.findSign(anotation.cls.id).templates

        maxResult = Recognitor.recognizeTemplate(image, templates[0], methodName)
        for tmp in templates[1:]:
            result = Recognitor.recognizeTemplate(image, tmp, methodName)
            if result.matching > maxResult.matching:
                maxResult = result
        return maxResult

    def recognizeAnotation(self, index, methodName, matching) -> [Anotation, MatchResult]:
        results = []
        anotation: Anotation = self.anotations[index]

        for i, sign in enumerate(self.signs):
            print(round(i*100/len(self.signs), 2))
            image = cv2.imread(anotation.getImagePath(), cv2.IMREAD_GRAYSCALE)
            templates = sign.templates

            maxResult = Recognitor.recognizeTemplate(image, templates[0], methodName)
            for tmp in templates[1:]:
                result = Recognitor.recognizeTemplate(image, tmp, methodName)
                if result.matching > maxResult.matching:
                    maxResult = result
            if maxResult.matching >= matching:
                results.append(maxResult)

        return results

    @classmethod
    def plotResult(cls, matchResult: MatchResult):
        plt.subplot(121)
        plt.imshow(matchResult.template)
        plt.title('Anotation'), plt.xticks([]), plt.yticks([])
        plt.subplot(122)
        plt.imshow(matchResult.img)
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(f'{matchResult.method} => {matchResult.matching}%')
        plt.show()

class Recognitor:

    @classmethod
    def recognizeTemplate(cls, img_original, template, methodName) -> MatchResult:
        matching = None
        w, h = template.shape[::-1]
        method = getattr(cv2, methodName)
        img = img_original.copy()

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            matching = min_val
        else:
            top_left = max_loc
            matching = max_val

        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 0, 2)
        return MatchResult(matching, img, template, methodName)
