import pygame

# Initialize the pygame
pygame.init()


# Gets the value of the monitor size that you are using
def get_monitor_size():
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

    # Writes the value to a file
    with open("assets/monsiz.txt", "w") as msf:
        msf.write('%s\n' % monitor_size[0])
    with open("assets/monsiz.txt", "a") as msf:
        msf.write('%s\n' % monitor_size[1])
