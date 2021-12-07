from Graph import *
import sys

# used https://www.geeksforgeeks.org/bellman-ford-algorithm-dp-23/ and
# https://www.youtube.com/watch?v=FtN3BYH2Zes&ab_channel=AbdulBari to learn how this algorithm works
def BellmanFord(graph, node1, rows, columns, floors):
    numOfVerticies = rows * columns * floors
    # numOfEdges = numOfVerticies - 1
    distances = [sys.maxsize] * numOfVerticies

    distances[node1] = 0
    for i in range(0, numOfVerticies - 1):
        for node1 in graph.adjList.keys():
            edges = graph.adjList[node1]
            for node2 in edges.keys():
                currEdge = graph.adjList[node1][node2]
                if distances[node1] != sys.maxsize and distances[node1] + currEdge.getWeight() < distances[node2]:
                    distances[node2] = distances[node1] + currEdge.getWeight()
    # no need to check for negative loops
    return distances


if __name__ == '__main__':
    graph = createRandomGraph(10, 10, 2)
    dist = BellmanFord(graph, 0, 10, 10, 2)

    for int in dist:
        print(int)



