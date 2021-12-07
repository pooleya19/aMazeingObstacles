import pygame
from pygame.locals import *
import sys
import pyautogui
import time

from Button import Button
from Text import Text
from Graph import *
from SolvingAlgorithms import dijkstra
from BellmanFord import BellmanFord

class Display:
    def __init__(self):
        pygame.init()
        self.buttons = []
        self.texts = []
        self.maze = None
        self.activeFloor = 0
        self.graph = None

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

        self.renderingDijsktra = False
        self.dijkstraSolution = None
        self.renderingBellmanFord = False
        self.bellmanFordSolution = None

    def renderBackground(self):
        self.screen.blit(self.background, (0,0))

    def createObjects(self):
        self.buttons.append(Button("Generate Maze",50,(200,200),self.button_generateMaze))
        self.buttons.append(Button("Set Dimensions",30,(200,270),self.button_setDimensions))
        self.buttons.append(Button("Up",30,(700,630),self.button_floorUp))
        self.buttons.append(Button("Down", 30, (700, 690), self.button_floorDown))
        self.buttons.append(Button("Solve: Dijkstra", 30, (200, 400), self.button_solveDijkstra))
        self.buttons.append(Button("Solve: Bellman Ford", 30, (200, 460), self.button_solveBellmanFord))

        self.texts.append(Text("aMazeing Obstacles", 50, (230,40)))
        self.floorCounter = Text("Floor: 0", 30, (700,580))
        self.texts.append(self.floorCounter)
        self.processing = Text("Processing...",30,(1070,780))

        self.colorDict = {"Water":(0,0,255),
                          "Conveyor Belt":(255,178,102),
                          "Glue":(255,255,51),
                          "Ice":(153,255,255),
                          "Minotaur":(255,0,0),
                          "Path":(255,255,255),
                          "Ladder":(0,0,0)}


    def setupMaze(self):
        self.mazeBorderThick = 5
        self.mazePos = (650,50)
        self.mazeSize = (500,500)
        self.mazeBorder = self.makeSurface((self.mazeSize[0] + 2 * self.mazeBorderThick, self.mazeSize[1] + 2 * self.mazeBorderThick),(150, 150, 150))
        self.maze = self.makeSurface(self.mazeSize, (150, 150, 150))
        self.renderedMaze = None
        self.currentMaze = None

        self.rows = 20
        self.columns = 20
        self.floors = 5

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
        self.renderDijkstra()
        self.renderBellmanFord()
        self.drawMaze()
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
                elif(event.key == K_SPACE):
                    self.renderingDijsktra = True
                elif(event.key == K_v):
                    self.renderingBellmanFord = True
            if event.type == KEYUP:
                if(event.key == K_SPACE):
                    self.renderingDijsktra = False
                elif(event.key == K_v):
                    self.renderingBellmanFord = False
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if(button.mouseOver()):
                        button.activate()


    def renderMaze(self):
        if(self.renderedMaze != None):
            if(self.currentMaze == None): self.currentMaze = self.makeSurface(self.renderedMaze.get_size(),(0,0,0))
            self.currentMaze.blit(self.renderedMaze, (0,0))

    def renderDijkstra(self):
        if(self.renderingDijsktra):
            if(self.dijkstraSolution != None):
                self.startNode = 0
                mousePos = (pygame.mouse.get_pos()[0] - self.mazePos[0],pygame.mouse.get_pos()[1] - self.mazePos[1])
                if(0 <= mousePos[0] < self.mazeSize[0] and 0 <= mousePos[1] < self.mazeSize[1]):
                    mouseMazePos = (int(mousePos[0]/self.gridCellSize[0]),int(mousePos[1]/self.gridCellSize[1]))
                    mouseNode = mouseMazePos[0] + mouseMazePos[1]*self.columns + self.activeFloor * self.rows * self.columns

                    (last,lengths) = self.dijkstraSolution
                    currentNode = mouseNode
                    numNodes = 0
                    totalDist = 0
                    while(currentNode != self.startNode):
                        nextNode = last[currentNode]
                        currentPos = ((currentNode % self.columns)*self.gridCellSize[0]+self.gridCellSize[0]/2,int((currentNode%(self.rows*self.columns)) / self.columns)*self.gridCellSize[1]+self.gridCellSize[1]/2)
                        nextPos = ((nextNode % self.columns)*self.gridCellSize[0]+self.gridCellSize[0]/2,int((nextNode%(self.rows*self.columns)) / self.columns)*self.gridCellSize[1]+self.gridCellSize[1]/2)
                        currentNodeFloor = int(currentNode/(self.rows*self.columns))
                        nextNodeFloor = int(nextNode/(self.rows*self.columns))
                        if(currentNodeFloor == self.activeFloor and nextNodeFloor == self.activeFloor):
                            pygame.draw.line(self.currentMaze,(255,0,255),currentPos,nextPos,3)
                        currentNode = nextNode
                        numNodes += 1
                        totalDist += lengths[currentNode]

    def renderBellmanFord(self):
        if(self.renderingBellmanFord):
            if(self.bellmanFordSolution != None):
                self.startNode = 0
                mousePos = (pygame.mouse.get_pos()[0] - self.mazePos[0],pygame.mouse.get_pos()[1] - self.mazePos[1])
                if(0 <= mousePos[0] < self.mazeSize[0] and 0 <= mousePos[1] < self.mazeSize[1]):
                    mouseMazePos = (int(mousePos[0]/self.gridCellSize[0]),int(mousePos[1]/self.gridCellSize[1]))
                    mouseNode = mouseMazePos[0] + mouseMazePos[1]*self.columns + self.activeFloor * self.rows * self.columns

                    (last,lengths) = self.bellmanFordSolution
                    currentNode = mouseNode
                    numNodes = 0
                    totalDist = 0
                    while(currentNode != self.startNode):
                        nextNode = last[currentNode]
                        currentPos = ((currentNode % self.columns)*self.gridCellSize[0]+self.gridCellSize[0]/2,int((currentNode%(self.rows*self.columns)) / self.columns)*self.gridCellSize[1]+self.gridCellSize[1]/2)
                        nextPos = ((nextNode % self.columns)*self.gridCellSize[0]+self.gridCellSize[0]/2,int((nextNode%(self.rows*self.columns)) / self.columns)*self.gridCellSize[1]+self.gridCellSize[1]/2)
                        currentNodeFloor = int(currentNode/(self.rows*self.columns))
                        nextNodeFloor = int(nextNode/(self.rows*self.columns))
                        if(currentNodeFloor == self.activeFloor and nextNodeFloor == self.activeFloor):
                            pygame.draw.line(self.currentMaze,(0,255,0),currentPos,nextPos,3)
                        currentNode = nextNode
                        numNodes += 1
                        totalDist += lengths[currentNode]

    def drawMaze(self):
        self.screen.blit(self.mazeBorder, (self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
        if(self.currentMaze != None):
            self.screen.blit(self.currentMaze, self.mazePos)


    def button_generateMaze(self):
        print("Generate Maze.")
        self.updateProcessing()
        startTime = time.time()
        self.graph = createRandomGraph(self.rows, self.columns, self.floors)
        elapsedTime = time.time() - startTime
        alertMsg = "Generated " + str(self.rows) + "x" + str(self.columns) + "x" + str(self.floors) + " Maze\nElapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(alertMsg)
        pyautogui.alert(text=alertMsg,title="Maze Generation Algorithm Runtime")
        print("Edges:", self.graph.getEdgeCount())
        self.preRenderMaze()
        self.dijkstraSolution = None
        self.bellmanFordSolution = None

    def preRenderMaze(self):
        if(self.graph == None): return
        mazeBrushThickness = 5
        if (self.rows > 50 or self.columns > 50):
            mazeBrushThickness = 2
        mazeNodeSize = (mazeBrushThickness, mazeBrushThickness)
        mazeNode = self.makeSurface(mazeNodeSize, (255, 255, 255))
        gridCellSize = (self.mazeSize[0] / self.columns, self.mazeSize[1] / self.rows)
        self.gridCellSize = gridCellSize
        lineThick = mazeBrushThickness
        lineColor = (255, 255, 255)
        ladderNode = self.makeSurface(mazeNodeSize, (0,0,0))

        self.renderedMaze = pygame.Surface(self.maze.get_size())
        self.renderedMaze.blit(self.maze, (0,0))
        for row in range(0,self.rows):
            for column in range(0,self.columns):
                node1 = column + row*self.columns + self.activeFloor*self.rows*self.columns
                node1Pos = (column * gridCellSize[0] + gridCellSize[0] * 0.5 - 1,
                            row * gridCellSize[1] + gridCellSize[1] * 0.5 - 1)
                edges = self.graph.adjList[node1]
                for node2 in edges.keys():
                    # print(self.graph.adjList[node1][node2].getName())
                    pathName = self.graph.adjList[node1][node2].getName()
                    lineColor = self.colorDict[pathName]
                    node2column = node2 % self.columns
                    node2row = int((node2 % (self.rows*self.columns))/self.columns)
                    node2Pos = (node2column * gridCellSize[0] + gridCellSize[0] * 0.5 - 1,
                                node2row * gridCellSize[1] + gridCellSize[1] * 0.5 - 1)
                    pygame.draw.line(self.renderedMaze, lineColor, node1Pos, node2Pos, lineThick)
        for row in range(0,self.rows):
            for column in range(0,self.columns):
                node1 = column + row*self.columns + self.activeFloor*self.rows*self.columns
                node1Pos = (column * gridCellSize[0] + gridCellSize[0] * 0.5 - mazeNodeSize[0] / 2,
                            row * gridCellSize[1] + gridCellSize[1] * 0.5 - mazeNodeSize[1] / 2)
                self.renderedMaze.blit(mazeNode, node1Pos)
                edges = self.graph.adjList[node1]
                for node2 in edges.keys():
                    node2column = node2 % self.columns
                    node2row = int((node2 % (self.rows*self.columns))/self.columns)
                    if (row == node2row and column == node2column):
                        self.renderedMaze.blit(ladderNode, node1Pos)

    def button_setDimensions(self):
        answer = pyautogui.prompt(text="Enter Dimensions:    [Rows]x[Columns]x[Floors]",title="Set New Maze Dimensions")

        while True:
            if(answer == None):
                #Prompt exited
                break
            else:
                #An answer was given
                firstX = answer.find('x')
                secondX = answer.find('x',firstX+1)
                if(firstX != -1 and secondX != -1):
                    newRowsStr = answer[0:firstX]
                    newColumnsStr = answer[firstX+1:secondX]
                    newFloorsStr = answer[secondX+1:]
                    if(self.isInt(newRowsStr) and self.isInt(newColumnsStr) and self.isInt(newFloorsStr)):
                        newRows = int(newRowsStr)
                        newColumns = int(newColumnsStr)
                        newFloors = int(newFloorsStr)
                        break
            #If while loop gets to here, a bad answer was given
            answer = pyautogui.prompt(text="Incorrect Formatting!\n\nEnter Dimensions:    [Rows]x[Columns]x[Floors]",title="Set New Maze Dimensions")
        if(answer != None):
            self.rows = newRows
            self.columns = newColumns
            self.floors = newFloors
            print("Set New Maze Dimensions: (",self.rows,",",self.columns,",",self.floors,")",sep='')

    def button_floorUp(self):
        self.activeFloor += 1
        if(self.activeFloor >= self.floors): self.activeFloor = self.floors-1
        self.preRenderMaze()
        self.floorCounter.text = "Floor: " + str(self.activeFloor)
        self.floorCounter.preRender()
        print("Viewing Floor",self.activeFloor)

    def button_floorDown(self):
        self.activeFloor -= 1
        if(self.activeFloor <= 0): self.activeFloor = 0
        self.preRenderMaze()
        self.floorCounter.text = "Floor: " + str(self.activeFloor)
        self.floorCounter.preRender()
        print("Viewing Floor",self.activeFloor)

    def button_solveDijkstra(self):
        if(self.graph == None): return
        print("Solving Maze using Dijkstra's Algorithm")
        self.updateProcessing()
        self.startNode = 0
        startTime = time.time()
        (last, lengths) = dijkstra(self.graph,self.startNode, self.updateProcessing)
        elapsedTime = time.time() - startTime
        elapsedTimeMsg = "Elapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(elapsedTimeMsg)
        pyautogui.alert(text=elapsedTimeMsg,title="Dijkstra's Algorithm Runtime")
        self.dijkstraSolution = (last,lengths)

    def button_solveBellmanFord(self):
        if(self.graph == None): return
        print("Solving Maze using Bellman Ford's Algorithm")
        self.updateProcessing()
        self.startNode = 0
        startTime = time.time()
        (last, lengths) = BellmanFord(self.graph, self.startNode, self.rows, self.columns, self.floors, self.updateProcessing)
        elapsedTime = time.time() - startTime
        elapsedTimeMsg = "Elapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(elapsedTimeMsg)
        pyautogui.alert(text=elapsedTimeMsg,title="Bellman Ford's Algorithm Runtime")
        self.bellmanFordSolution = (last,lengths)

    def updateProcessing(self, percent=-1):
        percent = int(percent)
        self.processing.text = "Processing..."
        if(percent != -1): self.processing.text += str(percent) + "%"
        self.processing.preRender()
        print(self.processing.text)
        self.processing.render(self.screen, True)

    def isInt(self, inputString):
        try:
            int(inputString)
            return True
        except ValueError:
            return False

    def quit(self):
        print("Attempted Quit")
        pygame.quit()
        sys.exit()