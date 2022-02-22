import networkx as nx
from numpy.random import normal,choice
from collections import defaultdict

class RoadNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()
        # this data structure is for storing pre-computed shortest
        # paths for all pairs of nodes, the keys are
        # [origin][destination] and the values are node lists
        self.shortPath = defaultdict(lambda: defaultdict())
        self.pathDuration = defaultdict(lambda: defaultdict())

    def initGrid(self,numX,numY,meanTime = 1,stddev = 0.01):
        # numX and numY is the number of links in the X and Y
        # directions; link traversal times are drawn at random from a
        # Normal distribution; meanTime is the mean link traversal
        # time stddev is the std deviation of the link traversal time

        # node ID is 'i-j' where i \in [0:numX] and j \in [0:numY]

        # add horizontal links
        for j in range(1,numY + 1):
            for i in range(1,numX):
                # add forward and reverse links with the same
                # traversal time
                traversalTime = abs(normal(meanTime,stddev))
                A = f'{i}-{j}'
                B = f'{i+1}-{j}'
                self.graph.add_edge(A,B,traversal = traversalTime)
                self.graph.add_edge(B,A,traversal = traversalTime)

        # add vertical links
        for i in range(1,numX + 1):
            for j in range(1,numY):
                traversalTime = abs(normal(meanTime,stddev))
                A = f'{i}-{j}'
                B = f'{i}-{j+1}'
                self.graph.add_edge(A,B,traversal = traversalTime)
                self.graph.add_edge(B,A,traversal = traversalTime)

        # compute the shortest paths for all pairs of nodes
        paths = nx.shortest_path(self.graph)
        for orig,destDict in paths.items():
            for dest,path in destDict.items():
                # make a route object, calc times and save
                self.shortPath[orig][dest] = path
                self.pathDuration[orig][dest] = self.calcDuration(path)
                
    def randomNode(self):
        return choice(self.graph.nodes)

    def nextNodeOnPathFromTo(self,origin,destination):
        if origin == destination:
            return None
        path = self.shortPath[origin][destination]
        return path[1]

    def calcDuration(self,path):
        orig = path[0]
        time = 0.
        for dest in path[1:]:
            time += self.graph[orig][dest]['traversal']
            orig = dest

        return time
        
