from domain import *
from search import *
import sys

# Tole je povecanje max dovoljene rekurzije
sys.setrecursionlimit(10000)

def parseMatrixFile(path: str):
    matrika = []
    with open(path) as f:
        for line in f.readlines():
            matrika.append([int(st) for st in line.split(',')])
    return matrika

def main(path=None, SearcherClass=None, iterate=False, log=False):
    matrika = parseMatrixFile(path)
    labirint = Labirint(matrika)
    iskalec = SearcherClass(labirint.start)
    labirint.enter(iskalec)

    labirint.printNodeMap(log=log)

    if iterate:
        input("Press enter to continue... ")

    while iskalec.move(log=log):
        labirint.printNodeMap(log=log)
        if iterate:
            input("Press enter to continue... ")

    iskalec.report()

if __name__ == '__main__':
    for i in range(1,16):
        # main(f"labyrinths/demo.txt", DijkstraSearcher, iterate=True, log=True)
        main(f"labyrinths/labyrinth_{i}.txt", DepthFirstSearcer, iterate=False, log=False)
        main(f"labyrinths/labyrinth_{i}.txt", BreathFirstSearcher, iterate=False, log=False)
        main(f"labyrinths/labyrinth_{i}.txt", DijkstraSearcher, iterate=False, log=False)




