__author__ = "Charles A. Parker", "Tristan Q. Storz", "Robert P. Cope"

import itertools
import pygame
import random
import math
import logging
import operator
import pygame.transform as pytf

world_logger = logging.getLogger(__name__)


class World(object):
    """
    This is the the most basic level class.
    The player can interact with things inside a World.
    World objects are what generate the image seen at any time
    based on the objects inside of that World.  This includes Menus,
    Levels, etc.
    """
    def __init__(self, surface, state_vars):
        """
        """
        self.id_generator = itertools.count()
        self.world_objects = {}
        self.surface = surface
        self.state_vars = state_vars
        self.is_complete = False

    def gen_id(self):
        return self.id_generator.next()

    def receive_events(self, events):
        """
        Takes in events from any source (really should only be
        the function or class that instantiated this World) and
        reacts.  The passed in events are expected to be instances of
        pygame.event.Event
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.is_complete = True
        return True

    def process_events(self):
        pass

    def render_surface(self):
        # TODO: Objects are blitted together in dict order. Need to add concept
        #       of layers to World class to order blitting by depth.
        #       May also want to consider different ways graphics
        #       might be drawn to plan for all use cases.
        #
        #       There is a concept of layering in Sprite.Groups.  Can and probably
        #       should use that and design rendering around that.
        all_sprites = pygame.sprite.RenderPlain(map(lambda obj: obj.get_current_sprite(), self.world_objects.values()))
        all_sprites.update()
        all_sprites.draw(self.surface)

    # TODO: [DETECTION] Need to add a mechanism for an element of
    #       the world to query for other elements of the world.
    #       Maybe something like find_nearby_instance_of_class()?
    #
    #       Would it be beneficial to track objects of interest
    #       and objects of not-interest separately, so a method
    #       like find_nearby_instance... would have a smaller set
    #       to scan?


# TODO: Should we have different types of Worlds -- Menus?  Gameworlds?
#       Or should those be handled separately and have World be exclusively
#       for things like LevelOne?

# TODO: We should probably make each Level their own file.  Should also
#      consider an
class LevelOne(World):
    # TODO: Flesh out the utilities needed to build a Level.  How should
    # levels be created?  Should level maps be created
    def __init__(self, *args, **kwargs):
        World.__init__(self, *args, **kwargs)
        for x in xrange(0, 800, 64):
            id = self.gen_id()
            self.world_objects[id] = GrassBlock(id, (x, 340))
        # TODO: There's certainly a better way than this to draw
        #       backgrounds...
        for y in xrange(0, 340, 64):
            for x in xrange(0, 800, 64):
                id = self.gen_id()
                # TODO: Commented this out since layering doesn't exist.  need to see Player instance.
                # self.world_objects[id] = SkyBlock(id, (x, y))

        player_id = self.gen_id()
        self.world_objects[player_id] = Player(player_id, [200, 200])

        monster_id = self.gen_id()
        self.world_objects[monster_id] = Marty(monster_id, [400, 200])


# === OVERARCHING WORLD OBJECT ===
class WorldObject(pygame.sprite.Sprite):
    # TODO: Need to determine the real purpose of this
    #       class. What needs to be contained in here?
    """
    A WorldObject is any object within a level.
    """
    def __init__(self, identifier, pos, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self, *args, **kwargs)
        self.identifier = identifier
        # position, velocity, acceleration
        self.pos = pos
        self.velocity = [0, 0]
        self.acceleration = [0, 0]

    @staticmethod
    def load_image(sources):
        def apply_scaling(image):
            return pytf.scale2x(image)
        return [apply_scaling(pygame.image.load(src)) for src in sources]


# === TYPES OF WORLD OBJECTS ===
# TODO: What WorldObject types are there?
#       I think we should split up objects based on their graphical needs.
#       Their graphical needs correspond to common behavior, too.
#       i.e. a player, a monster, background animations, etc, are all
#            going to need a state indicating direction, as well as
#            methods to flip or transform their images.
#            But static things like blocks, decoration, etc. don't need that stuff
#            and may need to be treated differently.
#

class DynamicObject(WorldObject):
    """
    Contains methods for generating animations
    and motion.
    """
    def __init__(self, *args, **kwargs):
        WorldObject.__init__(self, *args, **kwargs)
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        pass

    def update_spatial_vars(self):
        self.pos = map(operator.add, self.pos, self.velocity)
        self.velocity = map(operator.add, self.velocity, self.acceleration)
        if self.falling is True:
            self.velocity[1] += 3
        if math.hypot(*self.velocity) < 1.0:
            self.velocity = [0, 0]


# === TYPES OF INTERACTABLE OBJECTS ===
class Player(DynamicObject):
    standing_images_sources = ['../Sprites/crusty_running/crusty1.png']
    running_images_sources = ['../Sprites/crusty_running/crusty1.png',
                              '../Sprites/crusty_running/crusty2.png']

    standing_images = WorldObject.load_image(standing_images_sources)
    running_images = WorldObject.load_image(running_images_sources)

    # TODO: This should be somewhere else... probably in a method
    running_animation = itertools.cycle(running_images)

    def __init__(self, *args, **kwargs):
        DynamicObject.__init__(self, *args, **kwargs)
        self.is_running = False
        self.facing_left = False
        # TODO: implement a more generic set of methods for
        #      modifiying state
        self.falling = True

    # TODO: Remove this.  Only here to test out animation of Player
    def handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        if self.falling is False:
            if True == pressed_keys[pygame.K_LEFT] and True == pressed_keys[pygame.K_RIGHT]:
                self.is_running = False
            elif True == pressed_keys[pygame.K_LEFT]:
                self.facing_left = True
                self.is_running = True
                self.velocity[0] -= 10
            elif True == pressed_keys[pygame.K_RIGHT]:
                self.facing_left = False
                self.is_running = True
                self.velocity[0] += 10
            else:
                self.is_running = False
                self.velocity[0] /= 1.4

        # TODO: Why am I even still playing with this... GET RID OF THIS GROSSNESS!
        if self.velocity[0] < -30 or self.velocity[0] > 30:
            self.velocity[0] /= 2

        if True == pressed_keys[pygame.K_UP]:
            if self.falling is False:
                self.falling = True
                self.velocity[1] -= 30
            pass
        elif True == pressed_keys[pygame.K_DOWN]:
            pass

        # TODO: Get rid of this hard coded stop.
        if self.pos[1] + self.velocity[1] > 270:
            self.pos[1] = 280
            self.velocity[1] = 0
            self.falling = False

    def get_current_sprite(self):
        self.handle_input()
        self.update_spatial_vars()
        # TODO: Maybe set up states as a key = state, value = action system?
        # TODO: Standardize updating of image and rect attributes.
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
    standing_images_sources = ['../Sprites/Marty/running1.png']
    running_images_sources = ['../Sprites/Marty/running1.png',
                              '../Sprites/Marty/running2.png']
    attacking_image_sources = ['../Sprites/Marty/attack1.png',
                               '../Sprites/Marty/attack2.png']

    standing_images = WorldObject.load_image(standing_images_sources)
    running_images = WorldObject.load_image(running_images_sources)
    attacking_images = WorldObject.load_image(attacking_image_sources)

    # TODO: This should be somewhere else... probably in a method
    running_animation = itertools.cycle(running_images)
    attacking_animation = itertools.cycle(attacking_images)

    def __init__(self, *args, **kwargs):
        DynamicObject.__init__(self, *args, **kwargs)
        self.is_running = True
        self.facing_left = False
        self.falling = False
        self.velocity[0] = 5

    # change this name.
    def handle_input(self):
        # TODO: Need to add a mechanism for detecting nearby surroundings.
        #       see tag [DETECTION]
        #       would like to switch to using attacking animation when near
        #       a player.
        if self.pos[0] < 40 and self.velocity[0] < 0:
            self.velocity[0] *= -1
            self.facing_left = False
        elif self.pos[0] > 800 - 120 and self.velocity[0] > 0:
            self.velocity[0] *= -1
            self.facing_left = True

    def get_current_sprite(self):
        self.handle_input()
        self.update_spatial_vars()
        # TODO: Maybe set up states as a key = state, value = action system?
        # TODO: Standardize updating of image and rect attributes.
        if self.is_running:
            self.image = self.running_animation.next()
        else:
            self.image = self.standing_images[0]

        if self.facing_left:
            self.image = pytf.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        return self


# === NONINTERACTABLE OBJECTS ===
class GrassBlock(WorldObject):
    """
    Grass blocks that act as platforms.
    """
    # Source for the images associated with this class
    image_sources = ['../Sprites/grass/grass1.png',
                     '../Sprites/grass/grass2.png',
                     '../Sprites/grass/grass3.png']
    sprites = WorldObject.load_image(image_sources)

    def __init__(self, *args, **kwargs):
        """
        Selects a random sprite to be loaded for each instance.
        Initializes position and rect object for this instance.
        """
        WorldObject.__init__(self, *args, **kwargs)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def get_current_sprite(self):
        return self


class SkyBlock(WorldObject):
    """
    Sky blocks that act as background coloring.  These are
    used to paint the scenery of the World. :3
    """
    # Source for the images associated with this class
    image_sources = ['../Sprites/sky/sky1.png']
    sprites = WorldObject.load_image(image_sources)

    def __init__(self, *args, **kwargs):
        """
        Selects a random sprite to be loaded for this instance.
        Initializes positions and rect object for this instance.
        """
        # TODO: Should this stuff be handled in WorldObject?
        WorldObject.__init__(self, *args, **kwargs)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def get_current_sprite(self):
        return self
