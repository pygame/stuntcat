"""
Elephant module
"""
import pygame
import pygame.draw

from pygame.surface import Surface
from pygame.sprite import DirtySprite, collide_rect

from stuntcat.resources import sfx


class ElephantAnimation:
    """
    Handles the elephant animations
    """

    def __init__(self):

        self.current_state = 0
        self.states = {
            0: "offscreen",
            1: "poise left",
            2: "stomp left",
            3: "offscreen",
            4: "poise right",
            5: "stomp right",
        }
        self.last_state = 0

        self.action_times = {
            "between_stomps": 1500,  # ms
            "poise": 1500,  # ms
            "stomp": 1500,  # ms
        }
        self.last_animation = 0  # ms
        self.just_happened = None

    def update(self, total_time):
        """
        Update the animation.
        """
        state = self.states[self.current_state]
        start_state = self.current_state
        if state == "offscreen":
            self.update_single_action(
                state, total_time, self.action_times["between_stomps"]
            )
        elif state in ["poise left", "poise right"]:
            self.update_single_action(state, total_time, self.action_times["poise"])
        elif state in ["stomp left", "stomp right"]:
            finished = self.update_single_action(
                state, total_time, self.action_times["stomp"]
            )
            if finished and self.current_state == max(self.states.keys()) + 1:
                self.current_state = 0

        self.last_state = start_state

    def update_single_action(self, state, total_time, action_time):
        """
        Animate a single elephant action.

        :param state: animation state.
        :param total_time: Current time.
        :param action_time: Duration of the action.

        :return: True if finished
        """
        finished = False
        just_happened = self.current_state != self.last_state
        self.just_happened = state if just_happened else None
        if total_time > self.last_animation + action_time:
            self.current_state += 1
            self.last_animation = total_time
            finished = True
        return finished


class Elephant(DirtySprite):
    """
    Elephant sprite class.
    """

    def __init__(self, scene):
        DirtySprite.__init__(self)

        self.scene = scene

        self.animation = ElephantAnimation()

        # stamp.
        sfx("foot_elephant.ogg")

        self.rect = pygame.Rect([0, 0, self.scene.width // 2, self.scene.height])
        self.image = Surface((self.rect[2], self.rect[3])).convert()
        self.image.fill((255, 0, 0))

        self.rect.x = -1000
        self.rect.y = -1000

    def animate(self, total_time):
        """
        Animate the elephant
        """
        self.animation.update(total_time)

    def update(self, *args, **kwargs):
        """
        Update the elephant.
        """
        # if self.animation.just_happened is not None:
        #     print(self.animation.just_happened)
        from_top = 100

        if self.animation.just_happened == "offscreen":
            self.dirty = True
            self.rect.x = -1000
            self.rect.y = -1000
            sfx("foot_elephant.ogg", stop=1)
        elif self.animation.just_happened == "poise left":
            self.rect.x = 0
            self.rect.y = from_top - self.scene.height
            self.dirty = True
            sfx("foot_elephant.ogg", play=1)
        elif self.animation.just_happened == "stomp left":
            # (self.height - self.image.get_height()) - self.scene.cat_wire_height
            self.rect.y = self.scene.cat_wire_height - self.scene.height
            self.rect.x = 0
            self.dirty = True

            if collide_rect(self, self.scene.cat):
                self.scene.reset_on_death()
                self.dirty = True

        elif self.animation.just_happened == "poise right":
            self.rect.x = self.scene.width // 2
            self.rect.y = from_top - self.scene.height
            self.dirty = True
            sfx("foot_elephant.ogg", play=1)
        elif self.animation.just_happened == "stomp right":
            self.rect.x = self.scene.width // 2
            self.rect.y = self.scene.cat_wire_height - self.scene.height
            self.dirty = True
            if collide_rect(self, self.scene.cat):
                self.scene.reset_on_death()
                self.dirty = True

    def render(self, screen, width, height):
        """
        Render the elephant.

        :param screen:
        :param width:
        :param height:
        """
        if self.animation.current_state == 1:  # poise left
            pygame.draw.polygon(
                screen,
                [255, 0, 0],
                [
                    [0.1 * width, 0],
                    [0.5 * width, 0],
                    [0.5 * width, 100],
                    [0.1 * width, 100],
                ],
            )
        if self.animation.current_state == 2:  # stomp left
            pygame.draw.polygon(
                screen,
                [255, 0, 0],
                [
                    [0.1 * width, 0],
                    [0.5 * width, 0],
                    [0.5 * width, height - 100],
                    [0.1 * width, height - 100],
                ],
            )
        if self.animation.current_state == 4:  # poise right
            pygame.draw.polygon(
                screen,
                [255, 0, 0],
                [
                    [0.5 * width, 0],
                    [0.9 * width, 0],
                    [0.9 * width, 100],
                    [0.5 * width, 100],
                ],
            )
        if self.animation.current_state == 5:  # stomp right
            pygame.draw.polygon(
                screen,
                [255, 0, 0],
                [
                    [0.5 * width, 0],
                    [0.9 * width, 0],
                    [0.9 * width, height - 100],
                    [0.5 * width, height - 100],
                ],
            )

    def collide(self, width):
        """
        Collide with the elephant.

        :param width:
        """
        state = self.animation.states[self.animation.current_state]
        if state == "stomp left":
            if self.scene.cat_head_location[0] < width / 2:
                self.scene.reset_on_death()
                self.dirty = True
        elif state == "stomp right":
            if self.scene.cat_head_location[0] > width / 2:
                self.scene.reset_on_death()
                self.dirty = True
