from copy import deepcopy
from typing import List, Dict
from domain import Searcher, Node
from math import inf

class DepthFirstSearcer(Searcher):

    def __init__(self, node):
        super().__init__(node, self)
        self.path: List[Node] = [node]
        self.visitedNodes: List[Node] = [node]

    def move(self, log=False):
        super(DepthFirstSearcer, self).move()

        hasMoved = False

        for con in self.node.connections:
            if con not in self.visitedNodes or con.isEnd:
                self.node = con # Premik na dovoljen node
                if con.isEnd:
                    break
                self.path.append(con)
                self.visitedNodes.append(con)
                hasMoved = True
                break

        if self.node.isEnd:
            self.solutions.append(deepcopy(self.path + [self.node])) # Kopiranje trenutno pot v solution.

        if not hasMoved:
            self.path.pop(-1) # Odstrani zadnji element poti
            if len(self.path) == 0:
                return False
            self.node = self.path[-1]

        if log:
            print([str(node) for node in self.path])

        return True

class BreathFirstSearcher(Searcher):
    def __init__(self, node):
        node.history = [node]
        self.queue: List[Node] = [node]
        super().__init__(node, self)

    def move(self, log=False):
        super(BreathFirstSearcher, self).move()

        for node in self.node.connections:
            if node not in self.queue:
                if node.isEnd: # V primeru ce je konekcija konec labirinta, konekcijo obravnavamo kot slepo ulico
                    # Ter dodamo trenutni node history v spisek solutionov.
                    self.solutions.append(self.node.history + [node])
                    continue
                self.queue.append(node)
                node.history = self.node.history + [node] # Dodam history prejsnje tocke v novo najdeno konekcijo...


        if self.moves < len(self.queue): # In ce zmanka cakalne vrste vem da je konec iskanja...
            self.node = self.queue[self.moves]
        else:
            return False

        if log:
            print(f"QUEUE ({len(self.queue)}/{self.moves}) : {[f'{node.x},{node.y}' for node in self.queue]}")

        return True

# https://www.youtube.com/watch?v=pVfj6mxhdMw
class DijkstraSearcher(Searcher):

    class Stats:
        def __init__(self, node: Node, distance: int, prevNode):
            self.node = node
            self.distance = distance
            self.prevNode = prevNode

        def __str__(self):
            return f'{self.node},{self.distance},{self.prevNode}'

    def __init__(self, node):
        self.shortestDistance = {} # Hash map <node>: <Stats>
        self.visited: List[Node] = [node]
        self.unvisited: List[Node] = []
        self.end: Node = None
        self.shortestDistance[node] = DijkstraSearcher.Stats(
            node, 0, None
        )
        super().__init__(node, self)

    def move(self, log=False):
        super(DijkstraSearcher, self).move()

        closestNodeDistance = inf
        closestNode: Node = None
        for node in self.node.connections:
            if node.isEnd:
                self.end = node

            if node.distances < closestNodeDistance and node not in self.visited:
                    closestNode = node
                    closestNodeDistance = node.distances

            prevStat = self.shortestDistance[self.node]
            if node not in self.shortestDistance: # Dodam node v tabelo (dinamicno) ce se ni dodana...
                self.shortestDistance[node] = DijkstraSearcher.Stats(
                    node, node.distances + prevStat.distance, self.node # Dodam node + vsoto prejsnje in trenutne + prejsni node.
                )
            elif self.shortestDistance[node].distance > node.distances + prevStat.distance: # Preverim ce je povezava krajsa od prejsne obiskane razdalije
                self.shortestDistance[node].distance = node.distances + prevStat.distance # Ce je krajsa jo na novo izracunam in pripisem trenutni.
                self.shortestDistance[node].prevNode = self.node

        for node in self.node.connections:
            if closestNode is not node and node not in self.visited:
                self.unvisited.append(node) # Dodam closest node v visited!


        # Preverjanje konca
        if closestNode is None or closestNode.isEnd: # Ce najblizji node ni najden ali ce je najblizji node konec
            if len(self.unvisited) == 0: # Preverim ce je se kaj neobiskanih nodeov.
                self.setShortestPath() # Iscem solution ko se pomikam nazaj po najkrajsi poti.
                return False # Sporocim konec iskanja
            self.node = self.unvisited[-1]
            self.unvisited.pop(-1)
        else:
            self.node = closestNode # Spremenim trenutni node na najblizjega.

        self.visited.append(self.node)

        if log:
            for k, v in self.shortestDistance.items():
                print(f'{k} => {v}')

            print(f"UNVISITED NODES: {[str(n) for n in self.unvisited]}")

        return True

    def setShortestPath(self):
        # Ko najdem konec se pomikam nazaj po najkrajsi poti do starta.
        node = self.end
        solution = [node]
        while not node.isStart:
            node = self.shortestDistance[node].prevNode
            solution.append(node)

        solution.reverse()
        self.solutions.append(solution)








