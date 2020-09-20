# Only the Explosion upwards - First working Explosion
#
# !/usr/bin/python3.4
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
    def __init__(self, x, y, time=100):
        self.x = x
        self.y = y
        self.time = time
        self.particles = []
        self.particles_left = True

    def draw(self, window):
        if self.time > 0:
            self.particles.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.time -= 1

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles.remove(particle)
            if not self.particles:
                self.particles_left = False


# Loop ------------------------------------------------------- #
while True:

    def draw_current_frame():
        for explosion in mainexplosions:
            if explosion.particles_left:
                explosion.draw(screen)
            else:
                mainexplosions.remove(explosion)

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