import os
import pygame

# Access files from others directories

# Loading images

# What you see when switching between apps
IMG_APPICON = pygame.image.load(os.path.join("resources/graphics", "app_icon(512).png"))

# Players ship
IMG_PLAYER_SHIP = pygame.image.load(os.path.join("resources/graphics", "Player_Ship.png"))

# Players Laser
IMG_PLAYER_LASER = pygame.image.load(os.path.join("resources/graphics", "Player_Laser.png"))

# Enemies ships
IMG_ENEMY_SHIP_RED = pygame.image.load(os.path.join("resources/graphics", "Enemy_Ship_Red.png"))
IMG_ENEMY_SHIP_GREEN = pygame.image.load(os.path.join("resources/graphics", "Enemy_Ship_Green.png"))
IMG_ENEMY_SHIP_BLUE = pygame.image.load(os.path.join("resources/graphics", "Enemy_Ship_Blue.png"))

# Enemy lasers
IMG_ENEMY_LASER_RED = pygame.image.load(os.path.join("resources/graphics", "Enemy_Laser_Red.png"))
IMG_ENEMY_LASER_GREEN = pygame.image.load(os.path.join("resources/graphics", "Enemy_Laser_Green.png"))
IMG_ENEMY_LASER_BLUE = pygame.image.load(os.path.join("resources/graphics", "Enemy_Laser_Blue.png"))

# Loading wav

# Music

SONG_ONE = "resources/music/Background_(1).wav"
SONG_TWO = "resources/music/Background_(2).wav"

# Sounds

SHIP_EXPLOSION = "resources/sounds/Explosion.wav"
SHOOTING_LASER = "resources/sounds/Laser_Shooting.wav"
