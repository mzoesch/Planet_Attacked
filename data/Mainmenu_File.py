# Main Menu file
# This file makes the main menu

import pygame
from data.WindowSize_File import *
from data.Game_File import game
from data.Tutorial_File import tutorial
import os
from pygame.locals import *
from data.Settings_File import settings

# Creates the menu screen
menuscreen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
play_game = None

# Declaring variables
clicked = False


# Mainmenu function
def mainmenu():

    global play_game
    global clicked
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
    clicked = False

    # Y-Value of the Highscore
    HIGHSCORE_TEXTY = 10

    # The function which is responsible for printing out the players high score in the top right corner
    def show_highscore(y):

        # Get the highscore from the file
        with open("assets/hs.txt", "r") as hsf:
            highscore_value = hsf.read()

        # Reads the last score from the file
        with open("assets/sv.txt", "r") as sv_bs_f:
            score_value_before_start = sv_bs_f.read()

        # Checking if there is a new highscore
        if score_value_before_start > highscore_value:
            highscore_value = score_value_before_start
            with open("assets/sv.txt", "w") as sv_bf_w_f:
                sv_bf_w_f.write('%d' % int(score_value_before_start))

        # Renders it
        HIGHSCORE_FONT = pygame.font.SysFont("jokerman", 32)
        rendered_highscore = HIGHSCORE_FONT.render(f"Highscore: {highscore_value}", True, (255, 0, 255))

        # Correct placement
        text_width, _ = pygame.Surface.get_size(rendered_highscore)
        x = current_width - text_width - 10

        # Shows it
        menuscreen.blit(rendered_highscore, (x, y))

    # Draws the buttons
    def show_button(x, y, message, width, height, normal_color, active_color, purpose):

        global clicked

        # Makes a button
        button = pygame.Rect(x, y, width, height)

        # Checking if a box was clicked or the cursor is over the button
        if button.collidepoint((mx, my)):
            pygame.draw.rect(menuscreen, active_color, button)
            if clicked:
                if purpose == "p":
                    game()
                    clicked = False
                elif purpose == "t":
                    # tutorial()
                    clicked = False
                elif purpose == "s":
                    # settings()
                    clicked = False

        else:
            pygame.draw.rect(menuscreen, normal_color, button)

        # Creating and showing the labels

        # Creates label
        button_label = button_font.render(message, True, BLACK)

        # Gets the size of the label
        message_width, _ = pygame.Surface.get_size(button_label)
        _, message_height = pygame.Surface.get_size(button_label)

        # Calculating the right coordinates of the message on the button
        message_x = (width / 2 - message_width / 2) + x
        message_y = (height / 2 - message_height / 2) + y

        # Printing it to the screen
        menuscreen.blit(button_label, (message_x, message_y))

    # Main menu loop
    while running_mainmenu:

        # Setting up the right screen size and fullscreen mode

        # Checking the size of the window
        current_width, _ = pygame.display.get_surface().get_size()
        _, current_height = pygame.display.get_surface().get_size()

        # Making the background the correct size
        mainmenu_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Main_Menu.png")), (current_width, current_height))

        # Shows the background
        menuscreen.blit(mainmenu_background, (0, 0))

        # This line shows the highscore
        show_highscore(HIGHSCORE_TEXTY)

        # Checking mouse coordinates
        mx, _ = pygame.mouse.get_pos()
        _, my = pygame.mouse.get_pos()

        # Creating fonts
        button_font = pygame.font.SysFont("Comic Sans MS", 40)
        name_font = pygame.font.SysFont("digital7monottf", 128)
        subtext_font = pygame.font.SysFont("snapitc", 32)
        warning_font = pygame.font.SysFont("centuryschoolbook", 16)

        # Creating a standard color
        BLACK = pygame.Color("black")
        RED = pygame.Color("red")

        # Creating not standard colors
        TITLE_BLUE = (0, 0, 204)
        SUBTEXT_PINK = (255, 0, 127)

        # Creating labels
        NAME_LABEL = name_font.render("PLANET ATTACKED", True, TITLE_BLUE)
        SUBTEXT_LABEL = subtext_font.render("CREATOR: Magnus Zoeschinger", True, SUBTEXT_PINK)
        WARNING_LABEL = warning_font.render("Settings and Tutorial are not available.", True, RED)

        # Calculating coordinates
        NAME_LABEL_WIDTH = pygame.Surface.get_width(NAME_LABEL)
        name_label_x = (current_width - NAME_LABEL_WIDTH) / 2
        SUBTEXT_LABEL_WIDTH = pygame.Surface.get_width(SUBTEXT_LABEL)
        subtext_label_x = (current_width - SUBTEXT_LABEL_WIDTH) / 2
        NAME_LABEL_HEIGHT = pygame.Surface.get_height(NAME_LABEL)
        SUBTEXT_LABEL_HEIGHT = pygame.Surface.get_height(SUBTEXT_LABEL)
        name_label_y = ((current_height - NAME_LABEL_HEIGHT) / 2) - SUBTEXT_LABEL_HEIGHT
        subtext_label_y = name_label_y + SUBTEXT_LABEL_HEIGHT + 50
        WARNING_LABEL_x, WARNING_LABEL_y = 10, 10

        # Printing labels to screen
        menuscreen.blit(NAME_LABEL, (name_label_x, name_label_y))
        menuscreen.blit(SUBTEXT_LABEL, (subtext_label_x, subtext_label_y))
        menuscreen.blit(WARNING_LABEL, (WARNING_LABEL_x, WARNING_LABEL_y))

        # Standard values for buttons
        button_width = 170
        button_height = 60
        height_for_button = current_height - 80

        # Drawing the buttons
        show_button(current_width - 190, height_for_button, "Play", button_width, button_height, (0, 150, 0), (0, 255, 0), "p")
        show_button(current_width - 190 - 170 - 20, height_for_button, "Tutorial", button_width, button_height, (226, 221, 79), (255, 247, 0), "t")
        show_button(20, height_for_button, "Settings", button_width, button_height, (150, 0, 0), (255, 0, 0), "s")

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
                    # tutorial()
                    pass

                # Quitting the mainmenu by pressing "Q"
                if event.key == pygame.K_q:
                    running_mainmenu = False
                    pygame.quit()
                    quit()
                    break

                # Settings
                if event.key == pygame.K_s:
                    # settings()
                    pass

            # Detects mouse button clicks and sets clicked to False
            clicked = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        # Updates display
        pygame.display.update()
