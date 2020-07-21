from .scene import Scene
from .. resources import gfx, sfx, music

import pygame as pg

class LoadingScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True
        self.image = gfx('intro_screen.png', convert=True)
        music('mainmenu.ogg', play=True)

    def render(self):
        self.screen.fill((255, 0, 255))
        self.screen.blit(self.image, [0,0])
        return [self.screen.get_rect()]

    def tick(self, dt):
        if not pg.mixer.music.get_busy():
            self.next()

    def next(self):
        self._game.scenes.remove(self)
        self._game.add_cat_scene()
        self.active = False
        music(stop=True)

    def event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN, pg.K_SPACE):
                self.next()
        if event.type == pg.MOUSEBUTTONDOWN:
            self.next()
        if event.type == pg.JOYBUTTONDOWN:
            if event.button in (0, 1):
                self.next()
