import pygame
import math
import random
from pygame.locals import *

from .scene import Scene


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class CatUniScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)

        # Loading screen should always be a fallback active scene
        self.active = True

        self.myfont = pygame.font.SysFont("monospace", 20)

        (width, height) = (1000, 600)
        self.width, self.height = width, height

        self.cat_location = [width / 2, height - 100]
        self.cat_speed = [0, 0]
        self.cat_speed_max = 8
        self.cat_fall_speed_max = 16
        self.cat_angle = 0
        self.cat_angular_vel = 0
        self.time_elapsed = 0
        self.left_pressed = False
        self.right_pressed = False
        self.score = 0

        self.dt_scaled = 0

        # lists of things to catch by [posx, posy, velx, vely]
        self.fish = [[0, height / 2, 10, -5]]
        self.not_fish = [[width, height / 2, -5, -2]]

    def render(self):
        screen = self.screen
        width, height = self.width, self.height

        background_colour = (0, 0, 0)
        screen.fill(background_colour)

        # draw cat
        pygame.draw.line(
            screen, [0, 0, 255], self.cat_location, self.cat_head_location, 20
        )
        pygame.draw.circle(screen, [0, 0, 255], self.cat_head_location, 50, 1)
        pygame.draw.circle(screen, [0, 255, 0], self.cat_head_location, 100, 1)

        # draw dead zones
        pygame.draw.polygon(
            screen,
            [255, 0, 0],
            [
                [0, height - 100],
                [0.1 * width, height - 100],
                [0.1 * width, height],
                [0, height],
            ],
        )
        pygame.draw.polygon(
            screen,
            [255, 0, 0],
            [
                [0.9 * width, height - 100],
                [width, height - 100],
                [width, height],
                [0.9 * width, height],
            ],
        )

        # draw fish and not fish
        for f in self.fish:
            pygame.draw.circle(screen, [0, 255, 0], [int(f[0]), int(f[1])], 10)
        for f in self.not_fish:
            pygame.draw.circle(screen, [255, 0, 0], [int(f[0]), int(f[1])], 10)

        # draw score
        textsurface = self.myfont.render(
            "score : " + str(self.score), True, [255, 255, 255]
        )
        screen.blit(textsurface, (100, 100))

        # pygame.display.flip()
        # time_elapsed = clock.tick(60)

    def tick(self, dt):
        dt_scaled = dt/17
        self.dt_scaled = dt_scaled
        width, height = self.width, self.height

        ##cat physics
        self.cat_angular_vel *= 0.9**dt_scaled #max(0.9/(max(0.1,dt_scaled)),0.999)

        # add gravity
        self.cat_speed[1] = min(self.cat_speed[1] + (1 * dt_scaled), self.cat_fall_speed_max)

        # accelerate the cat left or right
        if self.right_pressed:
            self.cat_speed[0] = min(
                self.cat_speed[0] + 0.3 * dt_scaled, self.cat_speed_max
            )
            self.cat_angle -= 0.01 * dt_scaled

        if self.left_pressed:
            self.cat_speed[0] = max(
                self.cat_speed[0] - 0.3 * dt_scaled, -self.cat_speed_max
            )
            self.cat_angle += 0.01 * dt_scaled

        # make the cat fall
        self.cat_angular_vel += 0.001 * self.cat_angle * dt_scaled
        self.cat_angle += self.cat_angular_vel * dt_scaled
        if self.cat_angle > math.pi / 2 or self.cat_angle < -math.pi / 2:
            self.cat_location = [width / 2, height - 100]
            self.cat_speed = [0, 0]
            self.cat_angle = 0
            self.cat_angular_vel = 0
            self.score = 0

        # move cat
        self.cat_location[0] += self.cat_speed[0] * dt_scaled
        self.cat_location[1] += self.cat_speed[1] * dt_scaled
        if self.cat_location[1] > height - 100:
            self.cat_location[1] = height - 100
            self.cat_speed[1] = 0
        self.cat_head_location = [
            int(self.cat_location[0] + 100 * math.cos(self.cat_angle - math.pi / 2)),
            int(self.cat_location[1] + 100 * math.sin(self.cat_angle - math.pi / 2)),
        ]

        # check for out of bounds
        if self.cat_location[0] > 0.9 * width or self.cat_location[0] < 0.1 * width:
            self.cat_location = [width / 2, height - 100]
            self.cat_speed = [0, 0]
            self.cat_angle = 0
            self.cat_angular_vel = 0
            self.score = 0

        ##object physics

        # move fish and not fish
        for f in reversed(self.fish):
            f[0] += f[2] * dt_scaled  # speed of the throw
            f[3] += 0.2 * dt_scaled  # gravity
            f[1] += f[3] * dt_scaled # y velocity
            # check out of bounds
            if f[1] > height:
                self.fish.remove(f)
        for f in reversed(self.not_fish):
            f[0] += f[2] * dt_scaled # speed of the throw
            f[3] += 0.2 * dt_scaled  # gravity
            f[1] += f[3] * dt_scaled  # y velocity
            # check out of bounds
            if f[1] > height:
                self.not_fish.remove(f)

        # check collision with the cat
        for f in reversed(self.fish):
            if distance([f[0], f[1]], self.cat_head_location) < 100:
                self.score += 1
                self.fish.remove(f)
        for f in reversed(self.not_fish):
            if distance([f[0], f[1]], self.cat_head_location) < 50:
                self.not_fish.remove(f)
                self.angle_to_not_fish = (
                    math.atan2(
                        self.cat_head_location[1] - f[1],
                        self.cat_head_location[0] - f[0],
                    )
                    - math.pi / 2
                )
                side = 1 if self.angle_to_not_fish < 0 else -1
                self.cat_angular_vel += side * random.uniform(0.08, 0.15)

        # refresh lists
        while len(self.fish) < 1:
            # choose a side of the screen
            if random.choice([0, 1]) == 0:
                self.fish.append(
                    [
                        0,
                        random.randint(0, height / 2),
                        random.randint(2, 5),
                        -random.randint(3, 10),
                    ]
                )
            else:
                self.fish.append(
                    [
                        width,
                        random.randint(0, height / 2),
                        -random.randint(2, 5),
                        -random.randint(3, 10),
                    ]
                )
        while len(self.not_fish) < 1:
            # choose a side of the screen
            if random.choice([0, 1]) == 0:
                self.not_fish.append(
                    [
                        0,
                        random.randint(0, height / 2),
                        random.randint(2, 5),
                        -random.randint(3, 10),
                    ]
                )
            else:
                self.not_fish.append(
                    [
                        width,
                        random.randint(0, height / 2),
                        -random.randint(2, 5),
                        -random.randint(3, 10),
                    ]
                )

    def event(self, event):
        width, height = self.width, self.height
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.right_pressed = True
                # cat_speed[0] = min(cat_speed[0] + 2, cat_speed_max)
                # cat_angle -= random.uniform(0.02*math.pi, 0.05*math.pi)
            elif event.key == K_LEFT:
                self.left_pressed = True
                # cat_speed[0] = min(cat_speed[0] - 2, cat_speed_max)
                # cat_angle += random.uniform(0.02*math.pi, 0.05*math.pi)
            elif event.key == K_a:
                self.cat_angular_vel -= random.uniform(0.01 * math.pi, 0.03 * math.pi)
            elif event.key == K_d:
                self.cat_angular_vel += random.uniform(0.01 * math.pi, 0.03 * math.pi)
            elif event.key == K_UP:
                if self.cat_location[1] == height - 100:
                    self.cat_speed[1] -= 25
        elif event.type == KEYUP:
            if event.key == K_UP:
                if self.cat_speed[1] < 0:
                    self.cat_speed[1] = 0
            elif event.key == K_RIGHT:
                self.right_pressed = False
            elif event.key == K_LEFT:
                self.left_pressed = False
