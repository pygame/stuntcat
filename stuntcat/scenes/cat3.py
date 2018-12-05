import pygame
import math
import random
from pygame.locals import *

from .scene import Scene
from .. resources import gfx, sfx, music


from pygame.sprite import DirtySprite, LayeredDirty

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class LayeredDirtyAppend(LayeredDirty):
    """ Like a group, except it has append and extend methods like a list.
    """
    def append(self, x):
        self.add(x)
    def extend(self, alist):
        for x in alist:
            self.add(x)


class Elephant(DirtySprite):
    def __init__(self, scene):
        DirtySprite.__init__(self)
        self.scene = scene
        self.width = scene.width
        self.height = scene.height
        self.state = 0
        self.states = {
            0: 'offscreen',
            1: 'poise left',
            2: 'stomp left',
            3: 'offscreen',
            4: 'poise right',
            5: 'stomp right',
        }
        self.last_state = 0
        self.just_happened = None


        self.time_between_stomps = 5000 #ms
        # self.time_between_stomps = 1000 #ms
        self.time_of_poise = 1500 #ms
        self.time_of_stomp = 500 #ms
        self.last_animation = 0 #ms

        # stamp.
        sfx('foot_elephant.ogg')

        self.image = gfx('foot.png', convert_alpha=True)
        # gfx('foot_part.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = -1000


    def update(self):
        # if self.just_happened is not None:
        #     print(self.just_happened)

        from_edge = 400
        from_top = 0

        if self.just_happened == 'offscreen':
            self.dirty = True
            self.rect.x = -1000
            self.rect.y = -1000
            sfx('foot_elephant.ogg', stop=1)
        elif self.just_happened == 'poise left':
            self.rect.x = from_edge
            self.rect.y = from_top
            self.dirty = True
        elif self.just_happened == 'stomp left':
            self.rect.y = (self.height - self.image.get_height()) - 10
            self.rect.x = from_edge
            self.dirty = True

            sfx('foot_elephant.ogg', play=1)
            if pygame.sprite.collide_rect(self, self.scene.cat):
                print('stop_right collide')
                self.scene.reset_on_death()
                self.dirty = True

        elif self.just_happened == 'poise right':
            self.rect.x = self.width - from_edge
            self.rect.y = from_top
            self.dirty = True
        elif self.just_happened == 'stomp right':
            self.rect.x = self.width - from_edge
            self.rect.y = (self.height - self.image.get_height()) - 10
            self.dirty = True
            sfx('foot_elephant.ogg', play=1)
            if pygame.sprite.collide_rect(self, self.scene.cat):
                print('stop_right collide')
                self.scene.reset_on_death()
                self.dirty = True


    def animate(self, total_time):
        state = self.states[self.state]
        start_state = self.state
        if state == 'offscreen':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None
            if total_time > self.last_animation + self.time_between_stomps:
                self.state += 1
                self.last_animation = total_time
        elif state == 'poise left' or state == 'poise right':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_poise:
                self.state += 1
                self.last_animation = total_time
        elif state == 'stomp left' or self.state == 'stomp right':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_stomp:
                self.state += 1

                if self.state == max(self.states.keys()) + 1:
                    self.state = 0
                    self.state = 0
                self.last_animation = total_time

        self.last_state = start_state


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
        pass
        # state = self.states[self.state]
        # if state == 'stomp left':
        #     if self.scene.cat_head_location[0] < width/2:
        #         self.scene.reset_on_death()
        #         self.dirty = True
        # if state == 'stomp right':
        #     if self.scene.cat_head_location[0] > width/2:
        #         self.scene.reset_on_death()
        #         self.dirty = True


class Lazer(DirtySprite):
    def __init__(self, container, width, height):
        DirtySprite.__init__(self, container)
        from_bottom = 210
        self.rect = pygame.Rect([200, height - from_bottom, width, 30])
        # self.rect.x = -1000
        self.image = pygame.Surface((self.rect[2], self.rect[3])).convert()
        self.image.fill((255, 0, 0))



