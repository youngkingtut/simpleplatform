__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import itertools
import pygame

class World(object):
    '''
    This is a generic level.  It tracks all the objects in a given
    a level.  It allows us to aggregate every element of a level into
    one place, which is quite handy!
    '''
    def __init__(self):
        self.idgen = itertools.count()
        self.world_objects = {}

    def gen_id(self):
        '''
        Return the next available object ID for this world.
        '''
        return self.idgen.next()

class WorldObject(pygame.Surface):
    '''
    This is an object within a level.  All world objects
    should inherit this, obviously. :D
    '''
    def __init__(self, id, *args, **kwargs):
        self.id = id

class WorldSolidBlock(WorldObject):
    pass
