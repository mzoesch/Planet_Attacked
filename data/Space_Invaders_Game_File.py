import pygame
import math
import random
from pygame import mixer
from time import sleep
from data.Music_File import play_random_songs
from data.Death_File import gameover
from data.Window_Size_File import gamescreen
from data.Window_Size_File import game_background

pygame.init()

# Player

playerImg = pygame.image.load("resources/graphics/space_invaders_ship(64).png")
playerX = 468
playerY = 500
playerX_Change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 1  # Number of enemies in the screen

# Lets the game create more than one enemy

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("resources/graphics/enemy(64).png"))
    enemyX.append(random.randint(0, 936))
    enemyY.append(random.randint(-200, -64))
    enemyX_Change.append(6)
    enemyY_Change.append(20)

# Bullet
# Ready - You cant see the bullet
# Fire - The bullet is moving and can be seen

bulletImg = pygame.image.load("resources/graphics/bullet_laser(32).png")
bulletX = 0
bulletY = 500  # This is also the "y" where the space ship is located
bulletX_Change = 0
bulletY_Change = 5  # Defines how much time the bullet needs to the top of the screen
bullet_state = "ready"

# Score
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)

# The location where the score can be seen by the player

score_textX = 10
score_textY = 10

# Game over text

over_font = pygame.font.Font("freesansbold.ttf", 64)

# The function whis is reponsible for printing out the players score on the top left corner


def show_score(x, y):
    score = score_font.render(f"Score: {score_value}", True, (255, 255, 255))
    gamescreen.blit(score, (x, y))


# The function which is reponsible for printing out the players postion


def player(x, y):
    gamescreen.blit(playerImg, (x, y))

# The function which is reponsible for printing each postion of an enemy


def enemy(x, y, j):
    gamescreen.blit(enemyImg[j], (x, y))


# The function which is reponsible for showing the bullet that was "ready"


def fire_bullet(x, y):

    global bullet_state

    bullet_state = "fire"

    # Makes the bullet realistic (so that it is shooted in middle of the space ship)

    gamescreen.blit(bulletImg, (x + 16, y + 10))


# Detects if the bullet is very near to a space ship

def is_collision(enemyx, enemyy, bulletx, bullety):

    # Just some math for collision detection

    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))

    if distance < 27:

        return True

    else:

        return False

# Game function


