import pygame
from pygame.locals import *
import sys
from Button import Button
from Text import getTextSurface
from Text import Text

class Display:
    def __init__(self):
        pygame.init()
        self.buttons = []
        self.texts = []

    def start(self):
        print("Beginning Program.")
        screenSize = (1200,800)
        self.screen = pygame.display.set_mode(screenSize)
        print("Screen Size:", self.screen.get_size())
        pygame.display.set_caption("Maze Visual")

        self.background = self.makeSurface(self.screen.get_size(), (180,180,180))
        self.screen.blit(self.background, (0,0))

        self.createObjects()

    def createObjects(self):
        self.buttons.append(Button("Generate Maze",50,(200,200),self.button_GenerateMaze))
        self.texts.append(Text("aMazeing Obstacles", 50, (230,40)))

    def makeSurface(self, size, rgb):
        surface = pygame.Surface(size)
        surface = surface.convert()
        surface.fill(rgb)
        return surface

    def update(self):
        self.renderObjects()
        self.handleEvents()
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

    def button_GenerateMaze(self):
        print("Generate Maze")

    def quit(self):
        print("Attempted Quit")
        pygame.quit()
        sys.exit()