class Shark(DirtySprite):
    def __init__(self, container, scene, width, height):
        DirtySprite.__init__(self, container)
        self.container = container
        self.scene = scene
        self.width, self.height = width, height

        self.state = 0 #
        self.states = {
            0: 'offscreen',
            1: 'about_to_appear',
            2: 'poise',
            3: 'fire laser',
            4: 'leaving',
        }
        self.last_state = 0
        self.just_happened = None
        self.lazered = False # was the cat hit?


        #TODO: to make it easier to test the shark
        # self.time_between_appearances = 1000 #ms
        self.time_between_appearances = 7000 #ms

        self.time_of_about_to_appear = 3000
        self.time_of_poise = 3000 #ms
        self.time_of_laser = 500 #ms
        self.time_of_leaving = 3000 #ms
        self.last_animation = 0 #ms

        sfx('default_shark.ogg')
        sfx('shark_appear.ogg')
        sfx('shark_gone.ogg')
        sfx('shark_lazer.ogg')
        sfx('zirkus.ogg')
        sfx('cat_laser_2.ogg')
        sfx('cat_laser_3.ogg')


        self.image = gfx('shark.png', convert_alpha=True)
        # gfx('foot_part.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = (self.height - self.image.get_height()) - 100


    def update(self):
        debug = True
        if self.just_happened == 'offscreen':
            if debug:print(self.just_happened)
            sfx('shark_gone.ogg', stop=1)
            sfx('zirkus.ogg', play=1)

            self.rect.x = -1000
            self.dirty = True

        elif self.just_happened == 'about_to_appear':
            if debug:print(self.just_happened)
            music(stop=True)
            sfx('shark_appear.ogg', play=1)
            sfx('zirkus.ogg', stop=1)

        elif self.just_happened == 'poise':
            if debug:print(self.just_happened)
            sfx('shark_appear.ogg', stop=1)
            sfx('shark_attacks.ogg', play=1)

            self.rect.x = 50
            self.dirty = True

        elif self.just_happened == 'fire laser':
            if debug:print(self.just_happened)
            self.lazer = Lazer(self.container, self.width, self.height)

            if self.scene.cat_location[1] > self.height - 130:
                # sfx('shark_lazer.ogg', play=1)
                print('shark collide')

                sfx('cat_laser_2.ogg', play=1)
                # sfx('cat_laser_3.ogg', play=1)

                self.lazered = True
            else:
                self.lazered = False
                sfx('shark_lazer.ogg', play=1)

        elif self.just_happened == 'leaving':
            if debug:print(self.just_happened)
            sfx('shark_attacks.ogg', stop=1)
            sfx('shark_gone.ogg', play=1)
            self.rect.x = 0
            self.dirty = True
            if self.lazered:
                self.scene.reset_on_death()
                self.lazered = False
            self.lazer.kill()


    def animate(self, total_time):
        # print('update', self.states[self.state], self.states[self.last_state])
        state = self.states[self.state]
        start_state = self.state

        if state == 'offscreen':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_between_appearances:
                self.state += 1
                self.last_animation = total_time

        elif state == 'about_to_appear':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_about_to_appear:
                self.state += 1
                self.last_animation = total_time

        elif state == 'poise':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_poise:
                self.state += 1
                self.last_animation = total_time

        elif state == 'fire laser':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_laser:
                self.state += 1
                self.last_animation = total_time

        elif state == 'leaving':
            just_happened = self.state != self.last_state
            if just_happened:
                self.just_happened = state
            else:
                self.just_happened = None

            if total_time > self.last_animation + self.time_of_leaving:
                self.state += 1
                if self.state == max(self.states.keys()) + 1:
                    self.state = 0
                self.last_animation = total_time

        self.last_state = start_state

    def render(self, screen, width, height):
        state = self.states[self.state]

        if state == 'poise':
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
        if state == 'fire laser':
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
        pass
        #TODO: this doesn't work. It means the laser never fires.
        # if self.state == 2:
        #     if cat_location[1] > height - 130:
        #         print('shark collide')
        #         scene.reset_on_death()


