import pygame
from data.Window_Size_File import width
from data.Window_Size_File import hight
from data.Window_Size_File import gamescreen
from data.Window_Size_File import gameover_background


def gameover():

    # Reads the current score

    with open("data/Currentscore_File.txt", "r") as csf:
        score_value = csf.read()

    # Describes how the "GAME OVER" Text looks like

    go_color = pygame.Color("red")
    over_font = pygame.font.Font("freesansbold.ttf", 64)
    go_rendered = over_font.render("GAME OVER", True, go_color)

    # Describes how the score looks like

    sc_color = pygame.Color("yellow")
    sc_font = pygame.font.Font("freesansbold.ttf", 48)
    sc_rendered = sc_font.render(f"Your score: {score_value}", True, sc_color)

    # Get the size of the "GAME OVER" text

    go_text_width, _ = pygame.Surface.get_size(go_rendered)
    _, go_text_hight = pygame.Surface.get_size(go_rendered)

    # Get the size of the score text

    sc_text_width, _ = pygame.Surface.get_size(sc_rendered)

    # Calculating the cooridnates of the "GAME OVER" text

    go_center_text_width = (width - go_text_width) / 2
    go_center_text_hight = (hight - go_text_hight) / 2

    # Calculating the cooridnates of the score text

    sc_center_text_width = (width - sc_text_width) / 2
    sc_center_text_hight = (hight - 200)

    # Renders it

    gamescreen.blit(gameover_background, (0, 0))

    gamescreen.blit(go_rendered, (go_center_text_width, go_center_text_hight))

    gamescreen.blit(sc_rendered, (sc_center_text_width, sc_center_text_hight))

    pygame.display.update()
