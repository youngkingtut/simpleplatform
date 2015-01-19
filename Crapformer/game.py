__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import pygame
from config import Config as C


class Crapformer(object):
    def __init__(self):
        self.screen = None

    def setup(self):
        pygame.init()
        pygame.display.set_caption(C.CAPTION)
        self.screen = pygame.display.set_mode(C.SCREEN_SIZE)

    def display(self, surface, position):
        self.screen.blit(surface, position)
        pygame.display.flip()

    def end_game(self):
        pygame.quit()
