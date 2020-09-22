import pygame
import os

# Setting up variables that are used everywhere
score_value = 0
current_width = 0  # Should be "None" but than the IDLE will show so many warnings ;-(
current_height = 0
paused_text_center_width = 0
paused_text_center_height = 0
subtext_center_width = 0
subtext_center_height = 0
counter = 0  # Just a counter that has the purpose that the score_value won't be shown if there is a new highscore existing
score_label = None
warning_label = None


# Getting the size values of the current window
def currents():
    global current_width
    global current_height
    global score_value

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()


# Function for the pause menu
def pausemenu():
    # Adding:
    # New Screen
    # Text; "Paused"; In Progress

    # Making variables global
    global paused_text_center_width
    global score_label
    global warning_label
    global paused_text_center_height
    global subtext_center_width
    global subtext_center_height
    global counter

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

    # Getting current score
    with open("assets/sv_pm.txt", "r") as sv_pmf:
        global score_value
        score_value = sv_pmf.read()

    # Getting the screen values of the monitor that the user is playing on
    with open("assets/monsiz.txt", "r") as msf:
        window_size = msf.readlines()
        monitor_sizeX = int(window_size[0])
        monitor_sizeY = int(window_size[1])

    # Getting current size of window
    currents()

    # Checking fullscreen
    if current_width == monitor_sizeX and current_height == monitor_sizeY:
        menuscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        menuscreen = pygame.display.set_mode((current_width, current_height))

    # Reads the current highscore
    with open("assets/hs.txt", "r") as hsf:
        current_highscore_value = hsf.read()

    # Setting a variable
    running_pausemenu = True

    # Defining the pause menu background
    pausemenu_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Standard.png")), (current_width, current_height))

    # Shows the background
    menuscreen.blit(pausemenu_background, (0, 0))

    # Defining some colors
    RED = pygame.Color("red")
    PINK = pygame.Color("pink")
    GREEN = pygame.Color("blue")
    YELLOW = pygame.Color("yellow")

    # Creating some fonts
    standard_font = pygame.font.SysFont("freesansbold.ttf", 64)
    paused_font = pygame.font.Font("freesansbold.ttf", 128)
    subtext_paused_font = pygame.font.Font("freesansbold.ttf", 32)
    warning_font = pygame.font.SysFont("freesansbold.ttf", 32)
    if (int(current_highscore_value) + 1) > int(score_value):
        highscore_label = standard_font.render(f"Highscore: {current_highscore_value}", True, RED)
        score_label = standard_font.render(f"Current score: {score_value}", True, GREEN)
        counter = 0
    else:
        highscore_label = standard_font.render(f"NEW Highscore: {score_value}", True, RED)
        warning_label = warning_font.render("You have to die to save your current score as your new highscore", True, RED)

    # Renders labels

    # Simple labels
    paused_label = paused_font.render("Game paused...", True, PINK)
    subtext_paused_label = subtext_paused_font.render("Press ESCAPE to continue playing", True, YELLOW)

    # Not so simple labels
    size_getting_and_calculating()

    # Draws the rendered labels
    menuscreen.blit(paused_label, (paused_text_center_width, paused_text_center_height))
    menuscreen.blit(subtext_paused_label, (subtext_center_width, subtext_center_height))
    menuscreen.blit(highscore_label, (10, 10))

    # Trying to draw labels ;-)
    try:
        if counter < 1:
            menuscreen.blit(score_label, (current_width - score_label.get_width() - 10, 10))
    except AttributeError:
        pass
    try:
        menuscreen.blit(warning_label, (10, current_height - warning_label.get_height() - 10))
    except AttributeError:
        pass

    # Counts the counter one up
    counter += 1

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
