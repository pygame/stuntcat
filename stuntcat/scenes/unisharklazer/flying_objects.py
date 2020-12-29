"""
Fish module
"""
import math
import random

from pygame.sprite import DirtySprite
from pygame.math import Vector2

from stuntcat.resources import gfx, sfx, distance


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

        dt_scaled = kwargs["time_delta"]
        height = kwargs["height"]

        self.pos[0] += self.velocity[0] * dt_scaled  # speed of the throw
        self.velocity[1] += 0.2 * dt_scaled  # gravity
        self.pos[1] += self.velocity[1] * dt_scaled  # y velocity
        # check out of bounds
        if self.pos[1] > height:
            self.kill()


class Fish(FlyingObject):
    """
    Fish sprite class.
    """

    colors = ["red", "yellow", "green"]

    def __init__(self, group, pos, vel):
        image = gfx("fish_" + random.choice(Fish.colors) + ".png", convert_alpha=True)
        FlyingObject.__init__(self, group, pos, vel, image)

    def update(self, *args, **kwargs):
        FlyingObject.update(self, *args, **kwargs)

        if (
            distance(
                [self.rect[0], self.rect[1]], kwargs["player_data"].cat_head_location
            )
            < 100
        ):
            kwargs["player_data"].increment_score()
            self.kill()
            sfx("eatfish.ogg", play=1)


class NotFish(FlyingObject):
    """
    Not-fish sprite class.
    """

    def __init__(self, group, pos, vel):
        image = gfx("ring.png", convert_alpha=True)
        FlyingObject.__init__(self, group, pos, vel, image)

    def update(self, *args, **kwargs):
        FlyingObject.update(self, *args, **kwargs)

        if (
            distance(
                [self.rect[0], self.rect[1]], kwargs["player_data"].cat_head_location
            )
            < 50
        ):
            self.kill()
            kwargs["player_data"].angle_to_not_fish = (
                math.atan2(
                    kwargs["player_data"].cat_head_location[1] - self.rect[1],
                    kwargs["player_data"].cat_head_location[0] - self.rect[0],
                )
                - math.pi / 2
            )
            side = 1 if kwargs["player_data"].angle_to_not_fish < 0 else -1
            kwargs["player_data"].cat_angular_vel += side * random.uniform(0.08, 0.15)
