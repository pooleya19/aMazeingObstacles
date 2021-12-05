import random

class Edge:
    def __init__(self):
        self.weight = -1
        self.name = ""

    def __init__(self, weight, name):
        self.weight = weight
        self.name = name

    def setWeight(self, weight):
        self.weight = weight

    def setName(self, name):
        self.name = name

    def getWeight(self):
        return self.weight

    def getName(self):
        return self.weight

class Graph:
    def __init__(self):
        self.adjList = {} # the dictionary that stores [(node being pointed to, weight)] at the key node that points
        self.values = []  # the "map" that stores what values have already been added

# used https://www.pythonpool.com/adjacency-list-python/ as reference
    def add_edge(self, node1, node2, weight):
        # first node is the node that points to the second node with value of weight

        if node1 not in self.values:
            self.add_node(node1)
        if node2 not in self.values:
            self.add_node(node2)

        currEdge = Edge(weight, "testName")
        self.adjList[node1][node2] = currEdge

    def add_node(self, node): # this function may be useless but I'll add it anyways
        # making sure to use an if statement to prevent adding a node that exists
        if node not in self.values:
            self.adjList[node] = {}
            self.values.append(node)

    def getEdgeCount(self):
        edgeCount = 0
        for node1 in self.adjList.keys():
            edgeCount += len(self.adjList[node1].keys())
        return edgeCount

    def createMinimumSpanningTree(self):
        #Setup lists
        edges = []
        MST = {}
        remaining = {}
        for node in self.adjList.keys():
            remaining[node] = self.adjList[node]

        #Add first node
        firstKey = None
        for key in remaining.keys():
            firstKey = key
            break
        MST[firstKey] = remaining[firstKey]
        remaining.pop(firstKey)

        while(len(remaining) > 0):
            minWeight = 2000000000 #init as large value -> find smallest
            minEdge = (-1,-1)
            toPop = []

            for node1 in MST.keys():
                stillUsable = False
                for node2 in MST[node1].keys():
                    if(remaining.get(node2) != None):
                        stillUsable = True
                        tempEdge = MST[node1][node2]
                        if(tempEdge.getWeight() < minWeight):
                            minWeight = tempEdge.getWeight()
                            minEdge = (node1,node2)
                if(not stillUsable):
                    toPop.append(node1)

            for node in toPop:
                MST.pop(node)

            MST[minEdge[1]] = remaining[minEdge[1]]
            remaining.pop(minEdge[1])
            edges.append(minEdge)

        newGraph = Graph()
        for currEdge in edges:
            newGraph.add_edge(currEdge[0], currEdge[1], -1)
            newGraph.add_edge(currEdge[1], currEdge[0], -1)

        return newGraph


def createRandomGraph(rows, columns, floorNumber):
    graph = Graph()

    for i in range(0, floorNumber):
        tempGraph = Graph()
        maxRand = 10000
        for row in range(0, rows):
            for column in range(0, columns):
                node1 = column + row * columns + rows * columns * floorNumber
                if (row != 0):
                    node2 = node1 - columns
                    weight = random.randrange(0, maxRand)
                    tempGraph.add_edge(node1, node2, weight)
                    tempGraph.add_edge(node2, node1, weight)
                if (row != rows - 1):
                    node2 = node1 + columns
                    weight = random.randrange(0, maxRand)
                    tempGraph.add_edge(node1, node2, weight)
                    tempGraph.add_edge(node2, node1, weight)
                if (column != 0):
                    node2 = node1 - 1
                    weight = random.randrange(0, maxRand)
                    tempGraph.add_edge(node1, node2, weight)
                    tempGraph.add_edge(node2, node1, weight)
                if (column != columns - 1):
                    node2 = node1 + 1
                    weight = random.randrange(0, maxRand)
                    tempGraph.add_edge(node1, node2, weight)
                    tempGraph.add_edge(node2, node1, weight)

        tempGraph = tempGraph.createMinimumSpanningTree()
        graph = combine(graph, tempGraph)

    for node1 in graph.adjList.keys(): # makes the different obstacles
        edges = graph.adjList[node1]
        for node2 in edges.keys():
            edge1 = graph.adjList[node1][node2]
            edge2 = graph.adjList[node2][node1]

            tile = random.randrange(0, 100)
            if (tile < 50):
                edge1.setWeight(20)
                edge1.setName("Path")  # white
                edge2.setWeight(20)
                edge2.setName("Path")
            elif (tile < 60):
                edge1.setWeight(50)
                edge1.setName("Water")  # blue
                edge2.setWeight(50)
                edge2.setName("Water")
            elif (tile < 70):
                edge1.setWeight(5)
                edge1.setName("Conveyor Belt")
                edge2.setWeight(5)
                edge2.setName("Conveyor Belt")
                # grey
            elif (tile < 83):
                edge1.setWeight(35)
                edge1.setName("Glue")
                edge2.setWeight(35)
                edge2.setName("Glue")
                # yellow
            elif (tile < 95):
                edge1.setWeight(10)
                edge1.setName("Ice")
                edge2.setWeight(10)
                edge2.setName("Ice")
                # light blue
            else:
                edge1.setWeight(60)
                edge1.setName("Minotaur")
                edge2.setWeight(60)
                edge2.setName("Minotaur")
                # red


    for i in range(0, floorNumber - 1): # make the ladder
        rand1 = random.randrange(0, rows * columns)
        rand2 = rand1
        while (rand2 == rand1):
            rand2 = random.randrange(0, rows * columns)
        rand1 = rand1 + i * rows * columns
        rand1to = rand1 + rows * columns
        rand2 = rand2 + i * rows * columns
        rand2to = rand2 + rows * columns
        Edge1 = Edge(40, "Ladder")
        Edge2 = Edge(40, "Ladder")
        graph.adjList[rand1][rand1to] = Edge1
        graph.adjList[rand1to][rand1] = Edge1
        graph.adjList[rand2][rand2to] = Edge2
        graph.adjList[rand2to][rand2] = Edge2

    return graph

def combine(Graph1, Graph2):
    Graph1.adjList.update(Graph2.adjList)
    return Graph1
