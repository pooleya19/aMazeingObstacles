import pygame
from pygame.locals import *
import sys

import Graph
from Button import Button
from Text import Text
from Graph import *

class Display:
    def __init__(self):
        pygame.init()
        self.buttons = []
        self.texts = []
        self.maze = None
        self.activeFloor = 0

    def start(self):
        print("Beginning Program.")
        screenSize = (1200,800)
        self.screen = pygame.display.set_mode(screenSize)
        print("Screen Size:", self.screen.get_size())
        pygame.display.set_caption("Maze Visual")

        self.background = self.makeSurface(self.screen.get_size(), (180,180,180))
        self.renderBackground()

        self.createObjects()
        self.setupMaze()

    def renderBackground(self):
        self.screen.blit(self.background, (0,0))

    def createObjects(self):
        self.buttons.append(Button("Generate Maze",50,(200,200),self.button_GenerateMaze))
        self.texts.append(Text("aMazeing Obstacles", 50, (230,40)))

    def setupMaze(self):
        self.mazeBorderThick = 5
        self.mazePos = (650,150)
        self.mazeSize = (500,500)
        self.mazeBorder = self.makeSurface((self.mazeSize[0] + 2 * self.mazeBorderThick, self.mazeSize[1] + 2 * self.mazeBorderThick),(150, 150, 150))
        self.maze = self.makeSurface(self.mazeSize, (150, 150, 150))
        self.currentMaze = None

        self.rows = 50
        self.columns = 50
        self.floors = 2

    def makeSurface(self, size, rgb):
        surface = pygame.Surface(size)
        surface = surface.convert()
        surface.fill(rgb)
        return surface

    def update(self):
        self.renderBackground()
        self.renderObjects()
        self.handleEvents()
        self.renderMaze()
        pygame.display.update()

    def renderObjects(self):
        for button in self.buttons:
            button.render(self.screen)
        for text in self.texts:
            text.render(self.screen)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    quit()
                elif (event.key == K_SPACE):
                    pass
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if(button.mouseOver()):
                        button.activate()

    def renderMaze(self):
        self.screen.blit(self.mazeBorder, (self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
        if(self.currentMaze != None):
            self.screen.blit(self.currentMaze, self.mazePos)


    def button_GenerateMaze(self):
        mazeBrushThickness = 5
        if (self.rows > 50 or self.columns > 50):
            mazeBrushThickness = 2
        mazeNodeSize = (mazeBrushThickness, mazeBrushThickness)
        mazeNode = self.makeSurface(mazeNodeSize, (255, 255, 255))
        gridCellSize = (self.mazeSize[0] / self.columns, self.mazeSize[1] / self.rows)
        lineThick = mazeBrushThickness
        lineColor = (255, 255, 255)

        print("Generate Maze.")
        graph = createRandomGraph(self.rows, self.columns, self.floors)
        print("Edges:",graph.getEdgeCount())

        self.currentMaze = pygame.Surface(self.maze.get_size())
        self.currentMaze.blit(self.maze, (0,0))
        for row in range(0,self.rows):
            for column in range(0,self.columns):
                node1Pos = (column * gridCellSize[0] + gridCellSize[0] * 0.5 - mazeNodeSize[0] / 2,
                            row * gridCellSize[1] + gridCellSize[1] * 0.5 - mazeNodeSize[1] / 2)
                self.currentMaze.blit(mazeNode, node1Pos)
                print(node1Pos)
                node1 = column + row*self.columns + self.activeFloor*self.rows*self.columns
                node1Pos = (column * gridCellSize[0] + gridCellSize[0] * 0.5,
                            row * gridCellSize[1] + gridCellSize[1] * 0.5)
                edges = graph.adjList[node1]
                for node2 in edges.keys():
                    node2column = node2 % self.columns
                    node2row = int((node2 % (self.rows*self.columns))/self.columns)
                    node2Pos = (node2column * gridCellSize[0] + gridCellSize[0] * 0.5,
                                node2row * gridCellSize[1] + gridCellSize[1] * 0.5)
                    pygame.draw.line(self.currentMaze, lineColor, node1Pos, node2Pos, lineThick)

    def quit(self):
        print("Attempted Quit")
        pygame.quit()
        sys.exit()