def game():

    # Making the player global

    global playerX
    global playerY
    global playerX_Change

    # Making the bullet global

    global bulletX
    global bulletY
    global bulletX_Change
    global bulletY_Change
    global bullet_state
    global i

    # Making the rest global

    global score_value
    global num_of_enemies

    # Resets everything so that you can play it more than onece in a row

    pygame.mixer.init()
    game_over = False
    running_game = True
    skip_game_over_text = False
    score_value = 0

    # Game Loop

    while running_game:

        # Creates more enemies when the score gehts higher

        for i in range(num_of_enemies):
            enemyImg.append(pygame.image.load("resources/graphics/enemy(64).png"))
            enemyX.append(random.randint(0, 936))
            enemyY.append(random.randint(-200, -64))
            enemyX_Change.append(6)
            enemyY_Change.append(20)

        # Background music

        play_random_songs()

        # Backscreen

        gamescreen.blit(game_background, (0, 0))

        # Events - detects events like what is pressed or if the window is colsed

        for event in pygame.event.get():

            # Game Close

            if event.type == pygame.QUIT:
                running_game = False
                skip_game_over_text = True
                break

            # Detects if a key is pressed

            if event.type == pygame.KEYDOWN:

                # Quitting the game by pressing "Q"

                if event.key == pygame.K_q:
                    running_game = False
                    skip_game_over_text = True
                    break

                # Moving the ship

                if event.key == pygame.K_LEFT:
                    playerX_Change = -10
                if event.key == pygame.K_a:
                    playerX_Change = -10
                if event.key == pygame.K_RIGHT:
                    playerX_Change = 10
                if event.key == pygame.K_d:
                    playerX_Change = 10

                # Bullet fire

                if event.key == pygame.K_SPACE:

                    # Detects if a bullit is already been fired

                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        bullet_sound = mixer.Sound("resources/sounds/Laser-Space_Invaders.wav")
                        bullet_sound.play()

            # Detects if the player isn't pressing the key anymore

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_Change = 0

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_Change = 0

        # This line actually moves the player by the value of playerX_Change

        playerX += playerX_Change

        # Checking for boundaries

        if playerX <= 0:
            playerX = 0
        elif playerX >= 936:
            playerX = 936

        # Enemy Movment

        for i in range(num_of_enemies):

            # Detects if an enemy has crossed the line

            if enemyY[i] > 390:  # Default: 390 (This is often changed by me while testing)

                game_over = True
                break

            # Moves an enemy

            enemyX[i] += enemyX_Change[i]

            if enemyX[i] <= 0:
                enemyX_Change[i] = 6
                enemyY[i] += enemyY_Change[i]
            elif enemyX[i] >= 936:
                enemyX_Change[i] = -6
                enemyY[i] += enemyY_Change[i]

            # Collision

            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)

            # If "collision" is returning true

            if collision:
                explosion_sound = mixer.Sound("resources/sounds/Explosion-Space_Invaders.wav")
                explosion_sound.play()
                bullet_state = "ready"
                bulletY = playerY
                score_value += 1
                enemyX[i] = random.randint(0, 936)
                enemyY[i] = -64

            # This line shows the enemis

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement

        # Allows you to fire as often as you like and "delets" the bullet that has been shooted out of the window

        if bulletY <= -32:
            bullet_state = "ready"
            bulletY = playerY

        # This is the statement where the bullet is traviling to the top

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_Change  # This is minus because zero is at the top of the window

        # This line shows the player

        player(playerX, playerY)

        # Calls the function where the score is printed out

        show_score(score_textX, score_textY)

        # This line is updating the screen, so that is does not turn black

        pygame.display.update()

        # Game Over

        if game_over:
            pygame.mixer.quit()
            break

        # Creates more enemies over time

        if score_value == 1 and num_of_enemies == 1:
            num_of_enemies = 6

        elif score_value == 10 and num_of_enemies == 6:
            num_of_enemies = 10

        elif score_value == 20 and num_of_enemies == 10:
            num_of_enemies = 15

        elif score_value == 25 and num_of_enemies == 15:
            num_of_enemies = 20

        elif score_value == 30 and num_of_enemies == 20:
            num_of_enemies = 25

        elif score_value == 35 and num_of_enemies == 35:
            num_of_enemies = 30

        elif score_value == 40 and num_of_enemies == 30:
            num_of_enemies = 35

        elif score_value == 50 and num_of_enemies == 35:
            num_of_enemies = 60

        sleep(0.005)

    def reset_play_again():

        global bulletX
        global bulletY
        global bulletX_Change
        global bullet_state
        global playerX_Change
        global playerX
        global num_of_enemies

        # Resets the bullet

        bulletX = 0
        bulletY = 500  # This is also the "y" where the space ship is located
        bulletX_Change = 0
        bullet_state = "ready"

        # Resets the coorinates of the players ship

        playerX_Change = 0
        playerX = 468

        # Resets the enemies coorinates

        for j in range(num_of_enemies):
            enemyY[j] = random.randint(-200, -64)
            enemyX[j] = random.randint(0, 936)

        # Resets the number of enemies that are on the screen

        num_of_enemies = 1

    if not skip_game_over_text:

        # Resets everything

        reset_play_again()

        # Shows the game over messeage

        with open("data/Currentscore_File.txt", "w") as csf:
            csf.write('%d' % score_value)

        gameover()

        sleep(5)

        # Opens the current highscore

        with open("data/hs.txt", "r") as hsf:
            highscore_value = hsf.read()

        # Checks if there is a new highscore

        if score_value > int(highscore_value):

            with open("data/hs.txt", "w") as hsf:
                hsf.write('%d' % score_value)

            print("Good Job")
            print(score_value)
            print(highscore_value)

        else:

            pass

    else:

        # Resets everything

        reset_play_again()

        # Stops the music that we dont want to hear in the mainmenu

        pygame.mixer.quit()
