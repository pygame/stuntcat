""" For showing news updates from a server.
"""

from .scene import Scene


class NewsScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

    def render(self):
        self.screen.fill((255, 0, 255))
