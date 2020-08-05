# Main File
# This file sets the basics things

import pygame
from data.Resources_Loading_File import IMG_APPICON
from data.Mainmenu_File import mainmenu


# Main function
def main():

    AUTHOR = "Magnus Zoeschinger"

    # Setting up the screen
    # Window name
    pygame.display.set_caption(f"Planet Attacked @{AUTHOR}")

    # What you see when switching between apps
    pygame.display.set_icon(IMG_APPICON)

    # Starting the mainmenu
    mainmenu()
