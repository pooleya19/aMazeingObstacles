import pygame
from pygame.locals import *
import sys

class Display:

    def start(self):
        print("Beginning Program.")
        screenSize = (1200,800)
        self.screen = pygame.display.set_mode(screenSize)
        print("Screen Size:", self.screen.get_size())
        pygame.display.set_caption("Maze Visual")

        self.background = self.makeSurface(self.screen.get_size(), (180,180,180))
        self.screen.blit(self.background, (0,0))

    def makeSurface(self, size, rgb):
        surface = pygame.Surface(size)
        surface = surface.convert()
        surface.fill(rgb)
        return surface

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    quit()
                elif (event.key == K_SPACE):
                    #generateMaze()
                    pass

    def quit(self):
        print("Attempted Quit")
        pygame.quit()
        sys.exit()