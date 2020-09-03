import os
import pygame
import random
from data.Music_File import play_random_songs
from data.Resources_Loading_File import IMG_ENEMY_LASER_BLUE
from data.Resources_Loading_File import IMG_ENEMY_LASER_RED
from data.Resources_Loading_File import IMG_ENEMY_LASER_GREEN
from data.Resources_Loading_File import IMG_ENEMY_SHIP_BLUE
from data.Resources_Loading_File import IMG_ENEMY_SHIP_GREEN
from data.Resources_Loading_File import IMG_ENEMY_SHIP_RED
from data.Resources_Loading_File import IMG_PLAYER_SHIP
from data.Resources_Loading_File import IMG_PLAYER_LASER
from data.Resources_Loading_File import SHIP_EXPLOSION

# Initialize the font
pygame.font.init()
pygame.mixer.init()
pygame.init()

# Setting up variables that are used everywhere
score_value = 0
mainexplosions = []

current_width = 0  # Should be "None" but than the IDLE will show so many warnings ;-(
current_height = 0


def currents():

    global current_width
    global current_height

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()


# Explosion class
class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.to_generate = 10
        self.particles_up = []
        self.particles_right = []
        self.particles_down = []
        self.particles_left = []
        self.particles_left_up = True
        self.particles_left_right = True
        self.particles_left_down = True
        self.particles_left_left = True
        self.particles_in_game = True

    def draw(self, window):
        if self.to_generate > 0:
            self.particles_up.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_right.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_down.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.particles_left.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 5)])
            self.to_generate -= 1

        for particle in self.particles_up:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_up.remove(particle)
            if not self.particles_up:
                self.particles_left_up = False

        for particle in self.particles_right:
            particle[0][0] -= particle[1][1]
            particle[0][1] += particle[1][0]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_right.remove(particle)
            if not self.particles_right:
                self.particles_left_right = False

        for particle in self.particles_down:
            particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_down.remove(particle)
            if not self.particles_down:
                self.particles_left_down = False

        for particle in self.particles_left:
            particle[0][0] += particle[1][1]
            particle[0][1] += particle[1][0]
            particle[2] -= 0.1
            pygame.draw.circle(window, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles_left.remove(particle)
            if not self.particles_left:
                self.particles_left_left = False

        if not self.particles_left_up and self.particles_left_right and self.particles_left_down and self.particles_left_left:
            self.particles_in_game = False


# Laser class
class Laser:

    def __init__(self, x, y, laser_img):
        self.x = x
        self.y = y
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.laser_img)

    # Draws the laser
    def draw(self, screen):
        screen.blit(self.laser_img, (self.x, self.y))

    # Moves the laser by the value of "velocity"
    def move(self, velocity):
        self.y += velocity

    # Returns a boolean value if the laser has crossed the screen
    def off_screen(self):
        return not (current_height + self.get_height() > self.y >= -self.get_height())

    # Returns a boolean value if the laser has collided with an other obj
    def collision(self, obj):
        return collide(self, obj)

    # Gets the height of the laser
    def get_height(self):
        return self.laser_img.get_height()


# Class that has the purpose that I don't have to copy so much code
class Ship:

    # Defines how often you can shoot
    # 30 equals 0.5 seconds because 30[COOL_DOWN] / 60[FPS] = 0.5[seconds]
    COOL_DOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser_img_height = None
        self.lasers = []
        self.cool_down_counter = 0

    # Draws the objects to the screen
    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    # Enemies lasers
    def move_lasers(self, velocity, player):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(player):
                player.health -= 10
                self.lasers.remove(laser)

    # Counts the cooldown
    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Lets the player shoot
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y - (self.laser_img_height / 2), self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Gets the width of the ship
    def get_width(self):
        return self.ship_img.get_width()

    # Gets the height of the ship
    def get_height(self):
        return self.ship_img.get_height()


