import pygame
import math
import random
from pygame.locals import *

#setup

background_colour = (0,0,0)
(width, height) = (1000, 600)

screen = pygame.display.set_mode((width, height))#,pygame.FULLSCREEN)
screen.fill(background_colour)
pygame.display.set_caption('Cat Game')
pygame.font.init()

myfont = pygame.font.SysFont("monospace", 20)

clock = pygame.time.Clock()

def distance(a,b):
	return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

cat_location = [width/2, height - 100]
cat_speed = [0,0]
cat_speed_max = 8
cat_fall_speed_max = 16
cat_angle = 0
cat_angular_vel = 0
time_elapsed = 0
left_pressed = False
right_pressed = False
score = 0

#lists of things to catch by [posx, posy, velx, vely]
fish = [[0,height/2, 10, -5]]
not_fish = [[width,height/2, -5, -2]]


running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			elif event.key == K_RIGHT:
				right_pressed = True
				#cat_speed[0] = min(cat_speed[0] + 2, cat_speed_max)
				#cat_angle -= random.uniform(0.02*math.pi, 0.05*math.pi)
			elif event.key == K_LEFT:
				left_pressed = True
				#cat_speed[0] = min(cat_speed[0] - 2, cat_speed_max)
				#cat_angle += random.uniform(0.02*math.pi, 0.05*math.pi)
			elif event.key == K_a:
				cat_angular_vel -= random.uniform(0.01*math.pi, 0.03*math.pi)
			elif event.key == K_d:
				cat_angular_vel += random.uniform(0.01*math.pi, 0.03*math.pi)
			elif event.key == K_UP:
				if cat_location[1] == height - 100:
					cat_speed[1] -= 25
		elif event.type == KEYUP:
			if event.key == K_UP:
				if cat_speed[1] < 0:
					cat_speed[1] = 0
			elif event.key == K_RIGHT:
				right_pressed = False
			elif event.key == K_LEFT:
				left_pressed = False
	       

	screen.fill(background_colour)

	##cat physics
	cat_angular_vel *= 0.9

	#add gravity
	cat_speed[1] = min(cat_speed[1] + 1, cat_fall_speed_max)

	#accelerate the cat left or right
	if right_pressed:
		cat_speed[0] = min(cat_speed[0] + 0.3*time_elapsed/17, cat_speed_max)
		cat_angle -= 0.01*time_elapsed/17

	if left_pressed:
		cat_speed[0] = max(cat_speed[0] - 0.3*time_elapsed/17, -cat_speed_max)
		cat_angle += 0.01*time_elapsed/17

	#make the cat fall
	cat_angular_vel += 0.001*cat_angle*time_elapsed/17
	cat_angle += cat_angular_vel*time_elapsed/17
	if cat_angle > math.pi/2 or cat_angle < -math.pi/2:
		cat_location = [width/2, height - 100]
		cat_speed = [0,0]
		cat_angle = 0
		cat_angular_vel = 0
		score = 0

	#move cat
	cat_location[0] += cat_speed[0]*time_elapsed/17
	cat_location[1] += cat_speed[1]*time_elapsed/17
	if cat_location[1] > height - 100:
		cat_location[1] = height - 100
		cat_speed[1] = 0
	cat_head_location = [int(cat_location[0] + 100*math.cos(cat_angle - math.pi/2)), int(cat_location[1] + 100*math.sin(cat_angle - math.pi/2))]

	#check for out of bounds
	if cat_location[0] > 0.9*width or cat_location[0] < 0.1*width:
		cat_location = [width/2, height - 100]
		cat_speed = [0,0]
		cat_angle = 0
		cat_angular_vel = 0
		score = 0

	##object physics

	#move fish and not fish
	for f in reversed(fish):
		f[0] += f[2]*time_elapsed/17 #speed of the throw
		f[3] += 0.2*time_elapsed/17 #gravity
		f[1] += f[3]*time_elapsed/17 #y velocity
		#check out of bounds
		if f[1] > height:
			fish.remove(f)
	for f in reversed(not_fish):
		f[0] += f[2]*time_elapsed/17 #speed of the throw
		f[3] += 0.2*time_elapsed/17 #gravity
		f[1] += f[3]*time_elapsed/17 #y velocity
		#check out of bounds
		if f[1] > height:
			not_fish.remove(f)

	#check collision with the cat
	for f in reversed(fish):
		if distance([f[0], f[1]], cat_head_location) < 100:
			score += 1
			fish.remove(f)
	for f in reversed(not_fish):
		if distance([f[0], f[1]], cat_head_location) < 50:
			not_fish.remove(f)
			angle_to_not_fish = math.atan2(cat_head_location[1] - f[1], cat_head_location[0] - f[0]) - math.pi/2
			side = 1 if angle_to_not_fish < 0 else -1
			cat_angular_vel += side*random.uniform(0.08,0.15)

	#refresh lists
	while len(fish) < 1:
		#choose a side of the screen
		if random.choice([0,1]) == 0:
			fish.append([0,random.randint(0, height/2), random.randint(2,5), -random.randint(3,10)])
		else:
			fish.append([width,random.randint(0, height/2), -random.randint(2,5), -random.randint(3,10)])
	while len(not_fish) < 1:
		#choose a side of the screen
		if random.choice([0,1]) == 0:
			not_fish.append([0,random.randint(0, height/2), random.randint(2,5), -random.randint(3,10)])
		else:
			not_fish.append([width,random.randint(0, height/2), -random.randint(2,5), -random.randint(3,10)])

	#draw cat
	pygame.draw.line(screen, [0,0,255], cat_location, cat_head_location, 20)
	pygame.draw.circle(screen, [0,0,255], cat_head_location, 50, 1)
	pygame.draw.circle(screen, [0,255,0], cat_head_location, 100, 1)

	#draw dead zones
	pygame.draw.polygon(screen, [255,0,0], [[0, height - 100], [0.1*width, height - 100], [0.1*width, height], [0,height]])
	pygame.draw.polygon(screen, [255,0,0], [[0.9*width, height - 100], [width, height - 100], [width, height], [0.9*width,height]])

	#draw fish and not fish
	for f in fish:
		pygame.draw.circle(screen, [0,255,0], [int(f[0]), int(f[1])], 10)
	for f in not_fish:
		pygame.draw.circle(screen, [255,0,0], [int(f[0]), int(f[1])], 10)

	#draw score
	textsurface = myfont.render("score : "+ str(score), True, [255,255,255])
	screen.blit(textsurface,(100, 100))

	pygame.display.flip()
	
	time_elapsed = clock.tick(60)
	

pygame.quit()