class Cat(DirtySprite):
    def __init__(self, cat_holder):
        DirtySprite.__init__(self)
        self.cat_holder = cat_holder
        self.image = gfx('cat_unicycle.png', convert_alpha=True)
        self.rect = self.image.get_rect()
        sfx('cat_jump.ogg')
        sfx('cat_wheel.ogg')

        # sfx('cat_jump.ogg', play=1)
        # sfx('cat_wheel.ogg', play=1)

        self.image_direction = [
            pygame.transform.flip(self.image, 1, 0),
            self.image,
        ]

        self.last_location = [0, 0]
        self.last_direction = True #right is true
        self.last_rotation = -1

    def update(self):
        direction = self.cat_holder.cat_speed[0] > 0
        # location = self.cat_holder.cat_location
        location = self.cat_holder.cat_head_location
        rotation = self.cat_holder.cat_angle
        #if self.last_location != location:
        #    self.dirty = True
        #    self.rect.x = int(location[0])
        #    self.rect.y = int(location[1])
        if self.last_direction != direction:
            self.dirty = True
            self.image = self.image_direction[int(direction)]
            if random.random() < 0.1:
                sfx('cat_wheel.ogg', play=1)

        if self.last_rotation != rotation or self.last_location != location:
            self.image = pygame.transform.rotate(self.image_direction[int(direction)], -self.cat_holder.cat_angle*180/math.pi)
            size = self.image.get_rect().size
            self.dirty = True
            self.rect.x = int(location[0]) - size[0]*0.5
            self.rect.y = int(location[1]) - size[1]*0.5

        self.last_location == location[:]
        self.last_direction = direction
        self.last_rotation = rotation



        # draw cat
        # pygame.draw.line(
        #     screen, [0, 0, 255], self.cat_location, self.cat_head_location, 20
        # )
        # pygame.draw.circle(screen, [0, 0, 255], self.cat_head_location, 50, 1)
        # pygame.draw.circle(screen, [0, 255, 0], self.cat_head_location, 100, 1)


class Fish(DirtySprite):
    colors = ["red", "yellow", "green"]

    def __init__(self, group, x, y, vx, vy):
        DirtySprite.__init__(self, group)
        self.image = gfx("fish_" + random.choice(Fish.colors) + ".png", convert_alpha=True)
        self.rect = self.image.get_rect()
        size = self.rect.size
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(vx, vy)

        self.last_pos = [x, y]
        self.pos = [x,y]

    def update(self):
        if self.last_pos != self.pos[:2]:
            self.dirty = True
            self.rect.x = self.pos[0] - 25
            self.rect.y = self.pos[1] - 25
        self.last_pos = self.pos[:2]

class NotFish(DirtySprite):
    def __init__(self, group, x, y, vx, vy):
        DirtySprite.__init__(self, group)
        self.image = gfx('ring.png', convert_alpha=True)
        self.rect = self.image.get_rect()
        size = self.rect.size
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(vx, vy)

        self.last_pos = [x, y]
        self.pos = [x,y]

    def update(self):
        if self.last_pos != self.pos[:2]:
            self.dirty = True
            self.rect.x = self.pos[0] - 25
            self.rect.y = self.pos[1] - 25
        self.last_pos = self.pos[:2]


class Score(DirtySprite):
    def __init__(self, score_holder):
        """
        score_holder has a 'score' attrib.
        """
        DirtySprite.__init__(self)
        self.score_holder = score_holder
        self.myfont = pygame.font.SysFont("monospace", 20)
        self.image = self.myfont.render(
            "score : " + str(self.score_holder.score), True, [255, 255, 255]
        )
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.last_score = self.score_holder.score

    def update(self):
        if self.last_score != self.score_holder.score:
            self.dirty = True
            self.image = self.myfont.render(
                "score : " + str(self.score_holder.score), True, [255, 255, 255]
            )
        self.last_score = self.score_holder.score



