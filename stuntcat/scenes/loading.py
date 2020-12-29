"""
Loading module.
"""
import pygame as pg

from .scene import Scene
from ..resources import gfx, music


class LoadingScene(Scene):
    """
    Loading Scene class.
    """

    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True
        self.image = gfx("intro_screen.png", convert=True)
        music("mainmenu.ogg", play=True)

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
        if not pg.mixer.music.get_busy():
            self.next_scene()

    def next_scene(self):
        """
        Progress to next scene.
        """
        self._game.scenes.remove(self)
        self._game.add_cat_scene()
        self.active = False
        music(stop=True)

    def event(self, event):
        """
        Process a pygame event.

        :param event: The event to process.
        """
        if event.type == pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_SPACE):
            self.next_scene()
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.next_scene()
        elif event.type == pg.JOYBUTTONDOWN and event.button in (0, 1):
            self.next_scene()
