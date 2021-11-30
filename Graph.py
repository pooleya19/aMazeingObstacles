class Graph:
    def __init__(self):
        self.adjList = {} # the dictionary that stores [node being pointed to, weight] at the key node that points
        self.values = []  # the "map" that stores what values have already been added

# used https://www.pythonpool.com/adjacency-list-python/ as reference
    def add_edge(self, node1, node2, weight):
        # first node is the node that points to the second node with value of weight
        temp = []

        if node1 not in self.values and node2 not in self.values:
            # if neither node exists
            self.adjList[node1] = None
            self.adjList[node2] = None

            self.values.append(node1)
            self.values.append(node2)

            temp.append([node2, weight])
            self.adjList[node1] = temp

        elif node2 not in self.values:
            # if the first node exist but not the second
            self.adjList[node2] = None
            self.values.append(node2)

            # in this case, the first node can already have pre-existing values so we account for that here
            temp.extend(self.adjList[node1])
            temp.append([node2, weight])
            self.adjList[node1] = temp

        elif node1 not in self.values:
            # second node exists but not the first
            self.adjList[node1] = None
            self.values.append(node1)

            temp.append([node2, weight])
            self.adjList[node1] = temp

        else:
            temp.extend(self.adjList[node1])
            temp.append([node2, weight])
            self.adjList[node1] = temp

    def add_node(self, node): # this function may be useless but I'll add it anyways
        # making sure to use an if statement to prevent adding a node that exists
        if node not in self.values:
            self.adjList[node] = None
            self.values.append(node)
