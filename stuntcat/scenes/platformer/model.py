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

    @property
    def position(self):
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


class UprightModel(BasicModel):
    def __init__(self):
        super().__init__()
        self.move_power = 1
        self.jump_power = 1
        self.motor = None
        self._debounce_time = 0
        self._grounded = False

    @property
    def grounded(self):
        return self._grounded

    @grounded.setter
    def grounded(self, value):
        value = bool(value)
        self._grounded = value

    def accelerate(self, direction):
        amt = direction * self.move_power
        self.motor.max_force = pymunk.inf
        self.motor.rate = amt

    def brake(self):
        self.motor.rate = 0
        self.motor.max_force = 300000
