from .scene import Scene
from .. resources import gfx, sfx


class LoadingScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True
        self.image = gfx('intro_screen.png', convert_alpha=True)
        self.timer = 0
        sfx('ict_0026.ogg', play=1)

    def render(self):
        self.screen.fill((255, 0, 255))
        self.screen.blit(image, [0,0])

    def tick(self, dt):
    	self.timer += dt
    	if self.timer > 10000:
    		self.active = False

