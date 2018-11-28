class Scene:
    def __init__(self, game):
        self.active = False

        self.screen = game.screen
        self._game = game

    def render(self):
        pass

    def tick(self, dt):
        pass

    def event(self, event):
        pass