class DeadZone(DirtySprite):
    def __init__(self, points):
        """
        score_holder has a 'score' attrib.
        """
        DirtySprite.__init__(self)
        color = [255, 0, 0]

        # draw dead zones
        surf = pygame.display.get_surface()
        rect = pygame.draw.polygon(
            surf,
            color,
            points
        )
        self.image = surf.subsurface(rect.clip(surf.get_rect())).copy()
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y



class CatUniScene(Scene):
    def __init__(self, *args, **kwargs):
        Scene.__init__(self, *args, **kwargs)
        (width, height) = (1920//2, 1080//2)
        self.width, self.height = width, height

        # Loading screen should always be a fallback active scene
        self.active = False
        self.first_render = True

        self.myfont = pygame.font.SysFont("monospace", 20)

        self.background = gfx('background.png').convert()
        # self.cat_unicycle = gfx('cat_unicycle.png').convert_alpha()
        # self.fish = gfx('fish.png').convert_alpha()
        # self.foot = gfx('foot.png').convert_alpha()
        # self.foot_part = gfx('foot_part.png').convert_alpha()
        # self.shark = gfx('shark.png').convert_alpha()

        sfx('cat_jump.ogg')
        sfx('eatfish.ogg')

        #cat variables
        self.cat_location = [width / 2, height - 100]
        self.cat_speed = [0, 0]
        self.cat_speed_max = 8
        self.cat_fall_speed_max = 16
        self.cat_angle = 0
        self.cat_angular_vel = 0
        self.cat_head_location = [
            int(self.cat_location[0] + 100 * math.cos(self.cat_angle - math.pi / 2)),
            int(self.cat_location[1] + 100 * math.sin(self.cat_angle - math.pi / 2)),
        ]

        self.left_pressed = False
        self.right_pressed = False
        self.score = 0


        #timing
        self.dt_scaled = 0
        self.total_time = 0


        #elephant and shark classes
        self.elephant = Elephant(self)
        self.shark_active = False #is the shark enabled yet
        self.elephant_active = False
        self.cat = Cat(self)
        self.score_text = Score(self)

        self.deadzones = []

        # self.deadzones = [
        #     DeadZone(
        #         [
        #             [0, height - 100],
        #             [0.1 * width, height - 100],
        #             [0.1 * width, height],
        #             [0, height],
        #         ],
        #     ),
        #     DeadZone(
        #         [
        #             [0.9 * width, height - 100],
        #             [width, height - 100],
        #             [width, height],
        #             [0.9 * width, height],
        #         ],
        #     ),
        # ]

        self.init_sprites()

        # lists of things to catch by [posx, posy, velx, vely]
        # self.fish = [[0, height / 2, 10, -5]]
        self.fish = LayeredDirtyAppend()
        self.fish.extend([Fish(self.allsprites, 0, height / 2, 10, -5)])

        self.not_fish = LayeredDirtyAppend()

        #difficulty varibles
        self.number_of_not_fish = 0



    def init_sprites(self):
        """temp, this will go in the init.
        """
        sprite_list = [
            self.elephant,
            self.cat,
            self.score_text
        ]
        sprite_list += self.deadzones
        self.allsprites = LayeredDirty(
            sprite_list,
            _time_threshold=1000/10.0
        )
        scene = self
        self.shark = Shark(self.allsprites, scene, self.width, self.height)
        self.allsprites.add(self.shark)
        self.allsprites.clear(self.screen, self.background)


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
        self.elephant.just_happened = None
        self.elephant.dirty = 1
        self.elephant_active = False

        self.shark.last_animation = 0
        self.shark.state = 0
        self.shark_active = False
        self.shark.just_happened = None
        self.shark.dirty = 1

        if hasattr(self.shark, 'lazer'):
            self.shark.lazer.kill()


    #periodically increase the difficulty
    def increase_difficulty(self):
        self.number_of_not_fish = 0
        if self.score > 6:
            self.number_of_not_fish = 1
        if self.score > 13:
            self.number_of_not_fish = 0
        if self.score > 19:
            self.number_of_not_fish = 1
        if self.score > 23:
            self.number_of_not_fish = 0
        if self.score > 30:
            self.number_of_not_fish = 1
        if self.score > 40:
            self.number_of_not_fish = 2
        if self.score >= 50:
            self.number_of_not_fish = int((self.score - 20)/10)

        #TODO: to make it easier to test.
        # if self.score >= 15:
        #     self.shark_active = True
        if self.score >= 3:
            self.shark_active = True

        #TODO: to make it easier to test.
        if self.score >= 8:
            self.elephant_active = True

    def render_sprites(self):
        rects = []
        self.allsprites.update()
        rects.extend(self.allsprites.draw(self.screen))
        return rects

    def render(self):
        rects = []
        if self.first_render:
            self.first_render = False
            rects.append(self.screen.get_rect())
        rects.extend(self.render_sprites())
        return rects

        # we draw the sprites, and then the lines over the top.
        self.render_sprites()

        screen = self.screen
        width, height = self.width, self.height

        if 0:
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
            pygame.draw.circle(screen, [0, 255, 0], [int(f.pos[0]), int(f.pos[1])], 10)
        for f in self.not_fish:
            pygame.draw.circle(screen, [255, 0, 0], [int(f.pos[0]), int(f.pos[1])], 10)

        # draw score
        textsurface = self.myfont.render(
            "score : " + str(self.score), True, [255, 255, 255]
        )
        screen.blit(textsurface, (100, 100))
        return [screen.get_rect()]

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
        for f in reversed(self.fish.sprites()):
            f.pos[0] += f.velocity[0] * dt_scaled  # speed of the throw
            f.velocity[1] += 0.2 * dt_scaled  # gravity
            f.pos[1] += f.velocity[1] * dt_scaled # y velocity
            # check out of bounds
            if f.pos[1] > height:
                self.fish.remove(f)
                f.kill()
        for f in reversed(self.not_fish.sprites()):
            f.pos[0] += f.velocity[0] * dt_scaled # speed of the throw
            f.velocity[1] += 0.2 * dt_scaled  # gravity
            f.pos[1] += f.velocity[1] * dt_scaled  # y velocity
            # check out of bounds
            if f.pos[1] > height:
                self.not_fish.remove(f)
                f.kill()

        # check collision with the cat
        for f in reversed(self.fish.sprites()):
            if distance([f.rect[0], f.rect[1]], self.cat_head_location) < 100:
                self.score += 1
                self.fish.remove(f)
                sfx('eatfish.ogg', play=1)
                f.kill()
        for f in reversed(self.not_fish.sprites()):
            if distance([f.rect[0], f.rect[1]], self.cat_head_location) < 50:
                self.not_fish.remove(f)
                f.kill()
                self.angle_to_not_fish = (
                    math.atan2(
                        self.cat_head_location[1] - f.rect[1],
                        self.cat_head_location[0] - f.rect[0],
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
                    Fish(self.allsprites,
                        0,
                        height/2,#random.randint(0, height / 2),
                        random.randint(3, 7),
                        -random.randint(5, 12),
                    )
                )
            else:
                self.fish.append(
                    Fish(self.allsprites,
                        width,
                        height/2,#random.randint(0, height / 2),
                        -random.randint(3, 7),
                        -random.randint(5, 12),
                    )
                )
        while len(self.not_fish) < self.number_of_not_fish:
            # choose a side of the screen
            if random.choice([0, 1]) == 0:
                self.not_fish.append(
                    NotFish(self.allsprites,
                        0,
                        height/2,#random.randint(0, height / 2),
                        random.randint(3, 7),
                        -random.randint(5, 12),
                    )
                )
            else:
                self.not_fish.append(
                    NotFish(self.allsprites,
                        width,
                        height/2,#random.randint(0, height / 2),
                        -random.randint(3, 7),
                        -random.randint(5, 12),
                    )
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
                    sfx('cat_jump.ogg', play=1)

        elif event.type == KEYUP:
            if event.key == K_UP:
                if self.cat_speed[1] < 0:
                    self.cat_speed[1] = 0
            elif event.key == K_RIGHT:
                self.right_pressed = False
            elif event.key == K_LEFT:
                self.left_pressed = False
