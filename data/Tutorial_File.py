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
from data.Resources_Loading_File import IMG_HEALING_POOL_25
from data.Resources_Loading_File import IMG_HEALING_POOL_50
from data.Resources_Loading_File import IMG_SHIELD_POWER_UP
from data.Resources_Loading_File import IMG_ARROW_LEFT
from data.Resources_Loading_File import IMG_ARROW_RIGHT
from data.Tutorial_Pause_Menu_File import pausemenu

# Initialize the font
pygame.font.init()
pygame.mixer.init()
pygame.init()

# Setting up variables that are used everywhere
score_value = 0
small_pool = 0
shield_counter = 0
mainexplosions = []
pools = []

current_width = 0  # Should be "None" but than the IDLE will show so many warnings ;-(
current_height = 0

# Variables for "saying hello"
move_left = 0
move_right = 0
move_up = 0
move_down = 0
shoot_bullets = 0
counter_saying_hello = 1
first_label = True
second_label = False
third_label = False
fourth_label = False
allow_shooting = False
fifth_label = False
plus_y = 0
sixth_label = False

# Getting the size values of the current window
def currents():
    global current_width
    global current_height

    # Checking the size of the window
    current_width, _ = pygame.display.get_surface().get_size()
    _, current_height = pygame.display.get_surface().get_size()


# Adding to score
def score_adding(amount):
    global small_pool
    global score_value
    global shield_counter

    score_value += amount
    small_pool += amount
    shield_counter += amount


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
                if player.shield > 9:
                    player.shield -= 10
                else:
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

    def __init__(self, x, y, health=100, shield=0):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(IMG_PLAYER_SHIP, (70, 70))
        self.laser_img = pygame.transform.scale(IMG_PLAYER_LASER, (70, 70))
        self.laser_img_height = 70
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.shield = shield
        self.max_shield = 100
        self.shield_counter = 0
        self.max_health = health
        self.allow_bars = False

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
                        score_adding(1)

    # Draws the player
    def draw(self, window):
        super().draw(window)
        if self.allow_bars:
            self.shieldbar(window)
            self.healthbar(window)
        self.adds_shield()
        self.checking_health()
        self.checking_shield()

    # Healthbar drawing
    def healthbar(self, window):
        if self.shield == 0:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))
        else:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 23, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 23, self.ship_img.get_width() * (self.health / self.max_health), 10))

    # Shieldbar drawing
    def shieldbar(self, window):
        if self.shield > 0:
            pygame.draw.rect(window, (0, 0, 100), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 0, 255), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.shield / self.max_shield), 10))

    # Checks that the health won't be more than a 100
    def checking_health(self):
        if self.health > self.max_health:
            self.health = self.max_health

    # Adds shield health over time
    def adds_shield(self):
        self.shield_counter += 1
        if self.shield_counter > 59 and self.shield < 100:
            self.shield += 1
            self.shield_counter = 0

    # Checks that the shield won't be more than a 100
    def checking_shield(self):
        if self.shield > self.max_shield:
            self.shield = self.max_shield


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


# Healing pool class
class Healing:
    def __init__(self, power):
        self.x = random.randrange(0, current_width - self.get_width())
        self.y = random.randrange(-100, 0 - (self.get_height()))

        self.power = power
        if self.power == 25:
            self.img = pygame.transform.scale(IMG_HEALING_POOL_25, (25, 25))
        elif self.power == 50:
            self.img = pygame.transform.scale(IMG_HEALING_POOL_50, (25, 25))

        self.mask = pygame.mask.from_surface(self.img)

    # Drawing function
    def draw(self, screen, velocity):
        screen.blit(self.img, (self.x, self.y))
        self.move(velocity)

    def move(self, velocity):
        self.y += velocity

    # Gets the width of the pool
    @staticmethod
    def get_width():
        return 25  # AttributeError: 'Healing' object has no attribute 'img'
        # return self.img.get_width()

    # Gets the height of the pool
    @staticmethod
    def get_height():
        return 25  # AttributeError: 'Healing' object has no attribute 'img'
        # return self.img.get_height()


# Shield power up class
class Shield:
    def __init__(self):
        self.x = random.randrange(0, current_width - self.get_width())
        self.y = random.randrange(-100, 0 - (self.get_height()))

        self.img = pygame.transform.scale(IMG_SHIELD_POWER_UP, (25, 25))
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen, velocity):
        screen.blit(self.img, (self.x, self.y))
        self.move(velocity)

    def move(self, velocity):
        self.y += velocity

    # Gets the width of the power up
    @staticmethod
    def get_width():
        return 25  # AttributeError: 'Shield' object has no attribute 'img'
        # return self.img.get_width()

    # Gets the height of the power up
    @staticmethod
    def get_height():
        return 25  # AttributeError: 'Shield' object has no attribute 'img'
        # return self.img.get_height()


