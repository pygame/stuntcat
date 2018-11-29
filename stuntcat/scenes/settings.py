""" For settings like resolution or other config options
"""

from .scene import Scene


class SettingsScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

    def render(self):
        self.screen.fill((255, 0, 255))
