"""
Unicycle Cat Module
"""

import logging
from math import radians
from typing import Optional, Tuple, List, Any

import pygame
import pymunk

from stuntcat import resources
from . import model
from .sprite import ShapeSprite

LOGGER = logging.getLogger(__name__)


class CatModel(model.UprightModel):
    """
    Cat model class.
    """

    def __init__(self):
        super().__init__()
        self.normal_rect = pygame.Rect(0, 0, 32, 40)
        self.model_data["move_power"] = 10

        self.feet = None  # type: Optional[pymunk.Body]

    @staticmethod
    def normal_feet_position(position, feet_shape):
        # type: (Tuple[float, float], pymunk.Circle) -> Tuple[float, float]
        """
        Calculates the feet position of our cat.

        :param position: The regular position
        :param feet_shape: The shape of the feet.
        :return: The feet position
        """
        return position[0], position[1] - feet_shape.radius * 0.7


def make_hitbox(body, rect):
    # type: (pymunk.Body, pygame.Rect) -> pymunk.Poly
    """
    Makes a Pymunk hit box from a Pygame rect.

    :param body: the pymunk.Body the hitbox is for.
    :param rect: the pygame.Rect to use.
    """
    vertices = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
    return pymunk.Poly(body, vertices)


def make_body(rect, moment=float("inf")):
    # type: (pygame.Rect, float) -> Tuple[pymunk.Body, pymunk.Poly]
    """
    Make a pymunk body.

    :param rect: The pygame rect.
    :param moment: moment
    """
    body = pymunk.Body() if moment is None else pymunk.Body(1, moment)
    shape = make_hitbox(body, rect)
    return body, shape


def build(space, group):
    # type: (pymunk.Space, pygame.sprite.AbstractGroup) -> CatModel
    """
    Builds our unicycle cat.

    :param space: The pymunk space to put the cat in.
    :param group: The pygame sprite group to put the cat in.
    """
    scale = 2
    normal_rect = pygame.Rect(0, 0, 32 * scale, 40 * scale)
    cat_model = CatModel()
    sprites = []
    pymunk_objects = []

    filter1 = pymunk.ShapeFilter(group=0b000001)

    # Main body
    body_body = pymunk.Body(0.00001, pymunk.inf)
    body_body.position = normal_rect.topleft
    cat_model.main_body = body_body
    pymunk_objects.append(body_body)

    # seat
    seat_body = build_seat(filter1, normal_rect, pymunk_objects, sprites)

    # build feet
    cat_model.feet, feet_sprite = build_feet(
        filter1, normal_rect, pymunk_objects, body_body, seat_body
    )
    sprites.append(feet_sprite)

    # Add motor
    cat_model.motor = pymunk.SimpleMotor(body_body, cat_model.feet, 0.0)
    pymunk_objects.append(cat_model.motor)

    # cat
    cat_body, cat_rect = build_cat(normal_rect, pymunk_objects, sprites)

    # hold cat the the seat
    spring = pymunk.DampedSpring(
        seat_body, cat_body, normal_rect.midtop, cat_rect.midbottom, 0, 1, 0
    )
    pymunk_objects.append(spring)

    # tilt corrector
    spring = pymunk.DampedRotarySpring(body_body, seat_body, radians(0), 60000, 20000)
    spring.collide_bodies = False
    pymunk_objects.append(spring)

    cat_model.sprites = sprites
    cat_model.pymunk_objects = pymunk_objects

    space.add(pymunk_objects)
    group.add(*sprites)

    return cat_model


