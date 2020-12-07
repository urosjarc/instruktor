from typing import List
from statistics import stdev

class Node:
    def __init__(self, x, y, distance, isStart=False, isEnd=False):
        self.connections: List[Node] = []
        self.distances: int = distance
        self.isStart = distance == Labirint.start_num
        self.isEnd = distance == Labirint.end_num
        self.x = x
        self.y = y

    def __str__(self):
        return f"{ 'x' if self.isEnd or self.isStart else self.distances}"#f"{len(self.connections)}"
        # return f"{ 'x' if self.isEnd or self.isStart else f'{self.x},{self.y}'}"#f"{len(self.connections)}"

    def connect(self, node):
        self.connections.append(node)
        node.connections.append(self)

    def isJunction(self) -> bool:
        if self.isStart or self.isEnd:
            return len(self.connections) > 1
        else:
            return len(self.connections) > 2

class Labirint:
    start_num = -2
    end_num = -3
    wall_num = -1

    def __init__(self, point_map: List[List[int]]):
        self.point_map = point_map
        self.node_map: List[List[Node]] = []

        self.searcher: Searcher
        self.start: Node
        self.end: Node

        self.initNodeMap()

    def initNodeMap(self):

        # USTVARI NEPOVEZAN NODE MAP + najdi start, end labirinta
        for y in range(len(self.point_map)):
            self.node_map.append([])
            for x in range(len(self.point_map[y])):
                point = self.point_map[y][x]
                node = None
                if point != Labirint.wall_num:
                    node = Node(x, y, point)
                    if node.isStart:
                        self.start = node
                    if node.isEnd:
                        self.end = node

                self.node_map[-1].append(node)

        # POVEZI PO VERTIKALI (dvosmerna povezava)
        for y in range(len(self.node_map)-1):
            for x in range(len(self.node_map[y])):
                node1 = self.node_map[y][x]
                node2 = self.node_map[y+1][x]
                if None not in [node1, node2]:
                    node1.connect(node2)

        # POVEZI PO HORIZONTALI (dvosmerna povezava)
        for y in range(len(self.node_map)):
            for x in range(len(self.node_map[y])-1):
                node1 = self.node_map[y][x]
                node2 = self.node_map[y][x+1]
                if None not in [node1, node2]:
                    node1.connect(node2)

    def printNodeMap(self, log):
        if not log:
            return

        self.searcher.porocilo()
        for l in self.node_map:
            for n in l:
                char = " "
                if n is not None:
                    char = n
                    if n is self.searcher.node:
                        char = self.searcher

                print(char, end=' ')
            print()

    def enter(self, searcher):
        self.searcher = searcher

class Searcher:
    def __str__(self):
        return "O"

    def __init__(self, node, name):
        self.name = name
        self.moves = 0
        self.node: Node = node # Node na katerem je lociran searcher v trenutni iteraciji.
        self.solutions: List[List[Node]] = []

    def report(self):
        print(f"\nSOLUTIONS: {type(self.name)}")
        for i, solution in enumerate(self.solutions):
            distance, ave_distance, stdev_distance, junctions = self.stats(solution)
            print(f"\t{i} ... Distance: {distance} ({ave_distance} +- {stdev_distance}), Moves: {len(solution)-1}, Junctions: {junctions}")
            print(f"\t    ... Path: {[f'{node.distances}*({node.x}, {node.y})' for node in solution]}")

    def move(self):
        self.moves += 1

    def stats(self, nodes: List[Node]):
        distances = [] # Distance values
        junctions = 0

        for node in nodes:
            if node.distances > 0:
                distances.append(node.distances)

            if len(node.connections) > 2:
                junctions+=1

        return (sum(distances), round(sum(distances)/len(nodes),1), round(stdev(distances),1), junctions)

