__author__ = "Charles A. Parker",  "Tristan Q. Storz",  "Robert P. Cope"

import itertools
import pygame
import random
import math
import logging
import operator
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
        #
        #      There is a concept of layering in Sprite.Groups.  Can and probably
        #      should use that and design rendering around that.
        allsprites = pygame.sprite.RenderPlain(map(lambda obj: obj.get_current_sprite(), self.world_objects.values()))
        allsprites.update()
        allsprites.draw(self.surface)

    #TODO: [DETECTION] Need to add a mechanism for an element of
    #      the world to query for other elements of the world.
    #      Maybe somethng like find_nearby_instance_of_class()?
    #
    #      Would it be beneficial to track objects of interest 
    #      and objects of not-interest seperately, so a method
    #      like find_nearby_indtance... would have a smaller set
    #      to scan?


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
        for x in xrange(0, 800, 64):
            id = self.gen_id()
            self.world_objects[id] = GrassBlock(id, (x, 340))
        #TODO: There's certainly a better way than this to draw
        #      backgrounds...
        for y in xrange(0, 340, 64):
            for x in xrange(0, 800, 64):
                id = self.gen_id()
                #TODO: Commented this out since layering doesn't exist.  need to see Player instance.
                # self.world_objects[id] = SkyBlock(id, (x, y))

        player_id = self.gen_id()
        self.world_objects[player_id] = Player(player_id, [200, 200])

        monster_id = self.gen_id()
        self.world_objects[monster_id] = Marty(monster_id, [400, 200])

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
        #position, velocity, acceleration
        self.pos = pos
        self.dpdt = [0,0]
        self.d2pdt2 = [0,0]

    @staticmethod
    def load_image(srcs):
        def apply_scaling(image):
            return(pytf.scale2x(image))
        return([apply_scaling(pygame.image.load(src)) for src in srcs])


# === TYPES OF WORLD OBJECTS ===
#TODO: What WorldObject types are there? 
#      I think we should split up objects based on their graphical needs.
#      Their graphical needs correspond to common behavior, too.
#      i.e. a player, a monster, background animations, etc, are all
#           going to need a state indicating direction, as well as 
#           methods to flip or transform their images.
#           But static things like blocks, decoration, etc. don't need that stuff
#           and may need to be treated differently.
#      

class DynamicObject(WorldObject):
    '''
    Contains methods for generating animations
    and motion.
    '''
    def __init__(self, *args, **kwargs):
        pass

    def update_spatial_vars(self):
        self.pos  = map(operator.add, self.pos, self.dpdt)
        self.dpdt = map(operator.add, self.dpdt, self.d2pdt2)
        if math.hypot(*self.dpdt) < 1.0:
            self.dpdt = [0,0]




# === TYPES OF INTERACTABLE OBJECTS ===
class Player(DynamicObject):
    standing_image_srcs = ['../Sprites/crusty_running/crusty1.png']
    running_image_srcs  = ['../Sprites/crusty_running/crusty1.png',
                           '../Sprites/crusty_running/crusty2.png']
    
    standing_images = WorldObject.load_image(standing_image_srcs)
    running_images  = WorldObject.load_image(running_image_srcs)

    #TODO: This should be somewhere else... probably in a method
    running_animation = itertools.cycle(running_images)

    def __init__(self, *args, **kwargs):
        WorldObject.__init__(self, *args, **kwargs)
        self.is_running = False
        self.facing_left = False

    #TODO: Remove this.  Only here to test out animation of Player
    #      Can't get it to work and I'm tired.  bed time.  I'll branch nd leave this here.
    def handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        if True == pressed_keys[pygame.K_LEFT] and True == pressed_keys[pygame.K_RIGHT]:
            self.is_running = False
        elif True == pressed_keys[pygame.K_LEFT]:
            self.facing_left = True
            self.is_running = True
            self.dpdt[0] -= 1
        elif True == pressed_keys[pygame.K_RIGHT]:
            self.facing_left = False
            self.is_running = True
            self.dpdt[0] += 1
        else:
            self.is_running = False
            self.dpdt[0] /= 2

        if True == pressed_keys[pygame.K_UP]:
            pass
        elif True == pressed_keys[pygame.K_DOWN]:
            pass


    def get_current_sprite(self):
        self.handle_input()
        self.update_spatial_vars()
        #TODO: Maybe set up states as a key = state, value = action system?
        #TODO: Standardize updating of image and rect attributes.
        if self.is_running:
            self.image = self.running_animation.next()
        else:
            self.image = self.standing_images[0]

        if self.facing_left:
            self.image = pytf.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        return(self)


class Marty(DynamicObject):
    standing_image_srcs   = ['../Sprites/Marty/running1.png']
    running_image_srcs    = ['../Sprites/Marty/running1.png',
                             '../Sprites/Marty/running2.png']
    attacking_image_srcs  = ['../Sprites/Marty/attack1.png',
                             '../Sprites/Marty/attack2.png']
    
    standing_images  = WorldObject.load_image(standing_image_srcs)
    running_images   = WorldObject.load_image(running_image_srcs)
    attacking_images = WorldObject.load_image(attacking_image_srcs)

    #TODO: This should be somewhere else... probably in a method
    running_animation = itertools.cycle(running_images)
    attacking_animation = itertools.cycle(attacking_images)

    def __init__(self, *args, **kwargs):
        WorldObject.__init__(self, *args, **kwargs)
        self.is_running = True
        self.facing_left = False
        self.dpdt[0] = 5

    #change this name.
    def handle_input(self):
        #TODO: Need to add a mechanism for detecting nearby surroundings.
               # see tag [DETECTION]
               # would like to switch to using attacking animation when near
               # a player.
        if self.pos[0] < 40 and self.dpdt[0] < 0:
            self.dpdt[0] *= -1
            self.facing_left = False
        elif self.pos[0] > 800 - 120 and self.dpdt[0] > 0:
            self.dpdt[0] *= -1
            self.facing_left = True

    def get_current_sprite(self):
        self.handle_input()
        self.update_spatial_vars()
        #TODO: Maybe set up states as a key = state, value = action system?
        #TODO: Standardize updating of image and rect attributes.
        if self.is_running:
            self.image = self.running_animation.next()
        else:
            self.image = self.standing_images[0]

        if self.facing_left:
            self.image = pytf.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        return(self)

# === NONINTERACTABLE OBJECTS ===
class GrassBlock(WorldObject):
    '''
    Grass blocks that act as platforms.
    '''
    #Source for the images associated with this class
    image_srcs = ['../Sprites/grass/grass1.png',
                  '../Sprites/grass/grass2.png',
                  '../Sprites/grass/grass3.png']
    sprites = WorldObject.load_image(image_srcs)

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


class SkyBlock(WorldObject):
    '''
    Sky blocks that act as background coloring.  These are
    used to paint the scenery of the World. :3
    '''
    #Source for the images associated with this class
    image_srcs = ['../Sprites/sky/sky1.png']
    sprites = WorldObject.load_image(image_srcs)

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