def build_cat(
    normal_rect,  # type: pygame.Rect
    pymunk_objects,  # type: List[Any]
    sprites,  # type: List[ShapeSprite]
):
    # type: (...) -> Tuple[pymunk.Body, pygame.Rect]
    """
    Build the cat.

    :param normal_rect: The cat's normal rect.
    :param pymunk_objects: The cat's list of pymunk objects.
    :param sprites: The list of pygame sprites for the cat.

    :return: The cat's pymunk Body and pygame Rect hitbox.
    """
    cat_surface = resources.gfx("cat.png", convert_alpha=True)
    cat_rect = pygame.Rect(0, 0, 64, 48)
    cat_body = pymunk.Body()
    cat_shape = make_hitbox(cat_body, cat_rect)
    cat_body.position = normal_rect.x, normal_rect.y - cat_rect.height - 10
    cat_shape.mass = 0.001
    cat_shape.elasticity = 0.1
    cat_shape.friction = 10.0
    cat_shape.filter = pymunk.ShapeFilter(group=0b000010)
    cat_sprite = ShapeSprite(cat_surface, cat_shape, 1.5)
    cat_sprite.layer = 2
    sprites.append(cat_sprite)
    pymunk_objects.append(cat_body)
    pymunk_objects.append(cat_shape)
    return cat_body, cat_rect


def build_feet(
    filter1,  # type: pymunk.ShapeFilter
    normal_rect,  # type: pygame.Rect
    pymunk_objects,  # type: List[Any]
    body_body,  # type: pymunk.Body
    seat_body,  # type: pymunk.Body
):
    # type: (...) -> Tuple[pymunk.Body, pygame.Sprite]
    """
    Builds our unicycle cat's feet.

    :param filter1: The pymunk Shape filter.
    :param normal_rect: The cat's normal rect.
    :param pymunk_objects: The cat's list of pymunk objects.
    :param body_body: The cat's body Pymunk.Body.
    :param seat_body: The unicycle seat's Pymunk.Body.
    """
    radius = normal_rect.width * 0.55
    feet_body = pymunk.Body()
    feet_shape = pymunk.Circle(feet_body, radius, (0, 0))
    feet_shape.mass = 1
    feet_shape.elasticity = 0
    feet_shape.friction = 100
    feet_shape.filter = filter1
    feet_sprite = ShapeSprite(
        resources.gfx("wheel.png", convert_alpha=True), feet_shape
    )
    feet_sprite.layer = 0

    pymunk_objects.append(feet_body)
    pymunk_objects.append(feet_shape)

    # adjust the position of the feet and body
    feet_body.position = normal_rect.midbottom

    # motor and joints for feet
    joint = pymunk.PivotJoint(
        body_body, feet_body, (normal_rect.centerx, normal_rect.bottom - 10), (0, 0)
    )
    pymunk_objects.append(joint)
    joint = pymunk.PivotJoint(
        seat_body, feet_body, (normal_rect.centerx, normal_rect.bottom - 10), (0, 0)
    )
    pymunk_objects.append(joint)
    return feet_body, feet_sprite


def build_seat(
    filter1,  # type: pymunk.ShapeFilter
    normal_rect,  # type: pygame.Rect
    pymunk_objects,  # type: List[Any]
    sprites,  # type: List[ShapeSprite]
):
    # type: (...) -> pymunk.Body
    """
    Builds our unicycle cat's unicycle seat.

    :param filter1: The pymunk Shape filter.
    :param normal_rect: The cat's normal rect.
    :param pymunk_objects: The cat's list of pymunk objects.
    :param sprites: The list of pygame sprites for the cat.
    """
    seat_body = pymunk.Body()
    seat_body.center_of_gravity = normal_rect.midbottom
    seat_body.position = normal_rect.topleft
    seat_shape = make_hitbox(seat_body, normal_rect)
    seat_shape.mass = 0.5
    seat_shape.elasticity = 0
    seat_shape.friction = 2
    seat_shape.filter = filter1
    seat_sprite = ShapeSprite(resources.gfx("seat.png", convert_alpha=True), seat_shape)
    seat_sprite.layer = 1
    sprites.append(seat_sprite)
    pymunk_objects.append(seat_body)
    pymunk_objects.append(seat_shape)
    return seat_body
