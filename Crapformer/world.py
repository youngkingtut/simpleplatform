__author__ = "Charles A. Parker; Tristan Q. Storz; Robert P. Cope"

import itertools
import pygame
import random
import logging
import pygame.transform as pytf

world_logger = logging.getLogger(__name__)

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
        #TODO: Objects are blitted together in dict order. Need to add concept
        #      of layers to World class to order blitting by depth.
        #      May also want to condsider different ways graphics
        #      might be drawn to plan for all use cases.
        allsprites = pygame.sprite.RenderPlain(map(lambda obj: obj.get_current_sprite(), self.world_objects.values()))
        allsprites.update()
        allsprites.draw(self.surface)

        # for surf in map(lambda obj: obj.get_current_sprite(), self.world_objects.values()):
        #     surf.draw(self.surface)


#TODO: Should we have different types of Worlds -- Menus?  Gameworlds?
#      Or should those be handled seperately and have World be exclusively 
#      for things like LevelOne?

#TODO: We should probably make each Level their own file.  Should also
#      consider an 
class LevelOne(World):
    #TODO: Flesh out the utilities needed to build a Level.  How should
    #levels be created?  Should level maps be created
    def __init__(self, *args, **kwargs):
        World.__init__(self, *args, **kwargs)
        for x in xrange(0, 800, 32):
            id = self.gen_id()
            self.world_objects[id] = GrassBlock(id, (x, 380))
        #TODO: There's certainly a better way than this to draw
        #      backgrounds...
        for y in xrange(0, 380, 32):
            for x in xrange(0, 800, 32):
                id = self.gen_id()
                #TODO: Commented this out since layering doesn't exist.  need to see Player instance.
                # self.world_objects[id] = SkyBlock(id, (x, y))

        player_id = self.gen_id()
        self.world_objects[player_id] = Player(player_id, [200, 200])

# === OVERARCHING WORLD OBJECT ===
class WorldObject(pygame.sprite.Sprite):
    #TODO: Need to determine the real purpose of this 
    #      class. What needs to be contained in here?
    '''
    A WorldObject is any object within a level.
    '''
    def __init__(self, id, pos, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self, *args, **kwargs)
        self.id = id
        self.pos = pos

# === TYPES OF WORLD OBJECTS ===
#TODO: What WorldObject types are there? 
class InteractableObject(WorldObject):
    '''
    Can interact with other objects that 
    are also interactable.  They can collide, etc.
    '''    
    def __init__(self, *args, **kwargs):
        pass


class NoninteractableObject(WorldObject):
    '''
    Can NOT interact with any other objects.  No collisions, etc.
    '''
    def __init__(self, *args, **kwargs):
        pass


# === TYPES OF INTERACTABLE OBJECTS ===
class GrassBlock(InteractableObject):
    '''
    Grass blocks that act as platforms.
    '''
    #Source for the images associated with this class
    image_srcs = ['../Sprites/grass/grass1.png',
                  '../Sprites/grass/grass2.png',
                  '../Sprites/grass/grass3.png']
    sprites = [pygame.image.load(src) for src in image_srcs]

    def __init__(self, *args, **kwargs):
        '''
        Selects a random sprite to be loaded for each instance.
        Initializes position and rect object for this instance.
        '''
        WorldObject.__init__(self, *args, **kwargs)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def get_current_sprite(self):
        return(self)


class Player(InteractableObject):
    #TODO: Ew...  Should make a better system for tracking state.
    STATE_STANDING = 0
    STATE_RUNNING_RIGHT = 1
    STATE_RUNNING_LEFT  = 2
    STATE_FALLING = 3

    standing_image_srcs = ['../Sprites/crusty_running/crusty1.png']
    running_image_srcs  = ['../Sprites/crusty_running/crusty1.png',
                           '../Sprites/crusty_running/crusty2.png']
    
    standing_images = [pygame.image.load(src) for src in standing_image_srcs]
    running_images  = [pygame.image.load(src) for src in running_image_srcs]

    #TODO: This should be somewhere else... probably in a method
    running_animation = itertools.cycle(running_images)

    def __init__(self, *args, **kwargs):
        WorldObject.__init__(self, *args, **kwargs)
        self.state = Player.STATE_RUNNING_RIGHT

    #TODO: Remove this.  Only here to test out animation of Player
    #      Can't get it to work and I'm tired.  bed time.  I'll branch nd leave this here.
    def handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        if True == pressed_keys[pygame.K_LEFT]:
            self.state = Player.STATE_RUNNING_LEFT
            self.pos[0] -= 4
        elif True == pressed_keys[pygame.K_RIGHT]:
            self.state = Player.STATE_RUNNING_RIGHT
            self.pos[0] += 4
        elif True == pressed_keys[pygame.K_UP]:
            self.pos[1] -= 4
        elif True == pressed_keys[pygame.K_DOWN]:
            self.pos[1] += 4
        else:
            self.state = Player.STATE_STANDING
            
    def get_current_sprite(self):
        self.handle_input()
        #TODO: Maybe set up states as a key = state, value = action system?
        if self.state == Player.STATE_RUNNING_LEFT:
            #TODO: Standardize updating of image and rect attributes.
            self.image = pytf.flip(self.running_animation.next(), True, False)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
            return(self)

        if self.state == Player.STATE_RUNNING_RIGHT:
            #TODO: Standardize updating of image and rect attributes.
            self.image = self.running_animation.next()
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
            return(self)
            
        elif self.state == Player.STATE_STANDING:
            self.image = self.standing_images[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
            return(self)


# === NONINTERACTABLE OBJECTS ===
class SkyBlock(NoninteractableObject):
    '''
    Sky blocks that act as background coloring.  These are
    used to paint the scenery of the World. :3
    '''
    #Source for the images associated with this class
    image_srcs = ['../Sprites/sky/sky1.png']
    sprites = [pygame.image.load(src) for src in image_srcs]

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

    def get_current_sprite(self):
        return(self)



#GARBAGE CODE, LOL



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