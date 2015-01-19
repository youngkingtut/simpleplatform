__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import pygame
from gameconfig import GameConfig
import logging

game_logger = logging.getLogger(__name__)


class State(object):
    def __init__(self, screen, state_vars):
        self.screen = screen
        self.state_vars = state_vars

    def run(self):
        return None


class PlayGame(State):
    def __init__(self, *args, **kwargs):
        State.__init__(self, *args, **kwargs)
        self.surface = None
        self.player = None
        self.player_position = None
        self.clock = None

        self.player_2 = None
        self.player_2_position = None

    def setup(self):
        self.surface = pygame.Surface(GameConfig.SCREEN_SIZE)
        self.surface.fill((234, 234, 234))
        self.player = pygame.image.load('../Sprites/crusty_running/crusty1.png')
        self.player_2 = pygame.image.load('../Sprites/crusty_running/crusty2.png')
        self.player_position = [GameConfig.SCREEN_SIZE[0] - 50, 0]
        self.player_2_position = [GameConfig.SCREEN_SIZE[0] - 50, 100]
        self.surface.blit(self.player, self.player_position)
        self.surface.blit(self.player_2, self.player_2_position)
        self.clock = pygame.time.Clock()

    def run(self):
        self.setup()
        forward = True
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
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

            if self.player_2_position[0] > 200:
                forward = False
            if self.player_2_position[0] < 20:
                forward = True
            self.player_2_position[0] += 1 if forward else -1

            self.surface.fill((234, 234, 234))
            self.surface.blit(self.player, self.player_position)
            self.surface.blit(self.player_2, self.player_2_position)
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()


class StateHandler(object):
    def __init__(self):
        self.screen = None
        self.current_state = None
        self.state_vars = {}

    def setup(self):
        pygame.init()
        pygame.display.set_caption(GameConfig.CAPTION)
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_SIZE)
        self.current_state = PlayGame(self.screen, self.state_vars)

    def end_game(self):
        pygame.quit()

    def run_game(self):
        while self.current_state:
            current_state_object = self.current_state.run()
            self.current_state = current_state_object if not hasattr(current_state_object, "__call__") else current_state_object(self.screen, self.state_vars)

    def teardown(self):
        pass