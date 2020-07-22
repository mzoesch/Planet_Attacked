import pygame

pygame.init()

# Create the screen

width = 1000
hight = 600

menuscreen = pygame.display.set_mode((width, hight))
gamescreen = pygame.display.set_mode((width, hight))

# Backgrounds

game_background = pygame.image.load("resources/backgrounds/Space_Invaders_2020(scaledright_red).jpg")
gameover_background = pygame.image.load("resources/backgrounds/Space_Invaders_2020(scaledright).jpg")
