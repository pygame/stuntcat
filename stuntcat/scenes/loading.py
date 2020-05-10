"""
Loading module.
"""

import pygame as pg

from .scene import Scene
from .. resources import gfx, music


class LoadingScene(Scene):
    """
    Loading Scene class.
    """
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True
        self.image = gfx('intro_screen.png', convert_alpha=True)
        self.timer = 0
        music('ict_0026.ogg', play=True)

    def render(self):
        """
        Render the scene.
        """
        self.screen.fill((255, 0, 255))
        self.screen.blit(self.image, [0, 0])
        return [self.screen.get_rect()]

    def tick(self, time_delta):
        """
        Tick the scene.

        :param time_delta: The time delta.
        """
        self.timer += time_delta

        if self.timer > 10000:
            self.next()

    def next(self):
        """
        Progress to next scene.
        """
        self._game.scenes.remove(self)
        self._game.add_cat_scene()
        self.active = False
        music(stop=True)

    def event(self, pg_event):
        """
        Process a pygame event.

        :param pg_event: The event to process.
        """
        if pg_event.type == pg.KEYDOWN:
            self.next()
