import os
from gtts import gTTS
from moviepy.editor import *
import time

# Pygame setup to avoid showing the support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

def talk(texto):
    """
    This function converts the given text to speech using the gTTS library.
    It generates a temporary audio file and creates a black video with the 
    same duration as the audio. Then, it accelerates the video and saves the
    audio in a final output file that is played using Pygame.
    """

    # Configure gTTS options to convert the given text to speech in Brazilian Portuguese
    tts = gTTS(text=texto, lang="pt-br", slow=False)

    # Save the speech to a temporary audio file
    temp_audio_file = "talk.mp3"
    tts.save(temp_audio_file)

    # Load the audio file to get its duration
    audio_clip = AudioFileClip(temp_audio_file)
    audio_duration = audio_clip.duration  # Duration of the audio in seconds

    # Create a black video with the same duration as the audio
    video = ColorClip((1280, 720), color=(0, 0, 0), duration=audio_duration)
    video_with_audio = video.set_audio(audio_clip)

    # Accelerate the video slightly
    video_accelerated = video_with_audio.fx(vfx.speedx, factor=1.1)

    # Save the accelerated video audio as an MP3 file
    output_file = "talk.mp3"
    video_accelerated.audio.write_audiofile(output_file, codec="mp3")

    # Load and play the final output audio using Pygame
    mixer.music.load(output_file)
    mixer.music.play()

# Example usage
talk("Hoje sou eu que vou apresentar essa bagaça")
