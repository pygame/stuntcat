"""
Platformer Module
"""

from os.path import join as path_join

import pymunk
import pytmx

import pygame.mixer
from pygame import Rect
from pygame.sprite import LayeredUpdates

from stuntcat import resources
from stuntcat.scenes.scene import Scene
from . import actions
from . import event_handling
from . import sprite
from . import unicyclecat
from .model import BasicModel
from .simplefsm import SimpleFSM

# constants used in the map
MAP_FIXED = "fixed"
MAP_SPAWN = "player_spawn"
MAP_PLAYER_SPAWN = "player_spawn"
MAP_YARN_SPAWN = "yarn_spawn"

CONTROL = (
    ((actions.LEFT, True), "idle", "move", 1),
    ((actions.LEFT, False), "move", "idle"),
    ((actions.RIGHT, True), "idle", "move", -1),
    ((actions.RIGHT, False), "move", "idle"),
    ((actions.JUMP, True), "move", "jump"),
    ((actions.JUMP, True), "idle", "jump"),
    ((actions.JUMP, False), "*", "idle"),
)


class PlatformerScene(Scene):
    """
    Platformer Scene class.
    """

    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.active = True
        self.fsm = None
        self.space = pymunk.Space()
        self.space.gravity = (0, 1000)
        self.sprites = LayeredUpdates()
        self.event_handler = event_handling.EventQueueHandler()
        self.event_handler.print_controls()
        self.background = resources.gfx("background.png", convert=True)
        self.load()
        pygame.mixer.music.load(resources.music_path("zirkus.ogg"))
        pygame.mixer.music.play(-1)

    def add_static(self, vertices, rect):
        """
        Add static object to scene.

        :param vertices:
        :param rect:
        """
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = rect.x, rect.y
        shape = pymunk.Poly(body, vertices)
        shape.friction = 1.0
        shape.elasticity = 1.0
        self.space.add(body, shape)

    def load(self):
        """
        Load a scene in TMX format.
        """

        def box_vertices(box_x, box_y, width, height):
            top_left = box_x, box_y
            top_right = box_x + width, box_y
            bottom_right = box_x + width, box_y + height
            bottom_left = box_x, box_y + height
            return top_left, top_right, bottom_right, bottom_left

        filename = path_join("data", "maps", "untitled.tmx")
        tmxdata = pytmx.util_pygame.load_pygame(filename)
        for obj in tmxdata.objects:
            if obj.type == MAP_FIXED:
                rect = Rect(obj.x, obj.y, obj.width, obj.height)
                vertices = box_vertices(0, 0, obj.width, obj.height)
                self.add_static(vertices, rect)

            elif obj.type == MAP_YARN_SPAWN:
                ball = sprite.Ball(Rect((obj.x, obj.y), (32, 32)))
                model = BasicModel()
                model.sprites = [ball]
                model.pymunk_objects = ball.pymunk_shapes
                self.add_model(model)
                self.player = model

            elif obj.type == MAP_PLAYER_SPAWN:
                self.player = unicyclecat.build(self.space, self.sprites)
                self.player.position = obj.x, obj.y

        self.fsm = SimpleFSM(CONTROL, "idle")

    def add_model(self, model):
        """
        Add a model.

        :param model: Model to add.
        """
        self.sprites.add(*model.sprites)
        self.space.add(model.pymunk_objects)

    def remove_model(self, model):
        """
        Remove a model.

        :param model: Model to remove.
        """
        self.sprites.remove(*model.sprites)
        self.space.remove(model.pymunk_objects)

    def render(self):
        """
        Render scene to the screen surface.

        """
        surface = self._game.screen
        surface.blit(self.background, (0, 0))
        self.sprites.draw(surface)
        return [surface.get_rect()]

    def tick(self, time_delta):
        """
        Tick the physics and game update loops.
        """
        step_amount = (1 / 30.0) / 30
        for _ in range(30):
            self.space.step(step_amount)
        self.sprites.update(time_delta=time_delta)

    def event(self, event):
        """
        Process an event.

        :param event: The event to process
        """
        events = self.event_handler.process_event(event)
        position = self.player.position

        for evt in events:
            try:
                cmd, arg = self.fsm((evt.button, evt.held))
            except ValueError:
                continue

            if cmd == "move":
                resources.sfx("cat_wheel.ogg", False, True)
                resources.sfx("cat_wheel.ogg", True)
                self.player.accelerate(arg)

            if cmd == "idle":
                self.player.brake()

            elif cmd == "jump":
                resources.sfx("cat_jump.ogg", True)
                self.player.main_body.apply_impulse_at_world_point((0, -600), position)
