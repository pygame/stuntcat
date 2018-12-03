from math import degrees

from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.transform import rotozoom, smoothscale
from pymunk import Body, Circle

from stuntcat import resources

ball_mass = 1


class ShapeSprite(Sprite):
    def __init__(self, image=None, shape=None, factor=1.0):
        super(ShapeSprite, self).__init__()
        self.original_image = image
        self.shape = shape
        self._old_angle = None
        self.image = None
        self.rect = None
        if shape and image:
            bb = shape.cache_bb()
            size = int((bb.right - bb.left) * factor), int((bb.top - bb.bottom) * factor)
            self.original_image = smoothscale(image, size)

    def update(self, dt):
        if hasattr(self.shape, "needs_remove"):
            self.kill()
        else:
            angle = round(degrees(self.shape.body.angle), 0)
            if not angle == self._old_angle:
                self.image = rotozoom(self.original_image, -angle, 1)
                self.rect = self.image.get_rect()
                self._old_angle = angle
                self.dirty = 1

            self.rect.center = self.shape.bb.center()


class Ball(ShapeSprite):
    def __init__(self, rect):
        super(Ball, self).__init__()
        radius = rect.width / 2
        body = Body()
        body.position = rect.center
        self.shape = Circle(body, radius)
        self.shape.mass = ball_mass
        self.shape.elasticity = .25
        self.shape.friction = 1
        self.rect = Rect(0, 0, rect.width, rect.width)
        self.original_image = resources.gfx("yarnball.png", convert_alpha=True)
        self.pymunk_shapes = (body, self.shape)
