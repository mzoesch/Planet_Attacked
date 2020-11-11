import pygame
import os
from pygame.locals import *

# Declaring variables
current_width = 0
current_height = 0
running_settings = True
clicked = False
checkboxes = []

# Creating colors
TITLE_BLUE = (0, 0, 204)
SUBTEXT_PINK = (255, 0, 127)
WHITE = pygame.Color("white")
BACKGROUND_COLOR = (19, 17, 17)
BLACK = pygame.Color("black")
settingsscreen = None


# Getting the size values of the current window
def currents():

    global current_width
    global current_height

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()


# Class for checkbox
class Checkbox:

    def __init__(self, x, y, size=20, inside_pixels=4):
        self.x = x
        self.y = y
        self.size = size
        self.inside_pixels = inside_pixels

        # Getting the screen values of the monitor that the user is playing on
        with open("assets/monsiz.txt", "r") as msf:
            window_size = msf.readlines()
            monitor_sizeX = int(window_size[0])
            monitor_sizeY = int(window_size[1])

        if current_width == monitor_sizeX and current_height == monitor_sizeY:
            self.checked = True
        else:
            self.checked = False

        self.outside_box = pygame.Rect(self.x, self.y, self.size, self.size)
        self.inside_box = pygame.Rect(self.x + 2, self.y + 2,  self.size - self.inside_pixels,  self.size - self.inside_pixels)

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.outside_box)
        pygame.draw.rect(window, BACKGROUND_COLOR, self.inside_box)
        self.checking_checked()
        if self.checked:
            pass

    def checking_checked(self):
        global clicked
        global settingsscreen

        # Checking mouse coordinates
        mx, _ = pygame.mouse.get_pos()
        _, my = pygame.mouse.get_pos()

        # Checking if a box was clicked or the cursor is over the button
        if self.outside_box.collidepoint((mx, my)) and clicked:

            if self.checked:
                self.checked = False
                settingsscreen = pygame.display.set_mode((current_width, current_height))

            else:
                # Getting the screen values of the monitor that the user is playing on
                with open("assets/monsiz.txt", "r") as msf:
                    window_size = msf.readlines()
                    monitor_sizeX = int(window_size[0])
                    monitor_sizeY = int(window_size[1])

                self.checked = True
                settingsscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)

            clicked = False


# Function for the settings menu
def settings():

    global current_width
    global current_height
    global running_settings
    global clicked
    global checkboxes
    global settingsscreen

    # Drawing current frame
    def draw_current_frame():

        # Shows the background
        settingsscreen.blit(settingsmenu_background, (0, 0))

        # Drawing labels
        settingsscreen.blit(NAME_LABEL, (name_label_x, name_label_y))
        settingsscreen.blit(SUBTEXT_LABEL, (subtext_label_x, subtext_label_y))
        settingsscreen.blit(FULLSCREEN_LABEL, (fullscreen_label_x, fullscreen_label_y))

        # Drawing checkbox
        for current_checkbox in checkboxes:
            current_checkbox.draw(settingsscreen)

        # Drawing button
        show_button(20, height_for_button, "< Back", button_width, button_height, (150, 0, 0), (255, 0, 0), "b")

    # Shows buttons
    def show_button(x, y, message, width, height, normal_color, active_color, purpose):

        global running_settings
        global clicked

        # Makes a button
        button = pygame.Rect(x, y, width, height)

        # Checking if a box was clicked or the cursor is over the button
        if button.collidepoint((mx, my)):
            pygame.draw.rect(settingsscreen, active_color, button)

            if clicked:
                if purpose == "b":
                    running_settings = False
                    clicked = False

        else:
            pygame.draw.rect(settingsscreen, normal_color, button)

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
        settingsscreen.blit(button_label, (message_x, message_y))

    # Getting the screen values of the monitor that the user is playing on
    with open("assets/monsiz.txt", "r") as msf:
        window_size = msf.readlines()
        monitor_sizeX = int(window_size[0])
        monitor_sizeY = int(window_size[1])

    # Getting current size of window
    currents()

    # Checking fullscreen
    if current_width == monitor_sizeX and current_height == monitor_sizeY:
        settingsscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        settingsscreen = pygame.display.set_mode((current_width, current_height))

    # Setting variables
    running_settings = True
    clicked = False
    checkboxes = []

    # Creating fonts
    name_font = pygame.font.SysFont("digital7monottf", 100)
    subtext_font = pygame.font.SysFont("snapitc", 25)
    controls_font = pygame.font.SysFont("msreferencesansserif", 25)
    button_font = pygame.font.SysFont("Comic Sans MS", 40)
    
    # Creating labels
    NAME_LABEL = name_font.render("PLANET ATTACKED", True, TITLE_BLUE)
    SUBTEXT_LABEL = subtext_font.render("menu for settings", True, SUBTEXT_PINK)
    FULLSCREEN_LABEL = controls_font.render("Fullscreen     ", True, WHITE)

    # Standard values for buttons
    button_width = 170
    button_height = 60
    height_for_button = current_height - 80

    # Making the checkbox
    for checkbox in range(1):
        size = 20
        checkbox = Checkbox(100, 100, size)
        checkboxes.append(checkbox)

    # While loop for settings menu
    while running_settings:

        # Defining the pause menu background
        settingsmenu_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Main_Menu.png")), (current_width, current_height))

        # Calculating coordinates and size
        NAME_LABEL_WIDTH = pygame.Surface.get_width(NAME_LABEL)
        name_label_x = (current_width - NAME_LABEL_WIDTH) / 2
        name_label_y = 30
        NAME_LABEL_HEIGHT = pygame.Surface.get_height(NAME_LABEL)
        SUBTEXT_LABEL_WIDTH = pygame.Surface.get_width(SUBTEXT_LABEL)
        subtext_label_x = (current_width - SUBTEXT_LABEL_WIDTH) / 2
        subtext_label_y = name_label_y + NAME_LABEL_HEIGHT
        fullscreen_label_x = current_width / 3
        fullscreen_label_y = 500
        FULLSCREEN_LABEL_WIDTH = pygame.Surface.get_width(FULLSCREEN_LABEL)
        FULLSCREEN_LABEL_HEIGHT = pygame.Surface.get_height(FULLSCREEN_LABEL)



        # Checking mouse coordinates
        mx, _ = pygame.mouse.get_pos()
        _, my = pygame.mouse.get_pos()

        # Drawing window
        draw_current_frame()

        # Checking events
        for event_settings in pygame.event.get():

            # Quitting the game by closing the window
            if event_settings.type == pygame.QUIT:
                running_settings = False
                pygame.mixer.quit()
                pygame.quit()
                quit()
                break

            # Checks if a key is pressed
            if event_settings.type == pygame.KEYDOWN:

                # Quitting settings by pressing "q"
                if event_settings.key == pygame.K_q:
                    running_settings = False
                    break

                # Quitting settings menu
                if event_settings.key == pygame.K_ESCAPE:
                    running_settings = False
                    break

            # Detects mouse button clicks and sets clicked to False
            clicked = False
            if event_settings.type == MOUSEBUTTONDOWN:
                if event_settings.button == 1:
                    clicked = True

        # Update the screen
        pygame.display.update()
