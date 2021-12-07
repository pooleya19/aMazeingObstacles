from Graph import Graph

def dijkstra(graph, start, benchmarkFunc):
    nodeCnt = len(graph.values)
    visited = [False]*nodeCnt
    count = 0
    curr = start
    lengths = [2000000000]*nodeCnt #should be big enough
    lengths[start] = 0
    last = [start]*nodeCnt #last node

    currBenchmark = False
    benchThresh = 100000/nodeCnt

    while count < nodeCnt:
        visited[curr] = True
        toVisit = graph.adjList[curr].keys()
        smallest = 1999999999
        next = 0
        for key in toVisit:
            if lengths[key] > (graph.adjList[curr][key].getWeight() + lengths[curr]):
                lengths[key] = graph.adjList[curr][key].getWeight() + lengths[curr]
                last[key] = curr
        for i in range(nodeCnt):
            if ((not visited[i]) and (lengths[i] <= smallest)):
                next = i
                smallest = lengths[i]
        curr = next
        count += 1

        progress = count/nodeCnt * 100
        readyToBenchmark = (progress%benchThresh) > (benchThresh/2)
        if(readyToBenchmark != currBenchmark):
            if(readyToBenchmark): benchmarkFunc(progress)
            currBenchmark = readyToBenchmark
    benchmarkFunc(100)
    return (last, lengths)
