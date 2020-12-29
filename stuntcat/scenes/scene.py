"""
Scene module.
"""


class Scene:
    """
    Scene class.
    """

    def __init__(self, game):
        self.active = False

        self.screen = game.screen
        self._game = game

    def render(self):
        """
        Render the scene.
        """

    def tick(self, time_delta):
        """
        Tick the scene.

        :param time_delta: The time delta.
        """

    def event(self, event):
        """
        Process a pygame event.

        :param event: The event to process.
        """
