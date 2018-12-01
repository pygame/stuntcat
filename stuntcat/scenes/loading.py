from .scene import Scene
from .. resources import gfx, sfx, music_path

import pygame as pg

class LoadingScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True
        self.image = gfx('intro_screen.png', convert_alpha=True)
        self.timer = 0
        pg.mixer.music.load(music_path('ict_0026.ogg'))
        pg.mixer.music.play()

    def render(self):
        self.screen.fill((255, 0, 255))
        self.screen.blit(self.image, [0,0])
        return [self.screen.get_rect()]

    def tick(self, dt):
        self.timer += dt

        if self.timer > 10000:
            self.next()

    def next(self):
        self._game.scenes.remove(self)
        self._game.add_cat_scene()
        self.active = False
        pg.mixer.music.stop()

    def event(self, event):
        if event.type == pg.KEYDOWN:
            self.next()
