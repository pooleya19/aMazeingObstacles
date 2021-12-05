import pygame
from pygame.locals import Color

def getTextSurface(text, size=50):
    font = pygame.font.SysFont("Calibri",size)
    textColor = Color(0,0,0)
    antialias = False
    return font.render(text,antialias,textColor)

class Text:
    def __init__(self, text, size, textPos):
        self.textSurface = getTextSurface(text,size)
        self.size = self.textSurface.get_size()
        self.textPos = (textPos[0]-self.size[0]/2,textPos[1]-self.size[1]/2)

    def render(self, screen):
        screen.blit(self.textSurface, self.textPos)