# Main Menu file
# This file makes the main menu

import pygame
from data.WindowSize_File import *
from data.Game_File import game
from data.Tutorial_File import tutorial
import os

# Creates the menu screen
menuscreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


# Mainmenu function
def mainmenu():

    global menuscreen

    # Getting the screen values of the monitor that the user is playing on
    with open("assets/monsiz.txt", "r") as msf:
        window_size = msf.readlines()
        monitor_sizeX = int(window_size[0])
        monitor_sizeY = int(window_size[1])

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()

    # Checking fullscreen
    if current_width == monitor_sizeX and current_height == monitor_sizeY:
        fullscreen = True
        menuscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        fullscreen = False

    # Setting everything to default value
    exit_fullscreen_past_width = None
    exit_fullscreen_past_height = None
    running_mainmenu = True

    # Y-Value of the Highscore
    HIGHSCORE_TEXTY = 10

    # The function which is responsible for printing out the players high score in the top right corner
    def show_highscore(y):

        # Get the highscore from the file
        with open("assets/hs.txt", "r") as hsf:
            highscore_value = hsf.read()

        # Renders it
        HIGHSCORE_FONT = pygame.font.Font("freesansbold.ttf", 32)
        rendered_highscore = HIGHSCORE_FONT.render(f"Highscore: {highscore_value}", True, (255, 0, 255))

        # Correct placement
        text_width, _ = pygame.Surface.get_size(rendered_highscore)
        x = current_width - text_width - 10

        # Shows it
        menuscreen.blit(rendered_highscore, (x, y))

    # Main menu loop
    while running_mainmenu:

        # Setting up the right screen size and fullscreen mode

        # Checking the size of the window
        current_width, _ = pygame.display.get_surface().get_size()
        _, current_height = pygame.display.get_surface().get_size()

        # Making the background the correct size
        mainmenu_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Menu.png")), (current_width, current_height))

        # Shows the background
        menuscreen.blit(mainmenu_background, (0, 0))

        # This line shows the highscore
        show_highscore(HIGHSCORE_TEXTY)

        # Checking events
        for event in pygame.event.get():

            # Mainmenu Close
            if event.type == pygame.QUIT:
                running_mainmenu = False
                pygame.quit()
                quit()
                break

            # Makes the screen the size how the user wants it
            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    if event.w < 1000 or event.h < 600:
                        menuscreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    else:
                        menuscreen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Detects if a key is pressed
            if event.type == pygame.KEYDOWN:

                # Starting the game
                if event.key == pygame.K_p:

                    # Game loop
                    game()

                    # Reads last (high)score
                    with open("assets/sv.txt", "r") as svf:
                        score_value = svf.read()
                    with open("assets/hs.txt", "r") as hsf_read_after_play:
                        old_highscore_value = hsf_read_after_play.read()

                    # Checks if there is a new highscore
                    if int(score_value) > int(old_highscore_value):
                        with open("assets/hs.txt", "w") as hsf_write_after_play:
                            hsf_write_after_play.write(score_value)

                    # Making screen resizeable
                    if current_width == monitor_sizeX and current_height == monitor_sizeY:
                        fullscreen = True
                        menuscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
                    else:
                        fullscreen = False
                        menuscreen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

                # Entering or exit fullscreen mode
                if event.key == pygame.K_f:

                    # Making fullscreen the opposite value
                    fullscreen = not fullscreen

                    # Enters fullscreen
                    if fullscreen:

                        # Saving the values of the screen before entering the fullscreen
                        exit_fullscreen_past_width = current_width
                        exit_fullscreen_past_height = current_height

                        # Creates the fullscreen
                        menuscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)

                    # Exits fullscreen
                    else:
                        menuscreen = pygame.display.set_mode((exit_fullscreen_past_width, exit_fullscreen_past_height), pygame.RESIZABLE)

                # TODO: A Tutorial should be added; Maybe with some buttons - should be at the end of the project
                # Entering tutorial
                if event.key == pygame.K_t:
                    tutorial()

                # Quitting the mainmenu by pressing "Q"
                if event.key == pygame.K_q:
                    running_mainmenu = False
                    pygame.quit()
                    quit()
                    break

        # Updates Display
        pygame.display.update()