# Player class
class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(IMG_PLAYER_SHIP, (70, 70))
        self.laser_img = pygame.transform.scale(IMG_PLAYER_LASER, (70, 70))
        self.laser_img_height = 70
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # Moves the lasers and deletes them
    def move_lasers(self, velocity, enemies):

        # Making score_value global
        global score_value

        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy):

                        # If the ship laser has collided with the enemy
                        for explosion in range(1):
                            explosion = Explosion(enemy.x, enemy.y)
                            explosion.x += 35
                            explosion.y += 35
                            mainexplosions.append(explosion)
                        explosion_sound = pygame.mixer.Sound(SHIP_EXPLOSION)
                        explosion_sound.play()

                        # Respawns the enemy that was exploded
                        enemy.y = random.randrange(-100, 0) - enemy.get_height()
                        enemy.x = random.randrange(0, current_width - enemy.get_width())
                        enemy.ship_img, enemy.laser_img = random.choice([
                            (pygame.transform.scale(IMG_ENEMY_SHIP_RED, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_RED, (70, 70))),
                            (pygame.transform.scale(IMG_ENEMY_SHIP_BLUE, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_BLUE, (70, 70))),
                            (pygame.transform.scale(IMG_ENEMY_SHIP_GREEN, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_GREEN, (70, 70)))
                        ])
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        score_value += 1

    # Draws the player
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Healthbar drawing
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))


# Enemy class
class Enemy(Ship):

    # Each ship that can be created
    COLOR_MAP = {
        "red": (pygame.transform.scale(IMG_ENEMY_SHIP_RED, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_RED, (70, 70))),
        "green": (pygame.transform.scale(IMG_ENEMY_SHIP_GREEN, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_GREEN, (70, 70))),
        "blue": (pygame.transform.scale(IMG_ENEMY_SHIP_BLUE, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_BLUE, (70, 70)))
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)

        # Defines the type of an enemy ship
        self.ship_img, self.laser_img = self.COLOR_MAP[color]

        # Creates a mask
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Moves the enemy down by the value of "velocity"
    def move(self, velocity):
        self.y += velocity

    # Lets the enemies shoot randomly
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y + 10, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# Detects if objects have been collided
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) is not None


