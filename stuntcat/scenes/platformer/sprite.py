"""
Sprite Module
"""

from math import degrees

from pygame.rect import Rect
from pygame.sprite import DirtySprite
from pygame.transform import rotozoom, smoothscale
from pymunk import Body, Circle

from stuntcat import resources

BALL_MASS = 1


class ShapeSprite(DirtySprite):
    """
    Shape sprite class.
    """

    def __init__(self, image=None, shape=None, factor=1.0):
        DirtySprite.__init__(self)
        self.original_image = image
        self.shape = shape
        self._old_angle = None
        self.image = None
        self.rect = None
        if shape and image:
            bounding_box = shape.cache_bb()
            size = (
                int((bounding_box.right - bounding_box.left) * factor),
                int((bounding_box.top - bounding_box.bottom) * factor),
            )
            self.original_image = smoothscale(image, size)

    def update(self, *args, **kwargs):
        """
        Update the shape sprite.

        """
        if hasattr(self.shape, "needs_remove"):
            self.kill()
        else:
            angle = round(degrees(self.shape.body.angle), 0)
            if angle != self._old_angle:
                self.image = rotozoom(self.original_image, -angle, 1)
                self.rect = self.image.get_rect()
                self._old_angle = angle
                self.dirty = 1

            self.rect.center = self.shape.bb.center()


class Ball(ShapeSprite):
    """
    Ball class.
    """

    def __init__(self, rect):
        ShapeSprite.__init__(self)

        radius = rect.width / 2
        body = Body()
        body.position = rect.center
        self.shape = Circle(body, radius)
        self.shape.mass = BALL_MASS
        self.shape.elasticity = 0.25
        self.shape.friction = 1
        self.rect = Rect(0, 0, rect.width, rect.width)
        self.original_image = resources.gfx("yarnball.png", convert_alpha=True)
        self.pymunk_shapes = (body, self.shape)
