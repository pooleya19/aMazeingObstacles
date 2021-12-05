from Graph import Graph

def dijkstra(graph, start):
    nodeCnt = len(graph.values)
    visited = [False]*nodeCnt
    count = 0
    curr = start
    lengths = [2000000000]*nodeCnt #should be big enough
    lengths[start] = 0
    last = [start]*nodeCnt #last node
    while count < nodeCnt:
        toVisit = graph.adjList[curr].keys()
        smallest = 1999999999
        next = 0
        for key in toVisit:
            if lengths[key] > (graph.adjList[curr][key] + lengths[curr]):
                lengths[key] = graph.adjList[curr][key] + lengths[curr]
                last[key] = curr
        for i in range(nodeCnt):
            if (not visited[i]) and (lengths[i] <= smallest):
                next = i
                smallest = lengths[i]
        visited[curr] = True
        curr = next
        count += 1
    return lengths
