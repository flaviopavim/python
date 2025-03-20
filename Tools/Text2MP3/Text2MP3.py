import os
from gtts import gTTS
from moviepy.editor import *

# Pygame setup to avoid showing the support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

def talk(text,file):
    """
    This function converts the given text to speech using the gTTS library.
    It generates a temporary audio file and plays it using Pygame.
    """

    # Configure gTTS options to convert the given text to speech in Brazilian Portuguese
    tts = gTTS(text=text, lang="pt-br", slow=False)
    tts.save(file)

    # Load and play the final output audio using Pygame
    mixer.music.load(file)
    mixer.music.play()

# Example usage
talk("Hoje sou eu que vou apresentar essa bagaça","voice.mp3")
