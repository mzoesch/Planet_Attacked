# Created 26.06.2020
# Last modified 20.09.2020
# Creator @Magnus Zoeschinger

import pygame
import sys
from data.Important_Functions_File import get_monitor_size

# Initialize the pygame
pygame.init()

# Gets the value of the monitor size that you are using
get_monitor_size()

# Must be under the 'get_monitor_size()' function because of 'bugs' with pygame
from data.Main_File import main

# Starting up the game
main()

# Quitting the game
pygame.quit()
sys.exit()
