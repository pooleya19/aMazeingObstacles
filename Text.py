import pygame
from pygame.locals import *

def getTextSurface(text, textSize=50):
    font = pygame.font.SysFont("Calibri",textSize)
    textColor = Color(0,0,0)
    antialias = False
    return font.render(text,antialias,textColor)

def makeSurface(size, rgb):
    surface = pygame.Surface(size)
    surface = surface.convert()
    surface.fill(rgb)
    return surface

class Text:
    def __init__(self, text, textSize, textPos, backColor = (180,180,180)):
        self.text = text
        self.textSize = textSize
        self.textPos = textPos
        self.backColor = backColor
        self.preRender()

    def preRender(self):
        self.tempTextSurface = getTextSurface(self.text, self.textSize)
        self.textSurface = makeSurface(self.tempTextSurface.get_size(), self.backColor)
        self.textSurface.blit(self.tempTextSurface, (0,0))
        self.size = self.textSurface.get_size()
        self.cornerPos = (self.textPos[0] - self.size[0] / 2, self.textPos[1] - self.size[1] / 2)

    def render(self, screen, update=False):
        screen.blit(self.textSurface, self.cornerPos)
        if(update): pygame.display.update(Rect(self.cornerPos, self.size))