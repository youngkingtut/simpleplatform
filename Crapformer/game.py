__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import pygame
from config import Config as C


class State(object):
    def __init__(self, screen, state_vars):
        self.screen = screen
        self.state_vars = state_vars

    def run(self):
        return None


class PlayGame(State):
    def setup(self):
        self.surface = pygame.Surface(C.SCREEN_SIZE)
        self.surface.fill((234, 234, 234))
        self.player = pygame.image.load('../Sprites/crusty_running/crusty1.png')
        self.player_position = [C.SCREEN_SIZE[0] - 50, 0]
        self.surface.blit(self.player, (self.player_position))

    def run(self):
        self.setup()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.dict["key"] == pygame.K_LEFT:
                    self.player_position[0] -= 2
                if event.dict["key"] == pygame.K_RIGHT:
                    self.player_position[0] += 2
                if event.dict["key"] == pygame.K_UP:
                    self.player_position[1] -= 2
                if event.dict["key"] == pygame.K_DOWN:
                    self.player_position[1] += 2
            self.surface.fill((234, 234, 234))
            self.surface.blit(self.player, (self.player_position))
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()


class StateHandler(object):
    def __init__(self):
        self.screen = None
        self.current_state = None
        self.state_vars = {}

    def setup(self):
        pygame.init()
        pygame.display.set_caption(C.CAPTION)
        self.screen = pygame.display.set_mode(C.SCREEN_SIZE)
        self.current_state = PlayGame(self.screen, self.state_vars)

    def end_game(self):
        pygame.quit()

    def run_game(self):
        while self.current_state:
            current_state_object = self.current_state.run()
            self.current_state = current_state_object if not hasattr(current_state_object, "__call__") else current_state_object(self.screen, self.state_vars)
