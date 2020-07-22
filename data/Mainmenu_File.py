# Main Menu file
# This file loads the main menu

import pygame
from data.Window_Size_File import menuscreen
from data.Space_Invaders_Game_File import game
from data.Window_Size_File import width

# Acces files from other dirctories

menu_playerImg = pygame.image.load("resources/graphics/space_invaders_ship(64).png")
mainmenu_background = pygame.image.load("resources/backgrounds/Space_Invaders_2020(scaledright_red)-Background.jpg")


# The location where the highscore can be seen by the player

highscore_textY = 10


def mainmenu():

    running_mainmenu = True

    # The function which is reponsible for showing things in main menu that need to be explained

    def menu_player(x, y):
        menuscreen.blit(menu_playerImg, (x, y))

    # The function whis is reponsible for printing out the players score on the top right corner

    def show_highscore(y):

        highscore_font = pygame.font.Font("freesansbold.ttf", 32)

        # Get the highscore from the file

        with open("data/hs.txt", "r") as hsf:
            highscore_value = hsf.read()

        rendered_highscore = highscore_font.render(f"Highscore: {highscore_value}", True, (255, 0, 255))

        text_width, _ = pygame.Surface.get_size(rendered_highscore)

        x = width - text_width - 10

        menuscreen.blit(rendered_highscore, (x, y))

    # Main menu loop

    while running_mainmenu:

        menuscreen.blit(mainmenu_background, (0, 0))

        for event in pygame.event.get():

            # Mainmenu Close

            if event.type == pygame.QUIT:
                running_mainmenu = False

            # Starting the game

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game()

                # Quitting the game by pressing "Q"

                if event.key == pygame.K_q:
                    running_mainmenu = False
                    break

        # This line shows the menu_player

        menu_player(468, 500)

        # This line shows the highscore

        show_highscore(highscore_textY)

        pygame.display.update()
