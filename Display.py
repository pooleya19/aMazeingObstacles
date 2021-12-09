import pygame
from pygame.locals import *
import sys
import pyautogui
import math
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
        self.activeNode = None
        self.currentNode = None
        self.startNode = None
        self.endNode = None

        self.edgeDict = {"Water": ((0, 0, 255), 50),
                         "Conveyor Belt": ((255, 178, 102), 5),
                         "Glue": ((255, 255, 51), 35),
                         "Ice": ((153, 255, 255), 10),
                         "Minotaur": ((255, 0, 0), 60),
                         "Path": ((255, 255, 255), 20),
                         "Ladder": ((0, 0, 0), 40)}

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

        self.renderingDijkstra = False
        self.dijkstraSolution = None
        self.renderingBellmanFord = False
        self.bellmanFordSolution = None
        self.renderBellmanFromActiveNode = False

        self.preRenderLegend()
        self.renderingLegend = False

    def renderBackground(self):
        self.screen.blit(self.background, (0,0))

    def createObjects(self):
        #Button(text, fontSize, center position, function(optional) WITHOUT PARENTHESIS)
        self.buttons.append(Button("Generate Maze",50,(200,200),self.button_generateMaze))
        self.buttons.append(Button("Set Dimensions",30,(200,270),self.button_setDimensions))

        self.buttons.append(Button("Up",30,(700,660),self.button_floorUp))
        self.buttons.append(Button("Down", 30, (700, 720), self.button_floorDown))

        self.buttons.append(Button("Solve: Dijkstra", 30, (200, 450), self.button_solveDijkstra))
        self.buttons.append(Button("Step Through", 30, (200, 510), self.button_stepThroughDijkstra))
        # self.buttons.append(Button("Save GIF", 30, (300, 510), self.button_solveDijkstra))

        self.buttons.append(Button("Solve: Bellman Ford", 30, (200, 650), self.button_solveBellmanFord))
        self.buttons.append(Button("Step Through", 30, (200, 710), self.button_stepThroughBellmanFord))
        # self.buttons.append(Button("Save GIF", 30, (300, 710), self.button_solveBellmanFord))

        self.legendButton = Button("Maze Legend", 30, (1050, 40))
        self.legendButton.setHoverFunctions(self.showLegend, self.hideLegend)
        self.buttons.append(self.legendButton)

        self.buttons.append(Button("Set Start", 30, (540, 160), self.button_setStart))
        self.buttons.append(Button("Set End", 30, (540, 220), self.button_setEnd))

        self.texts.append(Text("aMazeing Obstacles", 60, (250,40)))
        self.floorCounter = Text("Floor: 0", 30, (700,610))
        self.texts.append(self.floorCounter)
        self.processing = Text("Processing...",30,(1070,780))

        self.texts.append(Text("Path: Start->End", 25, (510,440)))
        self.dijkstraNodesTraversed = Text("Nodes Traversed: N/A", 25, (510,480))
        self.texts.append(self.dijkstraNodesTraversed)
        self.dijkstraTotalDifficulty = Text("Total Difficulty: N/A", 25, (510,520))
        self.texts.append(self.dijkstraTotalDifficulty)

        self.texts.append(Text("Path: Start->End", 25, (510, 640)))
        self.bellmanFordNodesTraversed = Text("Nodes Traversed: N/A", 25, (510, 680))
        self.texts.append(self.bellmanFordNodesTraversed)
        self.bellmanFordTotalDifficulty = Text("Total Difficulty: N/A", 25, (510, 720))
        self.texts.append(self.bellmanFordTotalDifficulty)




    def setupMaze(self):
        self.mazeBorderThick = 5
        self.mazePos = (650,80)
        self.mazeSize = (500,500)
        self.mazeBorder = self.makeSurface((self.mazeSize[0] + 2 * self.mazeBorderThick, self.mazeSize[1] + 2 * self.mazeBorderThick),(150, 150, 150))
        self.maze = self.makeSurface(self.mazeSize, (150, 150, 150))
        self.renderedMaze = None
        self.currentMaze = None
        self.activeNode = None

        self.rows = 20
        self.columns = 20
        self.floors = 5

    def preRenderLegend(self):
        self.legendSize = self.mazeSize
        self.legendPos = self.mazePos
        self.legend = self.makeSurface(self.legendSize, (180,180,180))
        title = Text("Path Name     Color     Difficulty", 40, (250,30))
        title.render(self.legend)

        edges = list(self.edgeDict.keys())
        for i in range(0,len(edges)):
            edgeName = edges[i]
            edgeNameText = Text(edgeName,30,(90,80+40*i))
            edgeNameText.render(self.legend)
            pygame.draw.line(self.legend,self.edgeDict[edgeName][0],(240,80+40*i),(290,80+40*i),5)
            edgeDifficulty = Text(str(self.edgeDict[edgeName][1]),40,(420,80+40*i))
            edgeDifficulty.render(self.legend)

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
        self.renderLegend()
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
                elif(event.key == K_d):
                    self.renderingDijkstra = True
                elif(event.key == K_b):
                    self.renderingBellmanFord = True
                elif(event.key == K_f):
                    print("flag")
            if event.type == KEYUP:
                if(event.key == K_d):
                    self.renderingDijkstra = False
                elif(event.key == K_b):
                    self.renderingBellmanFord = False
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if(button.mouseOver()):
                        button.activate()
                mousePos = pygame.mouse.get_pos()
                keyPressed = pygame.mouse.get_pressed()
                if(self.mazePos[0] < mousePos[0] < self.mazePos[0] + self.mazeSize[0] and self.mazePos[1] < mousePos[1] < self.mazePos[1] + self.mazeSize[1] and keyPressed[0]):
                    # checks for left click now
                    self.mouseMazeClick()
                elif(keyPressed[2]): #  Checks for right click
                    self.clearActiveNode()

    def renderMaze(self):
        if(self.renderedMaze != None):
            if(self.currentMaze == None): self.currentMaze = self.makeSurface(self.renderedMaze.get_size(),(0,0,0))
            self.currentMaze.blit(self.renderedMaze, (0,0))

    def renderDijkstra(self):
        if(self.renderingDijkstra):
            if(self.dijkstraSolution != None):
                mousePos = (pygame.mouse.get_pos()[0] - self.mazePos[0],pygame.mouse.get_pos()[1] - self.mazePos[1])
                if(0 <= mousePos[0] < self.mazeSize[0] and 0 <= mousePos[1] < self.mazeSize[1]):
                    mouseMazePos = (int(mousePos[0]/self.gridCellSize[0]),int(mousePos[1]/self.gridCellSize[1]))
                    mouseNode = mouseMazePos[0] + mouseMazePos[1]*self.columns + self.activeFloor * self.rows * self.columns

                    (last,lengths) = self.dijkstraSolution
                    currentNode = mouseNode
                    numNodes = 0
                    totalDist = lengths[mouseNode]
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
        if (self.dijkstraSolution != None):
            (last, lengths) = self.dijkstraSolution
            currentNode = self.endNode
            numNodes = 0
            activeNodeDist = lengths[self.endNode]
            while (currentNode != self.startNode):
                nextNode = last[currentNode]
                currentPos = ((currentNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                              int((currentNode % (self.rows * self.columns)) / self.columns) *
                              self.gridCellSize[1] + self.gridCellSize[1] / 2)
                nextPos = ((nextNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                           int((nextNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                           self.gridCellSize[1] / 2)
                currentNodeFloor = int(currentNode / (self.rows * self.columns))
                nextNodeFloor = int(nextNode / (self.rows * self.columns))
                if (currentNodeFloor == self.activeFloor and nextNodeFloor == self.activeFloor):
                    pygame.draw.line(self.currentMaze, (0, 0, 0), currentPos, nextPos, 3)
                currentNode = nextNode
                numNodes += 1
            newMessage = "Nodes Traversed: " + str(numNodes)
            if(self.dijkstraNodesTraversed.text != newMessage):
                self.dijkstraNodesTraversed.text = newMessage
                self.dijkstraNodesTraversed.preRender()
            newMessage = "Total Difficulty: " + str(activeNodeDist)
            if(self.dijkstraTotalDifficulty.text != newMessage):
                self.dijkstraTotalDifficulty.text = newMessage
                self.dijkstraTotalDifficulty.preRender()
        else:
            newMessage = "Nodes Traversed: N/A"
            if (self.dijkstraNodesTraversed.text != newMessage):
                self.dijkstraNodesTraversed.text = newMessage
                self.dijkstraNodesTraversed.preRender()
            newMessage = "Total Difficulty: N/A"
            if (self.dijkstraTotalDifficulty.text != newMessage):
                self.dijkstraTotalDifficulty.text = newMessage
                self.dijkstraTotalDifficulty.preRender()



    def renderBellmanFord(self):
        if(self.renderingBellmanFord):
            if(self.bellmanFordSolution != None):
                mousePos = (pygame.mouse.get_pos()[0] - self.mazePos[0],pygame.mouse.get_pos()[1] - self.mazePos[1])
                if(0 <= mousePos[0] < self.mazeSize[0] and 0 <= mousePos[1] < self.mazeSize[1]):
                    mouseMazePos = (int(mousePos[0]/self.gridCellSize[0]),int(mousePos[1]/self.gridCellSize[1]))
                    mouseNode = mouseMazePos[0] + mouseMazePos[1]*self.columns + self.activeFloor * self.rows * self.columns

                    (last,lengths) = self.bellmanFordSolution
                    currentNode = mouseNode
                    numNodes = 0
                    totalDist = lengths[mouseNode]
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
        #if(self.renderBellmanFromActiveNode):
        if(self.bellmanFordSolution != None and self.endNode != None):
            (last, lengths) = self.bellmanFordSolution
            activeNode = self.endNode
            numNodes = 0
            totalActiveDist = lengths[self.endNode]
            while (activeNode != self.startNode):
                nextNode = last[activeNode]
                activePos = ((activeNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                              int((activeNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[
                                  1] + self.gridCellSize[1] / 2)
                nextPos = ((nextNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                           int((nextNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                           self.gridCellSize[1] / 2)
                activeNodeFloor = int(activeNode / (self.rows * self.columns))
                nextNodeFloor = int(nextNode / (self.rows * self.columns))
                if (activeNodeFloor == self.activeFloor and nextNodeFloor == self.activeFloor):
                    pygame.draw.line(self.currentMaze, (0, 0, 0), activePos, nextPos, 3)
                activeNode = nextNode
                numNodes += 1
            newMessage = "Nodes Traversed: " + str(numNodes)
            if (self.bellmanFordNodesTraversed.text != newMessage):
                self.bellmanFordNodesTraversed.text = newMessage
                self.bellmanFordNodesTraversed.preRender()
            newMessage = "Total Difficulty: " + str(totalActiveDist)
            if (self.bellmanFordTotalDifficulty.text != newMessage):
                self.bellmanFordTotalDifficulty.text = newMessage
                self.bellmanFordTotalDifficulty.preRender()
        else:
            newMessage = "Nodes Traversed: N/A"
            if (self.bellmanFordNodesTraversed.text != newMessage):
                self.bellmanFordNodesTraversed.text = newMessage
                self.bellmanFordNodesTraversed.preRender()
            newMessage = "Total Difficulty: N/A"
            if (self.bellmanFordTotalDifficulty.text != newMessage):
                self.bellmanFordTotalDifficulty.text = newMessage
                self.bellmanFordTotalDifficulty.preRender()

    def renderLegend(self):
        if(self.renderingLegend):
            self.screen.blit(self.legend, self.legendPos)

    def drawMaze(self):
        self.screen.blit(self.mazeBorder, (self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
        if(self.currentMaze != None):
            if (self.startNode != None and int(self.startNode / (self.rows * self.columns)) == self.activeFloor):
                startNodeSize = self.startNodeSurface.get_size()
                startNodePos = (
                self.gridCellSize[0] * (self.startNode % self.columns) + self.gridCellSize[0] / 2 - startNodeSize[0] / 2,
                self.gridCellSize[1] * int((self.startNode % (self.rows * self.columns)) / self.columns) +
                self.gridCellSize[1] / 2 - startNodeSize[1] / 2)
                self.currentMaze.blit(self.startNodeSurface, startNodePos)
            if (self.endNode != None and int(self.endNode / (self.rows * self.columns)) == self.activeFloor):
                endNodeSize = self.endNodeSurface.get_size()
                endNodePos = (
                self.gridCellSize[0] * (self.endNode % self.columns) + self.gridCellSize[0] / 2 - endNodeSize[0] / 2,
                self.gridCellSize[1] * int((self.endNode % (self.rows * self.columns)) / self.columns) +
                self.gridCellSize[1] / 2 - endNodeSize[1] / 2)
                self.currentMaze.blit(self.endNodeSurface, endNodePos)

            mousePos = (pygame.mouse.get_pos()[0] - self.mazePos[0], pygame.mouse.get_pos()[1] - self.mazePos[1])
            if (0 < mousePos[0] < self.mazeSize[0] and 0 < mousePos[1] < self.mazeSize[1]):
                mouseMazePos = (int(mousePos[0] / self.gridCellSize[0]), int(mousePos[1] / self.gridCellSize[1]))
                self.currentNode = mouseMazePos[0] + self.columns * mouseMazePos[1] + self.activeFloor * self.rows * self.columns
                currentNodeSize = self.currentNodeSurface.get_size()
                currentNodePos = (
                    mouseMazePos[0] * self.gridCellSize[0] + self.gridCellSize[0] / 2 - currentNodeSize[0] / 2,
                    mouseMazePos[1] * self.gridCellSize[1] + self.gridCellSize[1] / 2 - currentNodeSize[1] / 2)
                self.currentMaze.blit(self.currentNodeSurface, currentNodePos)
            if(self.activeNode != None):
                activeNodeMazePos = (self.activeNode % self.columns, int((self.activeNode % (self.rows * self.columns)) / self.columns))
                activeNodeSize = self.activeNodeSurface.get_size()
                activeNodePos = (activeNodeMazePos[0] * self.gridCellSize[0] + self.gridCellSize[0]/2 - activeNodeSize[0]/2, activeNodeMazePos[1] * self.gridCellSize[1] + self.gridCellSize[1]/2 - activeNodeSize[1]/2)
                self.currentMaze.blit(self.activeNodeSurface, activeNodePos)
            self.screen.blit(self.currentMaze, self.mazePos)

    def button_generateMaze(self):
        self.activeFloor = 0
        self.activeNode = None
        self.floorCounter.text = "Floor: " + str(self.activeFloor)
        self.floorCounter.preRender()
        print("Viewing Floor",self.activeFloor)

        print("Generate Maze.")
        self.updateProcessing()
        startTime = time.time()
        self.graph = createRandomGraph(self.rows, self.columns, self.floors, self.updateProcessing)
        elapsedTime = time.time() - startTime
        alertMsg = "Generated " + str(self.rows) + "x" + str(self.columns) + "x" + str(self.floors) + " Maze\nElapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(alertMsg)
        pyautogui.alert(text=alertMsg,title="Maze Generation Algorithm Runtime")
        print("Edges:", self.graph.getEdgeCount())
        self.preRenderMaze()
        self.dijkstraSolution = None
        self.bellmanFordSolution = None
        self.startNode = 0
        self.endNode = self.rows*self.columns*self.floors - 1

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
                    lineColor = self.edgeDict[pathName][0]
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
        self.preRenderNodes()

    def preRenderNodes(self):
        nodeSize = (self.gridCellSize[0]*0.6,self.gridCellSize[1]*0.6)
        self.startNodeSurface = self.makeSurface(nodeSize,(190,120,200))
        self.endNodeSurface = self.makeSurface(nodeSize,(120,50,130))
        self.currentNodeSurface = self.makeSurface(nodeSize,(0,255,210))
        self.activeNodeSurface = self.makeSurface(nodeSize,(255,0,0))

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
            self.graph = None
            self.renderedMaze = None
            self.currentMaze = None
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
        if(self.graph == None):
            pyautogui.alert(text="You must generate a maze first.",title="Error")
            return
        if(self.renderBellmanFromActiveNode):
            pass
            #self.renderBellmanFromActiveNode = False
        print("Solving Maze using Dijkstra's Algorithm")
        self.updateProcessing()
        startTime = time.time()
        (last, lengths) = dijkstra(self.graph,self.startNode, self.updateProcessing)
        elapsedTime = time.time() - startTime
        elapsedTimeMsg = "Elapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(elapsedTimeMsg)
        pyautogui.alert(text=elapsedTimeMsg,title="Dijkstra's Algorithm Runtime")
        self.dijkstraSolution = (last,lengths)

    def button_stepThroughDijkstra(self):
        if (self.dijkstraSolution == None):
            pyautogui.alert(text="You must solve using Dijkstra's algorithm first.", title="Error")
            return
        else:
            # self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
            # self.screen.blit(self.currentMaze, self.mazePos)
            # pygame.display.update()
            # time.sleep(0.001)
            # self.update()
            self.preRenderMaze()
            self.renderMaze()
            self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
            self.screen.blit(self.currentMaze, self.mazePos)
            stack = []
            (last, lengths) = self.dijkstraSolution
            currentNode = self.endNode
            numNodes = 0
            totalDist = 0
            delay = 0.2
            while (currentNode != self.startNode):
                nextNode = last[currentNode]
                currentPos = ((currentNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                              int((currentNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                              self.gridCellSize[1] / 2)
                nextPos = ((nextNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                           int((nextNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                           self.gridCellSize[1] / 2)
                currentNodeFloor = int(currentNode / (self.rows * self.columns))
                nextNodeFloor = int(nextNode / (self.rows * self.columns))
                stack.append((currentPos, nextPos, currentNodeFloor - nextNodeFloor))
                #print((currentPos, nextPos))
                currentNode = nextNode
                numNodes += 1
                totalDist += lengths[currentNode]
            while (len(stack) > 0):
                values = stack[len(stack) - 1]
                stack.pop(len(stack) - 1)
                currentPos = values[0]
                nextPos = values[1]
                floorChange = values[2]
                # print(currentPos)
                # print(nextPos)
                # print(floorChange)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == KEYDOWN:
                        if (event.key == K_ESCAPE):
                            quit()
                        if (event.key == K_UP):
                            if(delay - 0.05 > 0):
                                delay = delay - 0.05
                            else:
                                delay = 0.01
                        if (event.key == K_DOWN):
                            delay = delay + 0.05
                if (floorChange != 0):
                    self.activeFloor = self.activeFloor + floorChange
                    self.preRenderMaze()
                    self.renderMaze()
                    self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
                    self.screen.blit(self.currentMaze, self.mazePos)
                    self.floorCounter.text = "Floor: " + str(self.activeFloor)
                    self.floorCounter.preRender()
                    print("Viewing Floor", self.activeFloor)
                    self.renderObjects()
                else:
                    # self.renderMaze()
                    #print("draw line: ",currentPos, nextPos)
                    pygame.draw.line(self.currentMaze, (255, 0, 255), currentPos, nextPos, 3)

                    self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
                    self.screen.blit(self.currentMaze,self.mazePos)
                    time.sleep(delay)
                    pygame.display.update()
                    #print("did I do that")
                #time.sleep(1)
            pygame.display.update()

    def button_solveBellmanFord(self):
        if(self.graph == None):
            pyautogui.alert(text="You must generate a maze first.",title="Error")
            return
        print("Solving Maze using Bellman Ford's Algorithm")
        self.updateProcessing()
        startTime = time.time()
        (last, lengths) = BellmanFord(self.graph, self.startNode, self.rows, self.columns, self.floors, self.updateProcessing)
        elapsedTime = time.time() - startTime
        elapsedTimeMsg = "Elapsed Time: " + str(round(elapsedTime,5)) + " seconds"
        print(elapsedTimeMsg)
        pyautogui.alert(text=elapsedTimeMsg,title="Bellman Ford's Algorithm Runtime")
        self.bellmanFordSolution = (last,lengths)
        if(self.dijkstraSolution == None):
            self.renderBellmanFromActiveNode = True

    def button_stepThroughBellmanFord(self):
        if (self.bellmanFordSolution == None):
            pyautogui.alert(text="You must solve using Bellman Ford's algorithm first.", title="Error")
            return
        else:
            self.preRenderMaze()
            self.renderMaze()
            self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
            self.screen.blit(self.currentMaze, self.mazePos)
            stack = []
            (last, lengths) = self.bellmanFordSolution
            currentNode = self.endNode
            numNodes = 0
            delay = 0.2
            while (currentNode != self.startNode):
                nextNode = last[currentNode]
                currentPos = ((currentNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                              int((currentNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                              self.gridCellSize[1] / 2)
                nextPos = ((nextNode % self.columns) * self.gridCellSize[0] + self.gridCellSize[0] / 2,
                           int((nextNode % (self.rows * self.columns)) / self.columns) * self.gridCellSize[1] +
                           self.gridCellSize[1] / 2)
                currentNodeFloor = int(currentNode / (self.rows * self.columns))
                nextNodeFloor = int(nextNode / (self.rows * self.columns))
                stack.append((currentPos, nextPos, currentNodeFloor - nextNodeFloor))
                currentNode = nextNode
                numNodes += 1
            while (len(stack) > 0):
                values = stack[len(stack) - 1]
                stack.pop(len(stack) - 1)
                currentPos = values[0]
                nextPos = values[1]
                floorChange = values[2]
                # print(currentPos)
                # print(nextPos)
                # print(floorChange)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == KEYDOWN:
                        if (event.key == K_ESCAPE):
                            quit()
                        if (event.key == K_UP):
                            if(delay - 0.05 > 0):
                                delay = delay - 0.05
                            else:
                                delay = 0.01
                        if (event.key == K_DOWN):
                            delay = delay + 0.05
                if (floorChange != 0):
                    self.activeFloor = self.activeFloor + floorChange
                    self.preRenderMaze()
                    self.renderMaze()
                    self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
                    self.screen.blit(self.currentMaze, self.mazePos)
                    self.floorCounter.text = "Floor: " + str(self.activeFloor)
                    self.floorCounter.preRender()
                    print("Viewing Floor", self.activeFloor)
                    self.renderObjects()
                else:
                    # self.renderMaze()
                    #print("draw line: ",currentPos, nextPos)
                    pygame.draw.line(self.currentMaze, (0, 255, 0), currentPos, nextPos, 3)

                    self.screen.blit(self.mazeBorder,(self.mazePos[0] - self.mazeBorderThick, self.mazePos[1] - self.mazeBorderThick))
                    self.screen.blit(self.currentMaze,self.mazePos)
                    time.sleep(delay)
                    pygame.display.update()
                    #print("did I do that")
                #time.sleep(1)
            pygame.display.update()

    def updateProcessing(self, percent=-1):
        percent = int(percent)
        self.processing.text = "Processing..."
        if(percent != -1): self.processing.text += str(percent) + "%"
        self.processing.preRender()
        print(self.processing.text)
        self.processing.render(self.screen, True)

    def showLegend(self):
        self.renderingLegend = True

    def hideLegend(self):
        self.renderingLegend = False

    def button_setStart(self):
        if(self.activeNode != None):
            self.startNode = self.activeNode
            self.activeNode = None
            self.dijkstraSolution = None
            self.bellmanFordSolution = None

    def button_setEnd(self):
        if (self.activeNode != None):
            self.endNode = self.activeNode
            self.activeNode = None

    def mouseMazeClick(self):
        if(self.graph != None):
            self.activeNode = self.currentNode

    def clearActiveNode(self):
        self.activeNode = None

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