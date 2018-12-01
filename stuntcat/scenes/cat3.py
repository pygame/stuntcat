import pygame
import math
import random
from pygame.locals import *

from .scene import Scene
from .. resources import gfx

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

class elephant:
    def __init__(self):
        self.state = 0 #0 = offscreen, 1 = poise left, 2 = stomp left, 3 = offscreen, 4 = poise right, 5 = stomp right
        self.time_between_stomps = 5000 #ms
        self.time_of_poise = 1500 #ms
        self.time_of_stomp = 500 #ms
        self.last_animation = 0 #ms

    def animate(self, total_time):
        if self.state == 0 or self.state == 3:
            if total_time > self.last_animation + self.time_between_stomps:
                self.state += 1
                self.last_animation = total_time
        if self.state == 1 or self.state == 4:
            if total_time > self.last_animation + self.time_of_poise:
                self.state += 1
                self.last_animation = total_time
        if self.state == 2 or self.state == 5:
            if total_time > self.last_animation + self.time_of_stomp:
                self.state += 1
                if self.state == 6:
                    self.state = 0
                self.last_animation = total_time



    def render(self, screen, width, height):
        if self.state == 1: #poise left
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
        if self.state == 2: #stomp left
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
        if self.state == 4: #poise right
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
        if self.state == 5: #stomp right
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


    def collide(self, scene, width, height, cat_head_location):
        if self.state == 2:
            if cat_head_location[0] < width/2:
                scene.reset_on_death()
        if self.state == 5:
            if cat_head_location[0] > width/2:
                scene.reset_on_death()

class shark:
    def __init__(self):
        self.state = 0 #0 = offscreen, 1 = poise, 2 = fire laser
        self.time_between_appearances = 7000 #ms
        self.time_of_poise = 1500 #ms
        self.time_of_laser = 100 #ms
        self.last_animation = 0 #ms

    def animate(self, total_time):
        if self.state == 0:
            if total_time > self.last_animation + self.time_between_appearances:
                self.state += 1
                self.last_animation = total_time
        if self.state == 1:
            if total_time > self.last_animation + self.time_of_poise:
                self.state += 1
                self.last_animation = total_time
        if self.state == 2:
            if total_time > self.last_animation + self.time_of_laser:
                self.state += 1
                if self.state == 3:
                    self.state = 0
                self.last_animation = total_time



    def render(self, screen, width, height):
        if self.state == 1: #poise
            pygame.draw.polygon(
                screen,
                [255, 255, 0],
                [
                    [0, height - 130],
                    [0.2 * width, height - 130],
                    [0.2 * width, height],
                    [0, height],
                ],
            )
        if self.state == 2: #fire laser
            pygame.draw.polygon(
                screen,
                [255, 255, 0],
                [
                    [0, height - 130],
                    [0.2 * width, height - 130],
                    [0.2 * width, height],
                    [0, height],
                ],
            )
            pygame.draw.polygon(
                screen,
                [255, 0, 0],
                [
                    [0.2 * width, height - 130],
                    [width, height - 130],
                    [width, height - 100],
                    [0.2 * width, height - 100],
                ],
            )


    def collide(self, scene, width, height, cat_location):

        if self.state == 2:
            if cat_location[1] > height - 130:
                scene.reset_on_death()

class CatUniScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)
        (width, height) = (1920//2, 1080//2)
        self.width, self.height = width, height

        # Loading screen should always be a fallback active scene
        self.active = True

        self.myfont = pygame.font.SysFont("monospace", 20)

        self.background = gfx('background.png').convert()
        self.cat_unicycle = gfx('cat_unicycle.png').convert_alpha()
        self.fish = gfx('fish.png').convert_alpha()
        self.foot = gfx('foot.png').convert_alpha()
        self.foot_part = gfx('foot_part.png').convert_alpha()
        self.shark = gfx('shark.png').convert_alpha()


        #cat variables
        self.cat_location = [width / 2, height - 100]
        self.cat_speed = [0, 0]
        self.cat_speed_max = 8
        self.cat_fall_speed_max = 16
        self.cat_angle = 0
        self.cat_angular_vel = 0
        self.left_pressed = False
        self.right_pressed = False
        self.score = 0

        #timing
        self.dt_scaled = 0
        self.total_time = 0

        # lists of things to catch by [posx, posy, velx, vely]
        self.fish = [[0, height / 2, 10, -5]]
        self.not_fish = []

        #difficulty varibles
        self.number_of_not_fish = 0

        #elephant and shark classes
        self.elephant = elephant()
        self.shark = shark()
        self.shark_active = False #is the shark enabled yet
        self.elephant_active = False

    #what to do when you die, reset the level
    def reset_on_death(self):
        self.cat_location = [self.width / 2, self.height - 100]
        self.cat_speed = [0, 0]
        self.cat_angle = 0
        self.cat_angular_vel = 0
        self.score = 0
        self.total_time = 0
        self.elephant.last_animation = 0
        self.elephant.state = 0
        self.shark.last_animation = 0
        self.shark.state = 0
        self.shark_active = False
        self.elephant_active = False

    #periodically increase the difficulty
    def increase_difficulty(self):
        self.number_of_not_fish = int(self.score/10)
        if self.score >= 15:
            self.shark_active = True
        if self.score >= 25:
            self.elephant_active = True
           


    def render(self):
        screen = self.screen
        width, height = self.width, self.height

        background_colour = (0, 0, 0)
        screen.fill(background_colour)
        screen.blit(self.background, (0, 0))

        self.elephant.render(screen, width, height)
        self.shark.render(screen, width, height)

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
        self.increase_difficulty()

        self.total_time += dt #keep track of the total number of ms passed during the game
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
            self.cat_angle -= 0.003 * dt_scaled

        if self.left_pressed:
            self.cat_speed[0] = max(
                self.cat_speed[0] - 0.3 * dt_scaled, -self.cat_speed_max
            )
            self.cat_angle += 0.003 * dt_scaled

        # make the cat fall
        angle_sign = 1 if self.cat_angle > 0 else -1
        self.cat_angular_vel += 0.0002 * angle_sign * dt_scaled
        self.cat_angle += self.cat_angular_vel * dt_scaled
        if (self.cat_angle > math.pi / 2 or self.cat_angle < -math.pi / 2) and self.cat_location[1] > height - 160:
            self.reset_on_death()

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
        if (self.cat_location[0] > 0.9 * width or self.cat_location[0] < 0.1 * width) and self.cat_location[1] > height - 110:
            self.reset_on_death()

        #check for collision with the elephant stomp
        if self.elephant_active:
            self.elephant.animate(self.total_time)
            self.elephant.collide(self, width, height, self.cat_head_location)
        if self.shark_active:
            self.shark.animate(self.total_time)
            self.shark.collide(self, width, height, self.cat_location)

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
                        height/2,#random.randint(0, height / 2),
                        random.randint(3, 7),
                        -random.randint(5, 12),
                    ]
                )
            else:
                self.fish.append(
                    [
                        width,
                        height/2,#random.randint(0, height / 2),
                        -random.randint(3, 7),
                        -random.randint(5, 12),
                    ]
                )
        while len(self.not_fish) < self.number_of_not_fish:
            # choose a side of the screen
            if random.choice([0, 1]) == 0:
                self.not_fish.append(
                    [
                        0,
                        height/2,#random.randint(0, height / 2),
                        random.randint(3, 7),
                        -random.randint(5, 12),
                    ]
                )
            else:
                self.not_fish.append(
                    [
                        width,
                        height/2,#random.randint(0, height / 2),
                        -random.randint(3, 7),
                        -random.randint(5, 12),
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
