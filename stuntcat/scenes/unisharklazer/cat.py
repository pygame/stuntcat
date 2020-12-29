"""A cat riding a unicycle.
"""

import math

import pygame
from pygame.sprite import DirtySprite

from stuntcat.resources import gfx, sfx


class AnimatedCat(DirtySprite):
    """Handle animations for the cat."""

    def __init__(self):
        DirtySprite.__init__(self)

        self.last_location = [0, 0]
        self.last_direction = True  # right is true
        self.last_rotation = -1
        self.last_frame = None

        self.frame = 1
        self.frame_rate = 750  # time passed in ms before frame changes
        self.frame_time = 0
        self.frame_direction = True  # True = increasing, False = decreasing

        self.num_frames = 4

    def changed(self, location, direction, rotation, frame):
        """Has the cat state changed? Store the last state."""
        changed = (
            self.last_rotation != rotation
            or self.last_location != location
            or self.last_frame != self.frame
        )

        self.last_location = location
        self.last_direction = direction
        self.last_rotation = rotation
        self.last_frame = frame

        return changed

    def animate(self, time_delta):
        """Animate the sprite."""
        self.frame_time += time_delta
        if self.frame_time >= self.frame_rate:
            if self.frame_direction:
                self.frame += 1
            else:
                self.frame -= 1
            self.frame_time = 0
            if self.frame == self.num_frames or self.frame == 1:
                self.frame_direction = not self.frame_direction


class Cat(AnimatedCat):
    """Cat sprite class."""

    def __init__(self, cat_holder):
        AnimatedCat.__init__(self)
        self.cat_holder = cat_holder
        self.image = gfx("cat_unicycle1.png", convert_alpha=True)
        self.rect = self.image.get_rect()
        sfx("cat_jump.ogg")

        self.images = []
        self.flipped_images = []

        for i in range(self.num_frames):
            img = gfx("cat_unicycle%d.png" % (i + 1), convert_alpha=True)
            self.images.append(img)
            self.flipped_images.append(pygame.transform.flip(img, 1, 0))

    def get_image(self):
        """Return the image for the animated frame"""
        return (self.images, self.flipped_images)[
            self.cat_holder.player_data.cat_speed[0] < 0
        ][self.frame - 1]

    def update(self, *args, **kwargs):
        direction = self.cat_holder.player_data.cat_speed[0] > 0
        location = self.cat_holder.player_data.cat_head_location
        rotation = self.cat_holder.player_data.cat_angle

        if self.last_direction != direction:
            self.dirty = True
            self.image = self.get_image()

        if self.changed(location[:], direction, rotation, self.frame):
            self.image = pygame.transform.rotate(
                self.get_image(), -self.cat_holder.player_data.cat_angle * 180 / math.pi
            )
            size = self.image.get_rect().size
            self.dirty = True
            self.rect.x = int(location[0]) - size[0] * 0.5
            self.rect.y = int(location[1]) - size[1] * 0.5
