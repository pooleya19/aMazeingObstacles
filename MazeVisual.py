"""
INSTALL PACKAGES WITH PIP
In command prompt:
- Check python version: py --version
- Install pip: py -m pip install --upgrade pip
"""

import pygame
import sys
from pygame.locals import *
import time
import random

from Graph import Graph
from Display import Display

display = Display()

def main():
    display.start()

    while True:
        display.update()

"""
def generateMaze():
    startTime = time.time()
    mazeBorderThick = 5
    mazePos = (650, 150)
    mazeSize = (500, 500)
    mazeBorder = makeSurface((mazeSize[0] + 2 * mazeBorderThick, mazeSize[1] + 2 * mazeBorderThick), (150, 150, 150))
    maze = makeSurface(mazeSize, (150, 150, 150))
    screen.blit(mazeBorder, (mazePos[0] - mazeBorderThick, mazePos[1] - mazeBorderThick))
    screen.blit(maze, mazePos)
    pygame.display.update()

    rows = 5
    columns = 10

    mazeBrushThickness = 5
    if(rows > 50 or columns > 50): mazeBrushThickness = 2
    mazeNodeSize = (mazeBrushThickness, mazeBrushThickness)
    mazeNode = makeSurface(mazeNodeSize, (255, 255, 255))
    gridCellSize = (mazeSize[0] / columns, mazeSize[1] / rows)

    graph = Graph()

    lineThick = mazeBrushThickness
    lineColor = (255, 255, 255)
    maxRand = 10000
    # Generate graph and blit nodes
    #weight = row*row+column*column
    for row in range(0, rows):
        for column in range(0, columns):
            node1Pos = (mazePos[0] + column * gridCellSize[0] + gridCellSize[0] * 0.5 - mazeNodeSize[0] / 2,
                        mazePos[1] + row * gridCellSize[1] + gridCellSize[1] * 0.5 - mazeNodeSize[1] / 2)
            screen.blit(mazeNode, node1Pos)
            node1 = column + row * columns
            if (row != 0):
                node2 = node1 - columns
                weight = random.randrange(0,maxRand)
                graph.add_edge(node1, node2, weight)
                graph.add_edge(node2, node1, weight)
            if (row != rows - 1):
                node2 = node1 + columns
                weight = random.randrange(0,maxRand)
                graph.add_edge(node1, node2, weight)
                graph.add_edge(node2, node1, weight)
            if (column != 0):
                node2 = node1 - 1
                weight = random.randrange(0,maxRand)
                graph.add_edge(node1, node2, weight)
                graph.add_edge(node2, node1, weight)
            if (column != columns - 1):
                node2 = node1 + 1
                weight = random.randrange(0,maxRand)
                graph.add_edge(node1, node2, weight)
                graph.add_edge(node2, node1, weight)

    MSTedges = graph.createMinimumSpanningTree()
    print("MST Length:", len(MSTedges))
    debugPrint = True
    delay = 0.001
    for MSTedge in MSTedges:
        node1 = MSTedge[0]
        node2 = MSTedge[1]
        node1GridPos = (node1 % columns, int(node1 / columns))
        node2GridPos = (node2 % columns, int(node2 / columns))
        node1Pos = (mazePos[0] + node1GridPos[0] * gridCellSize[0] + gridCellSize[0] * 0.5 - 1,
                    mazePos[1] + node1GridPos[1] * gridCellSize[1] + gridCellSize[1] * 0.5 - 1)
        node2Pos = (mazePos[0] + node2GridPos[0] * gridCellSize[0] + gridCellSize[0] * 0.5 - 1,
                    mazePos[1] + node2GridPos[1] * gridCellSize[1] + gridCellSize[1] * 0.5 - 1)
        pygame.draw.line(screen, lineColor, node1Pos, node2Pos, lineThick)
        if (debugPrint):
            pygame.display.update()
            time.sleep(delay)
    print("Generated Maze.")
    print("Elapsed Time:",round(time.time()-startTime,5),"seconds")
"""

#Nice to have program start by calling a specific function, rather than just executing code from top
if __name__ == '__main__':
    main()