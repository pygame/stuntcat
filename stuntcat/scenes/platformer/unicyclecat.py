import logging
from math import radians

import pygame
import pymunk

from stuntcat import resources
from . import model
from .sprite import ShapeSprite

logger = logging.getLogger(__name__)


class CatModel(model.UprightModel):
    def __init__(self):
        super().__init__()
        self.normal_rect = pygame.Rect(0, 0, 32, 40)
        self.normal_feet_offset = (0, .7)
        self.move_power = 10
        self.jump_power = 30000
        self.jump_mod = 1.0

    @staticmethod
    def normal_feet_position(position, feet_shape):
        return position[0], position[1] - feet_shape.radius * .7


def make_hitbox(body, rect):
    vertices = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
    return pymunk.Poly(body, vertices)


def make_body(rect, moment=pymunk.inf):
    if moment is None:
        body = pymunk.Body()
    else:
        body = pymunk.Body(1, moment)
    shape = make_hitbox(body, rect)
    return body, shape


def build(space, group):
    scale = 2
    normal_rect = pygame.Rect(0, 0, 32 * scale, 40 * scale)
    model = CatModel()
    sprites = list()
    pymunk_objects = list()

    seat_surface = resources.gfx("seat.png", convert_alpha=True)
    feet_surface = resources.gfx("wheel.png", convert_alpha=True)

    filter1 = pymunk.ShapeFilter(group=0b000001)
    filter2 = pymunk.ShapeFilter(group=0b000010)

    # Main body
    body_body = pymunk.Body(0.00001, pymunk.inf)
    body_body.position = normal_rect.topleft
    model.main_body = body_body
    pymunk_objects.append(body_body)

    # seat
    seat_body = pymunk.Body()
    seat_body.center_of_gravity = normal_rect.midbottom
    seat_body.position = normal_rect.topleft
    seat_shape = make_hitbox(seat_body, normal_rect)
    seat_shape.mass = .5
    seat_shape.elasticity = 0
    seat_shape.friction = 2
    seat_shape.filter = filter1
    seat_sprite = ShapeSprite(seat_surface, seat_shape)
    seat_sprite._layer = 1
    sprites.append(seat_sprite)
    pymunk_objects.append(seat_body)
    pymunk_objects.append(seat_shape)

    # build feet
    radius = normal_rect.width * .55
    feet_body = pymunk.Body()
    model.feet = feet_body
    feet_shape = pymunk.Circle(feet_body, radius, (0, 0))
    feet_shape.mass = 1
    feet_shape.elasticity = 0
    feet_shape.friction = 100
    feet_shape.filter = filter1
    feet_sprite = ShapeSprite(feet_surface, feet_shape)
    feet_sprite._layer = 0
    sprites.append(feet_sprite)
    pymunk_objects.append(feet_body)
    pymunk_objects.append(feet_shape)

    # adjust the position of the feet and body
    feet_body.position = normal_rect.midbottom

    # motor and joints for feet
    motor = pymunk.SimpleMotor(body_body, feet_body, 0.0)
    model.motor = motor
    pymunk_objects.append(motor)
    x, y = normal_rect.midbottom
    y -= 10
    joint = pymunk.PivotJoint(body_body, feet_body, (x, y), (0, 0))
    pymunk_objects.append(joint)
    joint = pymunk.PivotJoint(seat_body, feet_body, (x, y), (0, 0))
    pymunk_objects.append(joint)

    # cat
    cat_surface = resources.gfx("cat.png", convert_alpha=True)
    cat_rect = pygame.Rect(0, 0, 64, 48)
    cat_body = pymunk.Body()
    cat_shape = make_hitbox(cat_body, cat_rect)
    cat_body.position = normal_rect.x, normal_rect.y - cat_rect.height - 10
    cat_shape.mass = 0.001
    cat_shape.elasticity = .1
    cat_shape.friction = 10.0
    cat_shape.filter = filter2
    cat_sprite = ShapeSprite(cat_surface, cat_shape, 1.5)
    cat_sprite._layer = 2
    sprites.append(cat_sprite)
    pymunk_objects.append(cat_body)
    pymunk_objects.append(cat_shape)

    # hold cat the the seat
    spring = pymunk.DampedSpring(seat_body, cat_body, normal_rect.midtop, cat_rect.midbottom, 0, 1, 0)
    pymunk_objects.append(spring)

    # tilt corrector
    spring = pymunk.DampedRotarySpring(body_body, seat_body, radians(0), 60000, 20000)
    spring.collide_bodies = False
    pymunk_objects.append(spring)

    model.sprites = sprites
    model.pymunk_objects = pymunk_objects

    space.add(pymunk_objects)
    group.add(*sprites)

    return model
