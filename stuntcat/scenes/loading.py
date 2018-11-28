from .scene import Scene
import pygame


class LoadingScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Replace with pyg.Font once that's done and pushed
        self.font = pygame.font.Font('stuntcat/data/segoeui.ttf', 56)

        # Loading screen should always be a fallback active scene
        self.active = True

    def render(self):
        self.screen.fill((25, 25, 25))

        t = self.font.render('Loading...', 1, (255, 255, 255))
        self.screen.blit(t,
                         ((self.screen.get_width() - t.get_width()) / 2,
                          (self.screen.get_height() - t.get_height()) / 2))