# Game function
def game():

    # Making score_value global
    global score_value

    # Draws everything
    def draw_current_frame():

        # Shows the background
        gamescreen.blit(game_background, (0, 0))

        # Renders labels
        lives_label = standard_font.render(f"Lives: {lives}", True, (255, 255, 255))
        score_label = standard_font.render(f"Score: {score_value}", True, (255, 255, 255))

        # Draws the rendered labels
        gamescreen.blit(lives_label, (10, 10))
        gamescreen.blit(score_label, (current_width - score_label.get_width() - 10, 10))

        # Draws the enemies
        for enemy_drawing in enemies:
            enemy_drawing.draw(gamescreen)

        # Draws the explosion of an enemy
        for explosion in mainexplosions:
            if explosion.particles_in_game:
                explosion.draw(gamescreen)
            else:
                mainexplosions.remove(explosion)

        # Draws the player
        player.draw(gamescreen)

        # Refresh
        pygame.display.update()

    # Movement function
    def movement():

        # Detects if a key is pressed
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]:
            if player.x <= 0:
                player.x = 0
            else:
                player.x -= player_velocity
        if keys[pygame.K_LEFT]:
            if player.x <= 0:
                player.x = 0
            else:
                player.x -= player_velocity

        # Right
        if keys[pygame.K_d]:
            if player.x >= current_width - player.get_width():
                player.x = current_width - player.get_width()
            else:
                player.x += player_velocity
        if keys[pygame.K_RIGHT]:
            if player.x >= current_width - player.get_width():
                player.x = current_width - player.get_width()
            else:
                player.x += player_velocity

        # Up
        if keys[pygame.K_w]:
            if player.y <= one_third_of_screen():
                player.y = one_third_of_screen()
            else:
                player.y -= player_velocity
        if keys[pygame.K_UP]:
            if player.y <= one_third_of_screen():
                player.y = one_third_of_screen()
            else:
                player.y -= player_velocity

        # Down
        if keys[pygame.K_s]:
            if player.y >= current_height - player.get_height():
                player.y = current_height - player.get_height()
            else:
                player.y += player_velocity
        if keys[pygame.K_DOWN]:
            if player.y >= current_height - player.get_height():
                player.y = current_height - player.get_height()
            else:
                player.y += player_velocity

        # Player Shooting
        if keys[pygame.K_SPACE]:
            player.shoot()

    # Gets one third of the screen
    def one_third_of_screen():
        return (current_height / 3) * 2

    # Setting up the right screen size and fullscreen mode

    # Getting the screen values of the monitor that the user is playing on
    with open("assets/monsiz.txt", "r") as msf:
        window_size = msf.readlines()
        monitor_sizeX = int(window_size[0])
        monitor_sizeY = int(window_size[1])

    # Getting current size of window
    currents()

    # Checking fullscreen
    if current_width == monitor_sizeX and current_height == monitor_sizeY:
        gamescreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        gamescreen = pygame.display.set_mode((current_width, current_height))

    # Making the background of the game the correct size
    game_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Game.png")), (current_width, current_height))

    # Making the background that is used when you die, the right size
    gameover_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Standard.png")), (current_width, current_height))

    # Creating fonts
    # Standard font
    standard_font = pygame.font.SysFont("freesansbold.ttf", 64)

    # The number of enemies created each wave
    # Starting the game with one enemy
    enemies_in_game = 1

    # (Re)sets everything to default value
    FPS = 60
    running_game = True
    lives = 5
    enemies = []
    skip_game_over_text = False
    enemy_velocity = 1
    player_velocity = 5
    laser_velocity = 5
    if score_value != 0:
        score_value = 0

    # Creating the player
    player = Player(current_width / 2 - (IMG_PLAYER_SHIP.get_width() / 2), current_height - 100)

    # Clock
    clock = pygame.time.Clock()

    # Creating first enemy
    for enemy in range(enemies_in_game):
        enemy = Enemy(current_width, current_height, random.choice(["red", "blue", "green"]))

        # Spawns enemy in the middle of the screen
        enemy.x = (current_width / 2) - (enemy.get_width() / 2)
        enemy.y = 0 - enemy.get_height()

        enemies.append(enemy)

    # Initialize the mixer
    pygame.mixer.init()

    # Game loop
    while running_game:

        # Has the purpose that the computer goes through this loop in the exact time
        clock.tick(FPS)

        # Making some background music
        play_random_songs()

        # Draws each frame
        draw_current_frame()

        # Detects if you lost
        if lives <= 0 or player.health <= 0:
            running_game = False
            pygame.mixer.quit()

        # Checking events
        for event in pygame.event.get():

            # Quitting the game by closing the window
            if event.type == pygame.QUIT:
                running_game = False
                pygame.mixer.quit()
                pygame.quit()
                quit()
                break

            # Checks if a key is pressed
            if event.type == pygame.KEYDOWN:

                # Quitting game by pressing "q"
                if event.key == pygame.K_q:
                    running_game = False
                    skip_game_over_text = True
                    pygame.mixer.quit()
                    break

        # Lets you move
        movement()

        # Moves the enemies and lasers
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            # Lets the enemies shoot randomly
            # First enemy doesn't shoot
            if score_value == 0:
                pass
            else:
                if random.randrange(0, 2 * FPS) == 1:
                    enemy.shoot()

            # Creating more enemies while the score is going upwards
            if score_value == 2 and enemies_in_game == 1:

                # Adds for more enemies
                enemies_in_game += 4

                # Spawns new enemies
                for new_enemy in range(enemies_in_game):
                    new_enemy = Enemy(random.randrange(50, current_width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(new_enemy)

            # Spawns the enemy above the screen when it has collided with the player
            if collide(enemy, player):
                for explosion in range(1):
                    explosion = Explosion(enemy.x, enemy.y)
                    explosion.x += 35
                    explosion.y += 35
                    mainexplosions.append(explosion)
                explosion_sound = pygame.mixer.Sound(SHIP_EXPLOSION)
                explosion_sound.play()
                player.health -= 20
                enemy.y = random.randrange(-100, 0) - enemy.get_height()
                enemy.x = random.randrange(0, current_width - enemy.get_width())
                enemy.ship_img, enemy.laser_img = random.choice([
                    (pygame.transform.scale(IMG_ENEMY_SHIP_RED, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_RED, (70, 70))),
                    (pygame.transform.scale(IMG_ENEMY_SHIP_BLUE, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_BLUE, (70, 70))),
                    (pygame.transform.scale(IMG_ENEMY_SHIP_GREEN, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_GREEN, (70, 70)))
                ])
                score_value += 2

            # Detects if an enemy has crossed the "line"
            elif enemy.y > current_height:  # Standard: current_height
                lives -= 1
                enemy.y = random.randrange(-100, 0) - enemy.get_height()
                enemy.x = random.randrange(0, current_width - enemy.get_width())
                enemy.ship_img, enemy.laser_img = random.choice([
                    (pygame.transform.scale(IMG_ENEMY_SHIP_RED, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_RED, (70, 70))),
                    (pygame.transform.scale(IMG_ENEMY_SHIP_BLUE, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_BLUE, (70, 70))),
                    (pygame.transform.scale(IMG_ENEMY_SHIP_GREEN, (70, 70)), pygame.transform.scale(IMG_ENEMY_LASER_GREEN, (70, 70)))
                ])

        # Moves the lasers of the player and detects if they have been collided with an other object
        player.move_lasers(-laser_velocity, enemies)

    # Game over function
    def death():

        # Writes the score value to a file
        with open("assets/sv.txt", "w") as svf:
            svf.write('%d' % score_value)

        # (Re)setting everything to default value
        running_death = True
        death_count_time = 0

        # Describes how the "GAME OVER" Text looks like
        go_color = pygame.Color("red")
        over_font = pygame.font.Font("freesansbold.ttf", 128)
        go_rendered = over_font.render("GAME OVER", True, go_color)

        # Describes how the score looks like
        sc_color = pygame.Color("yellow")
        sc_font = pygame.font.Font("freesansbold.ttf", 64)
        sc_rendered = sc_font.render(f"Your score: {score_value}", True, sc_color)

        # Gets the size of the "GAME OVER" text
        go_text_width, _ = pygame.Surface.get_size(go_rendered)
        _, go_text_height = pygame.Surface.get_size(go_rendered)

        # Gets the size of the score text
        sc_text_width, _ = pygame.Surface.get_size(sc_rendered)
        _, sc_text_height = pygame.Surface.get_size(sc_rendered)

        # Calculating the coordinates of the "GAME OVER" text
        go_center_text_width = current_width / 2 - go_text_width / 2
        go_center_text_height = current_height / 2 - go_text_height / 2

        # Calculating the coordinates of the score text
        sc_center_text_width = current_width / 2 - sc_text_width / 2
        sc_center_text_height = go_center_text_height + sc_text_height + 50

        # Renders it
        gamescreen.blit(gameover_background, (0, 0))
        gamescreen.blit(go_rendered, (go_center_text_width, go_center_text_height))
        gamescreen.blit(sc_rendered, (sc_center_text_width, sc_center_text_height))

        # Refresh
        pygame.display.update()

        while running_death:

            # Has the purpose that the computer goes through this loop in the exact time
            clock.tick(FPS)

            # Checking events
            for deathevent in pygame.event.get():

                # Quitting the death screen by closing the window
                if deathevent.type == pygame.QUIT:
                    running_death = False

                    # Reads last highscore
                    with open("assets/hs.txt", "r") as hsf_read_after_play:
                        old_highscore_value = hsf_read_after_play.read()

                    # Checks if there is a new highscore
                    if int(score_value) > int(old_highscore_value):
                        with open("assets/hs.txt", "w") as hsf_write_after_play:
                            hsf_write_after_play.write(str(score_value))

                    pygame.quit()
                    quit()
                    break

                # Checks if a key is pressed
                if deathevent.type == pygame.KEYDOWN:

                    # Quitting the death screen by pressing "q"
                    if deathevent.key == pygame.K_q:
                        running_death = False
                        break

            # Counts 60 up per second
            death_count_time += 1

            # How long the game over message is on the screen
            if death_count_time > FPS * 10:  # 10 Seconds
                running_death = False
            else:
                continue

    # Calling the death function
    if skip_game_over_text:
        pass
    else:
        death()
