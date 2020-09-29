import pygame
import os

# Setting up variables that are used everywhere
current_width = 0  # Should be "None" but than the IDLE will show so many warnings ;-(
current_height = 0
paused_text_center_width = 0
paused_text_center_height = 0
subtext_center_width = 0
subtext_center_height = 0
score_label = None
warning_label = None


# Getting the size values of the current window
def currents():
    global current_width
    global current_height

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()


# Function for the pause menu
def pausemenu():

    # Making variables global
    global paused_text_center_width
    global score_label
    global warning_label
    global paused_text_center_height
    global subtext_center_width
    global subtext_center_height

    # Just some calculating for the paused screen
    def size_getting_and_calculating():

        # Making some variables global
        global paused_text_center_width
        global paused_text_center_height
        global subtext_center_width
        global subtext_center_height

        # Gets the size of the "Game paused..." text
        paused_text_width, _ = pygame.Surface.get_size(paused_label)
        _, paused_text_height = pygame.Surface.get_size(paused_label)

        # Gets the size of the subtext label
        subtext_width, _ = pygame.Surface.get_size(subtext_paused_label)
        _, subtext_height = pygame.Surface.get_size(subtext_paused_label)

        # Calculating the coordinates of the "Game paused..." text
        paused_text_center_width = current_width / 2 - paused_text_width / 2
        paused_text_center_height = current_height / 2 - paused_text_height / 2

        # Calculating the coordinates of the score text
        subtext_center_width = current_width / 2 - subtext_width / 2
        subtext_center_height = paused_text_center_height + subtext_height + 128

    # Getting the screen values of the monitor that the user is playing on
    with open("assets/monsiz.txt", "r") as msf:
        window_size = msf.readlines()
        monitor_sizeX = int(window_size[0])
        monitor_sizeY = int(window_size[1])

    # Getting current size of window
    currents()

    # Checking fullscreen
    if current_width == monitor_sizeX and current_height == monitor_sizeY:
        pausescreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        pausescreen = pygame.display.set_mode((current_width, current_height))

    # Setting a variable
    running_pausemenu = True

    # Defining the pause menu background
    pausemenu_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Pause_Menu.png")), (current_width, current_height))

    # Shows the background
    pausescreen.blit(pausemenu_background, (0, 0))

    # Defining some colors
    PINK = pygame.Color("pink")
    YELLOW = pygame.Color("yellow")

    # Creating some fonts
    paused_font = pygame.font.Font("freesansbold.ttf", 128)
    subtext_paused_font = pygame.font.Font("freesansbold.ttf", 32)

    # Renders labels

    # Simple labels
    paused_label = paused_font.render("Tutorial paused...", True, PINK)
    subtext_paused_label = subtext_paused_font.render("Press ESCAPE to continue playing", True, YELLOW)

    # Not so simple labels
    size_getting_and_calculating()

    # Draws the rendered labels
    pausescreen.blit(paused_label, (paused_text_center_width, paused_text_center_height))
    pausescreen.blit(subtext_paused_label, (subtext_center_width, subtext_center_height))

    # Update the screen
    pygame.display.update()

    # While loop for pausemenu
    while running_pausemenu:
        for event_pause in pygame.event.get():

            # Quitting the game by closing the window
            if event_pause.type == pygame.QUIT:
                running_pausemenu = False
                pygame.mixer.quit()
                pygame.quit()
                quit()
                break

            # Checks if a key is pressed
            if event_pause.type == pygame.KEYDOWN:

                # Quitting pausemenu by pressing "q"
                if event_pause.key == pygame.K_q:
                    running_pausemenu = False
                    break

                # Quitting pause menu
                if event_pause.key == pygame.K_ESCAPE:
                    running_pausemenu = False
                    break
