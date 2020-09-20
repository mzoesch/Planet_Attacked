# First working Explosion -- 03.09.2020
#
#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame
import sys
import random
from pygame.locals import *

mainexplosions = []

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)


# Explosion class
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.to_generate = 10
        self.particles_up = []
        self.particles_right = []
        self.particles_down = []
        self.particles_left = []
        self.particles_left_up = True
        self.particles_left_right = True
        self.particles_left_down = True
        self.particles_left_left = True
        self.particles_in_game = True

    def draw(self, window):
        if self.to_generate > 0:
            self.particles_up.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_right.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_down.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_left.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.to_generate -= 1

        for particle in self.particles_up:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_up.remove(particle)
            if not self.particles_up:
                self.particles_left_up = False

        for particle in self.particles_right:
            particle[0][0] -= particle[1][1]
            particle[0][1] += particle[1][0]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_right.remove(particle)
            if not self.particles_right:
                self.particles_left_right = False

        for particle in self.particles_down:
            particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_down.remove(particle)
            if not self.particles_down:
                self.particles_left_down = False

        for particle in self.particles_left:
            particle[0][0] += particle[1][1]
            particle[0][1] += particle[1][0]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_left.remove(particle)
            if not self.particles_left:
                self.particles_left_left = False

        if not self.particles_left_up and self.particles_left_right and self.particles_left_down and self.particles_left_left:
            self.particles_in_game = False


# Loop ------------------------------------------------------- #
while True:

    def draw_current_frame():
        for explosion in mainexplosions:
            if explosion.particles_in_game:
                explosion.draw(screen)
            else:
                mainexplosions.remove(explosion)
                print("DELETED")

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:
                for explosion in range(1):
                    explosion = Explosion(random.randint(100, 200), random.randint(100, 200))
                    explosion.x = 250
                    mainexplosions.append(explosion)

    # Update ------------------------------------------------- #
    draw_current_frame()
    pygame.display.update()
    mainClock.tick(60)