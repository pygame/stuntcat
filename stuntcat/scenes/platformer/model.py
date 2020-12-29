"""
Model Module
"""
from typing import Dict, Any
import pymunk


class BasicModel:
    """
    * Models can track body and may have multiple sprites.
    * Models are not drawn, but can be thought of as
      containers for ShapeSprites and manage pymunk object references.
    * Models should implement high-level functions for groups
      of related shapes/bodies/joints
    """

    def __init__(self):
        self.main_body = None
        self.pymunk_objects = set()
        self.sprites = set()
        self.model_data = {}  # type: Dict[str, Any]

    @property
    def position(self):
        """
        Position property.

        :return: The model's position.
        """
        return self.main_body.position

    @position.setter
    def position(self, value):
        position = pymunk.Vec2d(*value)
        delta = position - self.main_body.position
        for obj in self.pymunk_objects:
            try:
                obj.position += delta
            except AttributeError:
                continue

    def list_objects(self):
        """
        Print out the set of pymunk objects that make up this body.
        """
        print(self.pymunk_objects)


class UprightModel(BasicModel):
    """
    Upright Model class.
    """

    def __init__(self):
        super().__init__()
        self.model_data["move_power"] = 1
        self.motor = None
        self._debounce_time = 0
        self._grounded = False

    @property
    def grounded(self):
        """
        Grounded property.

        :return: True if grounded.
        """
        return self._grounded

    @grounded.setter
    def grounded(self, value):
        value = bool(value)
        self._grounded = value

    def accelerate(self, direction):
        """
        Accelerate in a direction.

        :param direction: The direction to go.
        """
        amt = direction * self.model_data["move_power"]
        self.motor.max_force = pymunk.inf
        self.motor.rate = amt

    def brake(self):
        """
        Put on the brakes.
        """
        self.motor.rate = 0
        self.motor.max_force = 300000
