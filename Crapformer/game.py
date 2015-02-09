__author__ = "Charles A. Parker", "Tristan Q. Storz", "Robert P. Cope"

import pygame
from gameconfig import GameConfig
import logging
import world

game_logger = logging.getLogger(__name__)


class State(object):
    '''
    Default State class. The StateHandler depends on each state having a run
    method. If a new state does not redefine the run method, then the default
    run method will return none and StateHandler.run_game will exit. Also,
    contains the Pygame screen and state_vars for communicating across states.
    '''
    def __init__(self, screen, state_vars):
        self.screen = screen
        self.state_vars = state_vars

    def run(self):
        return None


class PlayGame(State):
    def __init__(self, *args, **kwargs):
        State.__init__(self, *args, **kwargs)
        self.surface = None
        self.clock = None
        self.world = None

    def setup(self):
        '''
        Creates a screen to blit images to and a clock for this
        instance of play.
        '''
        # TODO: Add support for SCREEN_SIZE and other config options
        # changing while the game is running
        self.surface = pygame.Surface(GameConfig.SCREEN_SIZE)
        self.surface.fill((234, 234, 234))
        self.clock = pygame.time.Clock()
        self.world = world.LevelOne(self.state_vars, self.surface)

    def run(self):
        '''
        Passes in (pygame.event.Event)s until an exit condition is met.
        The exit condition is determined by the active World.  This also
        handles the time between frames in game.  For each frame, it
        delays a set amount of time, and then renders the surface generated
        by the World instance running.
        '''
        self.setup()
        while not self.world.is_complete:
            state = self.world.recieve_events(pygame.event.get())
            # 10 frames per second max
            self.clock.tick(10)

            self.world.process_events()

            self.surface.fill((234, 234, 234))
            self.world.render_surface()
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()

        # Handle completed status
        return None


class StateHandler(object):
    '''
    Handles change of game state (no way!).
    #TODO: I don't understand this well enough to
           write a useful docstring right now.
    '''
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
