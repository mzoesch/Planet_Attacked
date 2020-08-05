import random
import pygame
from data.Resources_Loading_File import SONG_ONE
from data.Resources_Loading_File import SONG_TWO

# Random background music
# Music lives forever

next_song = None
stop_music = False

# All the songs that can be played
background_songs = [
        SONG_ONE,
        SONG_TWO
    ]


# The actual function that plays the music
def play_random_songs():

    global next_song

    if pygame.mixer.music.get_busy():
        pass

    else:

        next_song = random.choice(background_songs)  # Chooses a random song

        pygame.mixer.music.load(next_song)

        pygame.mixer.music.play()
