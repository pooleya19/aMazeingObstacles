import pygame
from Text import getTextSurface

class Button:
    def __init__(self, text, textSize, buttonPos, func=None):
        self.func = func
        self.text = text
        self.textSize = textSize
        self.buttonPos = buttonPos
        self.preRenderSurface()
        self.hoverOver = False
        self.hoverOn = None
        self.hoverOff = None

    def preRenderSurface(self):
        textSurface = getTextSurface(self.text, self.textSize)

        textBorder = 10
        self.size = (textSurface.get_size()[0] + 2 * textBorder, textSurface.get_size()[1] + 2 * textBorder)
        buttonSurface_default = pygame.Surface(self.size)
        buttonSurface_default.convert()
        buttonSurface_default.fill((140, 140, 140))
        buttonSurface_default.blit(textSurface, (textBorder, textBorder))
        buttonSurface_hover = pygame.Surface(self.size)
        buttonSurface_hover.convert()
        buttonSurface_hover.fill((100, 100, 100))
        buttonSurface_hover.blit(textSurface, (textBorder, textBorder))
        self.buttonSurfaces = (buttonSurface_default, buttonSurface_hover)
        self.cornerPos = (self.buttonPos[0] - self.size[0] / 2, self.buttonPos[1] - self.size[1] / 2)


    def render(self, screen):
        if(self.mouseOver()):
            screen.blit(self.buttonSurfaces[1], self.cornerPos)
            if(self.hoverOver == False):
                self.hoverOver = True
                if(self.hoverOn != None): self.hoverOn()
        else:
            screen.blit(self.buttonSurfaces[0], self.cornerPos)
            if(self.hoverOver == True):
                self.hoverOver = False
                if(self.hoverOff != None): self.hoverOff()

    def mouseOver(self):
        cursorPos = pygame.mouse.get_pos()
        if(self.cornerPos[0] < cursorPos[0] < self.cornerPos[0] + self.size[0]
        and self.cornerPos[1] < cursorPos[1] < self.cornerPos[1]+self.size[1]):
            return True
        else:
            return False

    def setHoverFunctions(self, hoverOn, hoverOff):
        self.hoverOn = hoverOn
        self.hoverOff = hoverOff



    def activate(self):
        if(self.func != None):  self.func()