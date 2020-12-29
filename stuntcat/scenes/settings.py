"""
For settings like resolution or other config options
"""

from .scene import Scene


class SettingsScene(Scene):
    """
    Settings Scene class.
    """

    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

    def render(self):
        """
        Render the settings scene as the colour purple.
        """
        self.screen.fill((255, 0, 255))
