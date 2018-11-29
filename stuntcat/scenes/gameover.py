""" For when the game is over.
"""

from .scene import Scene


class GameOverScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

    def render(self):
        self.screen.fill((255, 0, 255))
