"""
Fish module
"""
import random

from pygame.sprite import DirtySprite
from pygame.math import Vector2

from stuntcat.resources import gfx


class FlyingObject(DirtySprite):
    """
    Flying Object class for things that are tossed to the cat.
    """
    def __init__(self, group, pos, vel, image):
        DirtySprite.__init__(self, group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.velocity = Vector2(vel)

        self.last_pos = [self.rect.x, self.rect.y]
        self.pos = [self.rect.x, self.rect.y]

    def update(self, *args, **kwargs):
        if self.last_pos != self.pos[:2]:
            self.dirty = True
            self.rect.x = self.pos[0] - 25
            self.rect.y = self.pos[1] - 25
        self.last_pos = self.pos[:2]


class Fish(FlyingObject):
    """
    Fish sprite class.
    """
    colors = ["red", "yellow", "green"]

    def __init__(self, group, pos, vel):
        image = gfx("fish_" + random.choice(Fish.colors) + ".png", convert_alpha=True)
        FlyingObject.__init__(self, group, pos, vel, image)


class NotFish(FlyingObject):
    """
    Not-fish sprite class.
    """
    def __init__(self, group, pos, vel):
        image = gfx('ring.png', convert_alpha=True)
        FlyingObject.__init__(self, group, pos, vel, image)
