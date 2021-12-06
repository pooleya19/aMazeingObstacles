from Graph import *
import sys

def breadthFirst(graph, node1, node2, rows, columns, floors):
    visited = []
    qValue = []
    q = []
    finalWeights = []
    visited.append(node1)
    qValue.append(0)
    q.append(node1)

    while(len(visited) > 0):
        currIndex = q[0]
        currValue = qValue[0]
        q.pop(0)
        qValue.pop(0)
        if (currIndex == node2):
            finalWeights.append(currValue)

        for keys in graph.adjList.keys():
            edges = graph.adjList[node1]
            for node2 in edges.keys():
                if node2 not in visited:
                    visited.append(node2)
                    q.append(node2)
                    qValue.append(currValue + graph.adjList[node1][node2].getWeight())

    smallestWeight = sys.maxsize
    for int in finalWeights:
        if int < smallestWeight:
            smallestWeight = int

    return smallestWeight
