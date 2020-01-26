from pathlib import Path
from typing import *


class SignInfo:
    NAMES = [
        'speed limit 20 (prohibitory)',
        'speed limit 30 (prohibitory)',
        'speed limit 50 (prohibitory)',
        'speed limit 60 (prohibitory)',
        'speed limit 70 (prohibitory)',
        'speed limit 80 (prohibitory)',
        'restriction ends 80 (other)',
        'speed limit 100 (prohibitory)',
        'speed limit 120 (prohibitory)',
        'no overtaking (prohibitory)',
        'no overtaking (trucks) (prohibitory)',
        'priority at next intersection (danger)',
        'priority road (other)',
        'give way (other)',
        'stop (other)',
        'no traffic both ways (prohibitory)',
        'no trucks (prohibitory)',
        'no entry (other)',
        'danger (danger)',
        'bend left (danger)',
        'bend right (danger)',
        'bend (danger)',
        'uneven road (danger)',
        'slippery road (danger)',
        'road narrows (danger)',
        'construction (danger)',
        'traffic signal (danger)',
        'pedestrian crossing (danger)',
        'school crossing (danger)',
        'cycles crossing (danger)',
        'snow (danger)',
        'animals (danger)',
        'restriction ends (other)',
        'go right (mandatory)',
        'go left (mandatory)',
        'go straight (mandatory)',
        'go right or straight (mandatory)',
        'go left or straight (mandatory)',
        'keep right (mandatory)',
        'keep left (mandatory)',
        'roundabout (mandatory)',
        'restriction ends (overtaking) (other)',
        'restriction ends (overtaking (trucks)) (other)'
    ]

    def __init__(self, ID):
        self.id = int(ID)
        self.name = self.NAMES[self.id]
    def __str__(self):
        return f'[ {self.id}\t{self.name} ]'

class Sign:
    def __init__(self, classID):
        self.info = SignInfo(classID)
        self.templates = []
    def __str__(self):
        return str(self.info)

class Anotation:

    def __init__(self, leftCol, topRow, rightCol, bottomRow, classID):
        self.leftCol = leftCol
        self.topRow = topRow
        self.rightCol = rightCol
        self.bottomRow = bottomRow
        self.signInfo = SignInfo(classID)

class TrainingImg:
    def __init__(self, imgPath: Path, anotations):
        self.anotations: List[Anotation] = anotations
        self.imagePath: Path = imgPath
    def getImagePath(self):
        return str(self.imagePath)

class MatchResult:
    def __init__(self, matching, img, template, method, rectangle):
        self.matching = matching
        self.img = img
        self.template = template
        self.method = method
        self.rectangle = rectangle

    def __str__(self):
        return f'Matching: {round(self.matching*100, 2)} ({self.method})'
