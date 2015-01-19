__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import itertools
import pygame
import random

class World(object):
    '''
    This is a generic level.  It tracks all the objects in a given
    a level.  It allows us to aggregate every element of a level into
    one place, which is quite handy!
    '''
    def __init__(self, state, surface):
        self.idgen = itertools.count()
        self.world_objects = {}
        self.surface = surface
        self.state = state

    def gen_id(self):
        '''
        Return the next available object ID for this world.
        '''
        return self.idgen.next()

    def recieve_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return None
        return True

    def process_events(self):
        pass

    def render_surface(self):
        print self.world_objects.values()
        allsprites = pygame.sprite.RenderPlain(self.world_objects.values())
        allsprites.update()
        allsprites.draw(self.surface)


class LevelOne(World):
    def __init__(self, *args, **kwargs):
        World.__init__(*args, **kwargs)

        for x in xrange(0, 100, 32):
            id = self.gen_id()
            self.world_objects[id] = GrassBlock(id, (x,0))




class WorldObject(pygame.sprite.Sprite):
    '''
    This is an object within a level.  All world objects
    should inherit this, obviously. :D
    '''
    def __init__(self, id, pos, *args, **kwargs):
        self.id = id
        self.pos = pos
        pygame.sprite.Sprite.__init__(self, *args, **kwargs)


class GrassBlock(WorldObject):
    sprites_src = ['../Sprites/grass/grass1.png',
                   '../Sprites/grass/grass2.png',
                   '../Sprites/grass/grass3.png']

    sprites = [pygame.image.load(src) for src in sprites_src]

    def __init__(self, *args, **kwargs):
        WorldObject.__init__(*args, **kwargs)
        self.image = random.choice(sprites)
        self.rect  = self.image.get_rect()
        self.rect.topleft = self.pos


class Player(WorldObject):
    def __init__(self):
        pass







# self.player = pygame.image.load('../Sprites/crusty_running/crusty1.png')
#         self.player_2 = pygame.image.load('../Sprites/crusty_running/crusty2.png')
#         self.player_position = [GameConfig.SCREEN_SIZE[0] - 50, 0]
#         self.player_2_position = [GameConfig.SCREEN_SIZE[0] - 50, 100]

                # for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             return None
        #         if event.type == pygame.KEYDOWN:
        #             if event.dict["key"] == pygame.K_LEFT:
        #                 self.player_position[0] -= 2
        #             if event.dict["key"] == pygame.K_RIGHT:
        #                 self.player_position[0] += 2
        #             if event.dict["key"] == pygame.K_UP:
        #                 self.player_position[1] -= 2
        #             if event.dict["key"] == pygame.K_DOWN:
        #                 self.player_position[1] += 2