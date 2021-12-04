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

        self.adjList[node1][node2] = weight

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
                        weight = MST[node1][node2]
                        if(weight < minWeight):
                            minWeight = weight
                            minEdge = (node1,node2)
                if(not stillUsable):
                    toPop.append(node1)

            for node in toPop:
                MST.pop(node)

            MST[minEdge[1]] = remaining[minEdge[1]]
            remaining.pop(minEdge[1])
            edges.append(minEdge)
        return edges