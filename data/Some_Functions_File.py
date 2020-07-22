import pygame


def setting_up_the_screen():

    # Acces files from other dirctories

    player_ship = pygame.image.load("resources/graphics/space_ship_icon(512).png")

    # Window name

    pygame.display.set_caption("Space Invaders @Magnus Zoeschinger")

    # What you see when switching between apps

    app_icon = player_ship
    pygame.display.set_icon(app_icon)
