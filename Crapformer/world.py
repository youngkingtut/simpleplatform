__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import itertools
import pygame
import random

class World(object):
    '''
    This is the the most basic level class.
    The player can interact with things inside a World.
    World objects are what generate the image seen at any time
    based on the objects inside of that World.  This includes Menus, 
    Levels, etc.
    '''
    def __init__(self, state, surface):
        '''
        '''
        self.idgen = itertools.count()
        self.world_objects = {}
        self.surface = surface
        self.state = state
        self.is_complete = False

    def gen_id(self):
        return self.idgen.next()

    def recieve_events(self, events):
        '''
        Takes in events from any source (really should only be 
        the function or class that instantiated this World) and 
        reacts.  The passed in events are expected to be instances of
        pygame.event.Event
        '''
        for event in events:
            if event.type == pygame.QUIT:
                self.is_complete = True
        return True

    def process_events(self):
        pass

    def render_surface(self):
        allsprites = pygame.sprite.RenderPlain(self.world_objects.values())
        allsprites.update()
        allsprites.draw(self.surface)


#TODO: Should we have different types of Worlds -- Menus?  Gameworlds?
#Or should those be handled seperately and have World be exclusively 
#for things like LevelOne?
class LevelOne(World):
    #TODO: Flesh out the utilities needed to build a Level.  How should
    #levels be created?  Should level maps be created
    def __init__(self, *args, **kwargs):
        World.__init__(self, *args, **kwargs)
        for x in xrange(0, 800, 32):
            id = self.gen_id()
            self.world_objects[id] = GrassBlock(id, (x, 380))
        for y in xrange(0, 380, 32):
            for x in xrange(0, 800, 32):
                id = self.gen_id()
                self.world_objects[id] = SkyBlock(id, (x, y))


class WorldObject(pygame.sprite.Sprite):
    #TODO: Need to determine the real purpose of this 
    #      class. What needs to be contained in here?

    #TODO: Objects are blitted together in dict order. Need to add concept
    #      of layers to World class to order blitting by depth.
    #      May also want to condsider different ways graphics
    #      might be drawn to plan for all use cases.
    '''
    A WorldObject is any object within a level.
    '''
    def __init__(self, id, pos, *args, **kwargs):
        self.id = id
        self.pos = pos
        pygame.sprite.Sprite.__init__(self, *args, **kwargs)


#TODO: What WorldObject types are there? 
class Platform(WorldObject):
    #TODO: Is this where the __init__s of GrassBlock would go?
    pass


class Background(WorldObject):
    #TODO: And SkyBlock would stick it's __init__ here?
    pass


class GrassBlock(Platform):
    '''
    Grass blocks that act as platforms.
    '''
    #Source for the images associated with this class
    sprites_src = ['../Sprites/grass/grass1.png',
                   '../Sprites/grass/grass2.png',
                   '../Sprites/grass/grass3.png']
    sprites = [pygame.image.load(src) for src in sprites_src]

    def __init__(self, *args, **kwargs):
        '''
        Selects a random sprite to be loaded for each instance.
        Initializes position and rect object for this instance.
        '''
        WorldObject.__init__(self, *args, **kwargs)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


class SkyBlock(Background):
    '''
    Sky blocks that act as background coloring.  These are
    used to paint the scenery of the World. :3
    '''
    #Source for the images associated with this class
    sprites_src = ['../Sprites/sky/sky1.png']
    sprites = [pygame.image.load(src) for src in sprites_src]

    def __init__(self, *args, **kwargs):
        '''
        Selects a random sprite to be loaded for this instance.
        Initializes positiona and rect object for this instance.
        '''
        #TODO: Should this stuff be handled in WorldObject?
        WorldObject.__init__(self, *args, **kwargs)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos







#GARBAGE CODE, LOL


#class Player(WorldObject):
#    def __init__(self):
#        pass

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