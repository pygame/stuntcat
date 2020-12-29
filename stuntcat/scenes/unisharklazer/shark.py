"""Shark with frickn lazers.
"""

import pygame
from pygame.sprite import DirtySprite

from stuntcat.resources import gfx, sfx, music


class Lazer(DirtySprite):
    """
    lazer sprite class.
    """

    def __init__(self, container, shark_size):
        DirtySprite.__init__(self, container)
        self.rect = pygame.Rect([150, shark_size[1] - 155, shark_size[0], 10])
        # self.rect.x = -1000
        self.image = pygame.transform.scale(
            gfx("shark_laser.png", convert_alpha=True), self.rect.size
        )


class Shark(DirtySprite):  # pylint:disable=too-many-instance-attributes
    """
    Shark sprite class.
    """

    def __init__(self, container, scene, width, height):
        DirtySprite.__init__(self, container)
        self.debug = False
        self.container = container
        self.scene = scene
        self.width, self.height = width, height

        self.state = 0  #
        self.states = {
            0: "offscreen",
            1: "about_to_appear",
            2: "poise",
            3: "aiming",
            4: "fire laser",
            5: "leaving",
        }
        self.last_state = 0
        self.just_happened = None
        self.lazered = False  # was the cat hit?
        self.lazer = None  # type: Optional[Lazer]
        self.laser_height = height - 150  # where should the laser be on the screen?

        # TODO: to make it easier to test the shark
        #        self.time_between_appearances = 1000 #ms
        # self.time_between_appearances = 5000 #ms

        # self.time_of_about_to_appear = 1000#ms
        # self.time_of_poise = 1000 #ms
        # self.time_of_aiming = 500 #ms
        # self.time_of_laser = 200 #ms
        # self.time_of_leaving = 1000 #ms

        self.timings = {
            "time_between_appearances": 5000,
            "time_of_about_to_appear": 1000,
            "time_of_poise": 1000,
            "time_of_aiming": 500,
            "time_of_laser": 200,
            "time_of_leaving": 1000,
        }
        self.last_animation = 0  # ms

        self.applaud = True

        sfx("default_shark.ogg")
        sfx("shark_appear.ogg")
        sfx("shark_gone.ogg")
        sfx("shark_lazer.ogg")
        sfx("applause.ogg")
        sfx("cat_shot.ogg")
        sfx("boo.ogg")

        self.image = gfx("shark.png", convert_alpha=True)
        # gfx('foot_part.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = self.height - self.image.get_height()

    def update(self, *args, **kwargs):

        if self.debug and self.just_happened:
            print(self.just_happened)

        if self.just_happened == "offscreen":
            sfx("shark_gone.ogg", stop=1)

            self.rect.x = -1000
            self.dirty = True

        elif self.just_happened == "about_to_appear":
            music(stop=True)
            self.applaud = True
            sfx("shark_appear.ogg", play=1)

        elif self.just_happened == "poise":
            sfx("shark_attacks.ogg", play=1)

            self.rect.x = -30
            self.dirty = True

        elif self.just_happened == "fire laser":
            self.fire_laserbeam(self.debug)

        elif self.just_happened == "leaving":
            sfx("shark_appear.ogg", fadeout=3500)
            sfx("shark_attacks.ogg", stop=1)
            sfx("shark_gone.ogg", play=1)
            self.dirty = True
            if self.lazered:
                sfx("boo.ogg", play=True)
                self.scene.reset_on_death()
                self.lazered = False
                self.scene.annoy_crowd()
            elif self.applaud:
                sfx("applause.ogg", play=1)
            if self.lazer:
                self.lazer.kill()
                self.lazer = None

    def fire_laserbeam(self, debug):
        """
        Fires the shark's head mounted laser cannon.

        :param debug:
        """
        if debug:
            print(self.just_happened)
        self.lazer = Lazer(self.container, (self.width, self.height))

        sfx("shark_lazer.ogg", play=1)

        if (
            self.scene.player_data.cat_location[1]
            > self.scene.player_data.cat_wire_height - 3
        ):
            sfx("cat_shot.ogg", play=1)

            self.lazered = True
        else:
            self.lazered = False

    def _update_last_animation(self, total_time, timing):
        """"""
        if total_time > self.last_animation + self.timings[timing]:
            self.state += 1
            self.last_animation = total_time

    def animate(self, total_time):
        """
        Animate method.

        :param total_time:
        """
        # print('update', self.states[self.state], self.states[self.last_state])
        state = self.states[self.state]
        start_state = self.state

        if state == "offscreen":
            self.just_happened = state if self.state != self.last_state else None
            self._update_last_animation(total_time, "time_between_appearances")

        elif state == "about_to_appear":
            self.just_happened = state if self.state != self.last_state else None
            self._update_last_animation(total_time, "time_of_about_to_appear")

        elif state == "poise":
            self.just_happened = state if self.state != self.last_state else None

            # smoothly animate upwards
            self.rect.y = (self.height - self.image.get_height()) + 0.2 * (
                self.last_animation + self.timings["time_of_poise"] - total_time
            )
            self.dirty = True

            self._update_last_animation(total_time, "time_of_poise")

        elif state == "aiming":
            self.just_happened = state if self.state != self.last_state else None
            self._update_last_animation(total_time, "time_of_aiming")

        elif state == "fire laser":
            self.just_happened = state if self.state != self.last_state else None
            self._update_last_animation(total_time, "time_of_laser")

        elif state == "leaving":
            self.just_happened = state if self.state != self.last_state else None

            # smoothly animate downwards
            self.rect.y = (self.height - self.image.get_height()) + 0.2 * (
                total_time - self.last_animation
            )
            self.dirty = True

            if total_time > self.last_animation + self.timings["time_of_leaving"]:
                self.state += 1
                if self.state == max(self.states.keys()) + 1:
                    self.state = 0
                self.last_animation = total_time

        self.last_state = start_state

    def set_state(self, new_state):
        """set the state number from the name """
        self.state = list(self.states.values()).index(new_state)

    def get_state(self):
        """get state name"""
        return self.states[self.state]

    def collide(self, scene, width, height, cat_location):
        """ TODO: this doesn't work. It means the laser never fires."""
        # if self.state == 2:
        #     if cat_location[1] > height - 130:
        #         print('shark collide')
        #         scene.reset_on_death()