# Detects if objects have been collided
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) is not None


# Game function
def tutorial():

    # Making variables global
    global score_value
    global small_pool
    global shield_counter
    global move_left
    global move_right
    global move_up
    global move_down
    global shoot_bullets
    global counter_saying_hello
    global first_label
    global second_label
    global third_label
    global allow_shooting
    global fourth_label
    global fifth_label
    global plus_y
    global sixth_label

    # Draws everything
    def draw_current_frame():

        # Shows the background
        if background_to_use == 1:
            tutscreen.blit(tutorial_beginning_background, (0, 0))
        elif background_to_use == 2:
            tutscreen.blit(tutorial_end_background, (0, 0))

        # Draws the enemies
        for enemy_drawing in enemies:
            enemy_drawing.draw(tutscreen)

        # Draws the explosion of an enemy
        for current_explosion in mainexplosions:
            if current_explosion.particles_in_game:
                current_explosion.draw(tutscreen)
            else:
                mainexplosions.remove(current_explosion)

        # Drawing healing pools
        for current_pool in pools:
            current_pool.draw(tutscreen, healing_velocity)

        # Drawing shield power up
        for current_shield in shields:
            current_shield.draw(tutscreen, shield_velocity)

        # Draws the player
        player.draw(tutscreen)

        # The tutorial is programmed under this comment

        # Start message
        saying_hello()

        # Refresh
        pygame.display.update()

    # Movement function
    def movement():

        # Making variables global
        global move_left
        global move_right
        global move_up
        global move_down
        global first_label
        global shoot_bullets
        global allow_shooting
        global third_label

        # Detects if a key is pressed
        keys = pygame.key.get_pressed()

        # Left
        if keys[pygame.K_a]:
            if player.x <= 0:
                player.x = 0
            else:
                player.x -= player_velocity
                if first_label:
                    move_left += 1

        if keys[pygame.K_LEFT]:
            if player.x <= 0:
                player.x = 0
            else:
                player.x -= player_velocity
                if first_label:
                    move_left += 1

        # Right
        if keys[pygame.K_d]:
            if player.x >= current_width - player.get_width():
                player.x = current_width - player.get_width()
            else:
                player.x += player_velocity
                if first_label:
                    move_right += 1

        if keys[pygame.K_RIGHT]:
            if player.x >= current_width - player.get_width():
                player.x = current_width - player.get_width()
            else:
                player.x += player_velocity
                if first_label:
                    move_right += 1

        # Up
        if keys[pygame.K_w]:
            if player.y <= 0:
                player.y = 0
            else:
                player.y -= player_velocity
                if first_label:
                    move_up += 1

        if keys[pygame.K_UP]:
            if player.y <= 0:
                player.y = 0
            else:
                player.y -= player_velocity
                if first_label:
                    move_up += 1

        # Down
        if keys[pygame.K_s]:
            if player.y >= current_height - player.get_height():
                player.y = current_height - player.get_height()
            else:
                player.y += player_velocity
                if first_label:
                    move_down += 1

        if keys[pygame.K_DOWN]:
            if player.y >= current_height - player.get_height():
                player.y = current_height - player.get_height()
            else:
                player.y += player_velocity
                if first_label:
                    move_down += 1

        # Player Shooting
        if allow_shooting:
            if keys[pygame.K_SPACE]:
                player.shoot()
                if third_label:
                    shoot_bullets += 10

    # Gets one third of the screen
    def one_third_of_screen():
        return (current_height / 3) * 2

    # Start of the tutorial
    def saying_hello():

        # Making global
        global counter_saying_hello
        global first_label
        global second_label
        global third_label
        global move_right
        global move_up
        global move_down
        global move_left
        global allow_shooting
        global shoot_bullets
        global fourth_label
        global fifth_label
        global plus_y
        global sixth_label

        # Prints the first labels
        if counter_saying_hello < FPS * 6 and counter_saying_hello != 0 and first_label:

            # Drawing labels and an arrow
            tutscreen.blit(saying_hello_urship_label, (player.x + 100, player.y - 45))
            tutscreen.blit(saying_hello_wasd_label, (player.x + 100, player.y - 20))
            IMG_ARROW_LEFT_SCALED = pygame.transform.scale(IMG_ARROW_LEFT, (70, 70))
            tutscreen.blit(IMG_ARROW_LEFT_SCALED, (player.x + 75, player.y))
            counter_saying_hello += 1

        # Detects the movement
        if move_up > 15 and move_down > 15 and move_left > 15 and move_right > 15:
            if first_label:
                counter_saying_hello = 0
            first_label = False
            counter_saying_hello += 1
            if counter_saying_hello > FPS * 1:
                second_label = True
                move_up = 0
                move_down = 0
                move_left = 0
                move_right = 0
                counter_saying_hello = 0

        # Say "Great" for 2 sec. and than calls immediately the third label
        if second_label:
            tutscreen.blit(saying_hello_good_job_label, (player.x + 100, player.y - 20))
            counter_saying_hello += 1
            if counter_saying_hello > FPS * 2:
                second_label = False
                third_label = True
                counter_saying_hello = 0

        # Says for 3 seconds that you have to shoot
        if third_label and counter_saying_hello < FPS * 3:
            tutscreen.blit(saying_hello_shooting_label, (player.x + 100, player.y - 45))
            tutscreen.blit(saying_hello_try_it_label, (player.x + 100, player.y - 20))
            allow_shooting = True
            counter_saying_hello += 1

        # Detects if you shoot
        if shoot_bullets > 1:
            if third_label:
                counter_saying_hello = 0
            third_label = False
            counter_saying_hello += 1
            if counter_saying_hello > FPS * 1:
                fourth_label = True
                shoot_bullets = 0
                counter_saying_hello = 0

        # Displaying "Great" for 2 seconds
        if fourth_label:
            counter_saying_hello += 1
            player.allow_bars = True
            player.shield = 0
            tutscreen.blit(saying_hello_very_good_job_label, (player.x + 100, player.y - 20))
            if counter_saying_hello > FPS * 2:
                fourth_label = False
                fifth_label = True
                counter_saying_hello = 0

        # Explains the health and shieldbar
        if fifth_label:
            counter_saying_hello += 1
            if counter_saying_hello == 1:
                player.shield = 0
            if counter_saying_hello < FPS * 2:
                player.shield = 0

            # Explains the healthbar
            if player.shield == 0:
                tutscreen.blit(saying_hello_health_second_label, (player.x - saying_hello_health_second_label.get_width() - 30, player.y + 10))
                tutscreen.blit(saying_hello_health_first_label, (player.x - saying_hello_health_second_label.get_width() - saying_hello_health_first_label.get_width() - 30, player.y + 10))
                IMG_ARROW_RIGHT_SCALED = pygame.transform.scale(IMG_ARROW_RIGHT, (70, 70))
                tutscreen.blit(IMG_ARROW_RIGHT_SCALED, (player.x - IMG_ARROW_RIGHT_SCALED.get_width() - 20, player.y + IMG_ARROW_RIGHT_SCALED.get_height() - 20))

            # Moves the health explanation down if the shield bar occurs
            else:

                # Makes a fancy animation
                if plus_y < 16:
                    plus_y += 0.25

                tutscreen.blit(saying_hello_health_second_label, (player.x - saying_hello_health_second_label.get_width() - 30, player.y + 10 + plus_y - 5))
                tutscreen.blit(saying_hello_health_first_label, (player.x - saying_hello_health_second_label.get_width() - saying_hello_health_first_label.get_width() - 30, player.y + 10 + plus_y - 5))
                IMG_ARROW_RIGHT_SCALED = pygame.transform.scale(IMG_ARROW_RIGHT, (70, 70))
                tutscreen.blit(IMG_ARROW_RIGHT_SCALED, (player.x - IMG_ARROW_RIGHT_SCALED.get_width() - 20, player.y + IMG_ARROW_RIGHT_SCALED.get_height() - 20 + plus_y))
                if plus_y < 1:
                    counter_saying_hello = FPS * 3

            # Explains the shield bar
            if player.shield > 0:
                tutscreen.blit(saying_hello_shield_first_label, (player.x + 100, player.y))
                tutscreen.blit(saying_hello_shield_second_label, (player.x + 100 + saying_hello_shield_first_label.get_width(), player.y))
                tutscreen.blit(saying_hello_shield_third_label, (player.x + 100, player.y + 20))
                IMG_ARROW_LEFT_SCALED = pygame.transform.scale(IMG_ARROW_LEFT, (70, 70))
                tutscreen.blit(IMG_ARROW_LEFT_SCALED, (player.x + 75, player.y + 50))
                if counter_saying_hello > FPS * 10:
                    counter_saying_hello = 0
                    fifth_label = False
                    sixth_label = True
            # TODO: Continue the Tutorial...
            # Moves the player under the line
            if sixth_label:
                if player.y < 0:
                    pass
                else:
                    pass

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
        tutscreen = pygame.display.set_mode((monitor_sizeX, monitor_sizeY), pygame.FULLSCREEN)
    else:
        tutscreen = pygame.display.set_mode((current_width, current_height))

    # Making the backgrounds that are used the right size
    tutorial_beginning_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Standard.png")), (current_width, current_height))
    tutorial_end_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Game.png")), (current_width, current_height))
    tutorial_gameover_background = pygame.transform.scale(pygame.image.load(os.path.join("resources/backgrounds", "Game_Over.png")), (current_width, current_height))

    # Creating fonts
    standard_font = pygame.font.SysFont("freesansbold.ttf", 64)
    saying_hello_urship_font = pygame.font.SysFont("unispacebold", 16)

    # Colors
    WHITE = pygame.Color("white")
    GREEN = pygame.Color("green")
    BLUE = pygame.Color("blue")

    # Creating labels
    saying_hello_urship_label = saying_hello_urship_font.render("This is your ship", True, WHITE)
    saying_hello_wasd_label = saying_hello_urship_font.render("Use W, A, S, D to move it", True, WHITE)
    # TODO: Hint to move faster
    saying_hello_good_job_label = saying_hello_urship_font.render("Great!!", True, WHITE)
    saying_hello_shooting_label = saying_hello_urship_font.render("You can shoot with SPACE", True, WHITE)
    saying_hello_try_it_label = saying_hello_urship_font.render("Try it!", True, WHITE)
    saying_hello_very_good_job_label = saying_hello_urship_font.render("Fantastic", True, WHITE)
    saying_hello_health_first_label = saying_hello_urship_font.render("This is your ", True, WHITE)
    saying_hello_health_second_label = saying_hello_urship_font.render("healthbar", True, GREEN)
    saying_hello_shield_first_label = saying_hello_urship_font.render("This is your ", True, WHITE)
    saying_hello_shield_second_label = saying_hello_urship_font.render("shieldbar", True, BLUE)
    saying_hello_shield_third_label = saying_hello_urship_font.render("It will regenerate over time", True, WHITE)

    # Defines how many enemies are spawned in at the beginning of the tutorial
    enemies_in_tutorial = 0

    # (Re)sets everything to default value
    FPS = 60
    running_tutorial = True
    lives = 1
    enemies = []
    skip_tut_game_over_text = False
    enemy_velocity = 1
    player_velocity = 5
    healing_velocity = 0.5
    shields = []
    shield_velocity = 0.5
    laser_velocity = 5
    background_to_use = 1
    if score_value != 0:
        score_value = 0
    move_left = 0
    move_right = 0
    move_up = 0
    move_down = 0
    shoot_bullets = 0
    counter_saying_hello = 1
    first_label = True
    second_label = False
    third_label = False
    allow_shooting = False
    fourth_label = False
    fifth_label = False
    plus_y = 0
    sixth_label = False

    # Part of the tutorial running
    saying_hello_running = True

    # Creating the player
    player = Player(current_width / 2 - (IMG_PLAYER_SHIP.get_width() / 2), current_height - 100)
    player.x = (current_width / 2) - (player.ship_img.get_width() / 2)
    player.y = (current_height / 2) - (player.ship_img.get_width() / 2)

    # Clock
    clock = pygame.time.Clock()

    # Initialize the mixer
    pygame.mixer.init()

    # Tutorial loop
    while running_tutorial:

        # Has the purpose that the computer goes through this loop in the exact time
        clock.tick(FPS)

        # Making some background music
        play_random_songs()

        # Draws each frame
        draw_current_frame()

        # Checking events
        for event in pygame.event.get():

            # Quitting the game by closing the window
            if event.type == pygame.QUIT:
                running_tutorial = False
                pygame.mixer.quit()
                pygame.quit()
                quit()
                break

            # Checks if a key is pressed
            if event.type == pygame.KEYDOWN:

                # Quitting game by pressing "q"
                if event.key == pygame.K_q:
                    running_tutorial = False
                    skip_tut_game_over_text = True
                    pygame.mixer.quit()
                    break

                # Entering pause menu by pressing "ESCAPE"
                if event.key == pygame.K_ESCAPE:

                    # Pauses music
                    pygame.mixer_music.pause()

                    # Calling pausemenu
                    pausemenu()

                    # Lets python continue the music
                    pygame.mixer_music.unpause()

        # Lets you move
        movement()

        # Moves the enemies and lasers
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

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

        # Removes healing pool when it has been collided with the player
        for pool in pools:
            if collide(pool, player):
                pools.remove(pool)
                player.health += pool.power
                player.checking_health()

            # Removes a healing pool when it has crossed the bottom of the screen
            if pool.y > current_height:
                pools.remove(pool)

        # Removes shield power up when it has been collided with the player
        for shield in shields:
            if collide(shield, player):
                shields.remove(shield)
                player.shield += 10
                player.checking_shield()

            if shield.y > current_height:
                shields.remove(shield)

        # Moves the lasers of the player and detects if they have been collided with an other object
        player.move_lasers(-laser_velocity, enemies)









    # Game over function
    def death():
        pass
        # TODO: If you fail the tutorial
        # Should be a restart button and maybe an explanation why you failed

    # Calling the death function
    if skip_tut_game_over_text:
        pass
    else:
        death()
