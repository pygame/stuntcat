from os.path import join as path_join

import pymunk
import pytmx
from pygame import Rect
from pygame.sprite import LayeredUpdates
import pygame.mixer
from pymunk import Space

from stuntcat import resources
from stuntcat.scenes.scene import Scene
from . import actions
from . import event_handling
from . import sprite
from . import unicyclecat
from .model import BasicModel
from .simplefsm import SimpleFSM

# constants used in the map
map_fixed = "fixed"
map_spawn = "player_spawn"
map_player_spawn = "player_spawn"
map_yarn_spawn = "yarn_spawn"

center = (0, 0)
control = (
    ((actions.LEFT, True), "idle", "move", 1),
    ((actions.LEFT, False), "move", "idle"),
    ((actions.RIGHT, True), "idle", "move", -1),
    ((actions.RIGHT, False), "move", "idle"),
    ((actions.JUMP, True), "move", "jump"),
    ((actions.JUMP, True), "idle", "jump"),
    ((actions.JUMP, False), "*", "idle"),
)


class PlatformerScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = None
        self.active = True

        self.geometry = list()
        self.space = Space()
        self.space.gravity = (0, 1000)
        self.sprites = LayeredUpdates()
        self.event_handler = event_handling.EventQueueHandler()
        self.background = resources.gfx("background.png", convert=True)
        self.load()
        pygame.mixer.music.load(resources.music_path("zirkus.ogg"))
        pygame.mixer.music.play(-1)

    def add_static(self, vertices, rect):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = rect.x, rect.y
        shape = pymunk.Poly(body, vertices)
        shape.friction = 1.0
        shape.elasticity = 1.0
        self.space.add(body, shape)

    def load(self):
        def box_vertices(x, y, w, h):
            lt = x, y
            rt = x + w, y
            rb = x + w, y + h
            lb = x, y + h
            return lt, rt, rb, lb

        filename = path_join("data", "maps", "untitled.tmx")
        tmxdata = pytmx.util_pygame.load_pygame(filename)
        for obj in tmxdata.objects:
            if obj.type == map_fixed:
                rect = Rect(obj.x, obj.y, obj.width, obj.height)
                vertices = box_vertices(0, 0, obj.width, obj.height)
                self.add_static(vertices, rect)

            elif obj.type == map_yarn_spawn:
                ball = sprite.Ball(Rect((obj.x, obj.y), (32, 32)))
                model = BasicModel()
                model.sprites = [ball]
                model.pymunk_objects = ball.pymunk_shapes
                self.add_model(model)
                self.player = model

            elif obj.type == map_player_spawn:
                self.player = unicyclecat.build(self.space, self.sprites)
                self.player.position = obj.x, obj.y

        self.fsm = SimpleFSM(control, "idle")

    def add_model(self, model):
        self.sprites.add(*model.sprites)
        self.space.add(model.pymunk_objects)

    def remove_model(self, model):
        self.sprites.remove(*model.sprites)
        self.space.remove(model.pymunk_objects)

    def render(self):
        surface = self._game.screen
        surface.blit(self.background, (0, 0))
        self.sprites.draw(surface)
        return [surface.get_rect()]

    def tick(self, dt):
        step_amount = (1 / 30.) / 30
        for i in range(30):
            self.space.step(step_amount)
        self.sprites.update(dt)

    def event(self, pg_event):
        events = self.event_handler.process_event(pg_event)
        position = self.player.position

        for event in events:
            try:
                cmd, arg = self.fsm((event.button, event.held))
            except ValueError as e:
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
