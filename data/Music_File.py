import random
import pygame

# Random Music
# Music lives forever

next_song = None
stop_music = False

# All the songs that can be played

background_songs = [
        "resources/sounds/Background-Space_Invaders(2).wav",
        "resources/sounds/Background-Space_Invaders(1).wav"
    ]


def play_random_songs():

    global next_song

    if pygame.mixer.music.get_busy():
        pass

    else:

        next_song = random.choice(background_songs)  # Chooses a random song

        pygame.mixer.music.load(next_song)

        pygame.mixer.music.play()

