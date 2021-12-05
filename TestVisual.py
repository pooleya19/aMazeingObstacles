"""
INSTALL PACKAGES WITH PIP
In command prompt:
- Check python version: py --version
- Install pip: py -m pip install --upgrade pip
"""

import pygame
import sys
from pygame.locals import *
from Graph import *
import time
import random

def main():
    print("Beginning Program.")
    screenSize = (1200,800)
    global screen
    screen = pygame.display.set_mode(screenSize)
    print("Size:", screen.get_size())
    pygame.display.set_caption("Maze Visual")

    background = makeSurface(screen.get_size(), (180,180,180))
    screen.blit(background, (0,0))

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    quit()
                elif(event.key == K_SPACE):
                    generateMaze()

def makeSurface(size, rgb):
    surface = pygame.Surface(size)
    surface = surface.convert()
    surface.fill(rgb)
    return surface

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

    rows = 50
    columns = 50

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


    MSTedges = createRandomGraph(10, 10, 1)
    print("MST Length:", len(MSTedges.adjList))
    debugPrint = True
    delay = 0.001
    for MSTedge in MSTedges.adjList:
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

def quit():
    print("Attempted Quit")
    pygame.quit()
    sys.exit()

#Nice to have program start by calling a specific function, rather than just executing code from top
if __name__ == '__main__':
    main()