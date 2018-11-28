from .scene import Scene


class LoadingScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True

    def render(self):
        self.screen.fill((255, 0, 255))
