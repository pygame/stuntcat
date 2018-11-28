import time

import pygame

from .scenes import LoadingScene


class Game:
    FLAGS = 0
    WIDTH = 1280
    HEIGHT = 720

    FPS = 32

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), self.FLAGS)
        self.clock = pygame.time.Clock()

        self.running = True
        self.scenes = [
            LoadingScene(self)
        ]

    def tick(self, dt):
        for i in self.scenes[::-1]:
            if i.active:
                if not i.tick(dt):
                    break

        self.clock.tick(self.FPS)

    def render(self):
        for i in self.scenes[::-1]:
            if i.active:
                if not i.render():
                    break

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def mainloop(self):
        dt = 0
        while self.running:
            fs = time.time()
            self.tick(dt)
            self.render()
            self.events()
            dt = (time.time() - fs) * 1000

        pygame.quit()
