import os
from gtts import gTTS
from moviepy.editor import *

texto = ""

# Read the content of the text file
with open("text.txt", "r", encoding="utf-8") as file:
    texto = texto + file.read()

# Configure gTTS options
tts = gTTS(text=texto, lang="pt-br", slow=False)

# Save the audio to a temporary file
temp_audio_file = "temp_audio.mp3"
tts.save(temp_audio_file)

# Get the duration of the audio in seconds
audio_clip = AudioFileClip(temp_audio_file)
audio_duration = audio_clip.duration

# Create a black video with the same duration as the audio
video = ColorClip((1280, 720), color=(0, 0, 0), duration=audio_duration)
video_with_audio = video.set_audio(audio_clip)

# Speed up the video
video_accelerated = video_with_audio.fx(vfx.speedx, factor=1.1)

# Save the accelerated audio in MP3 format
output_file = "audio.mp3"
video_accelerated.audio.write_audiofile(output_file, codec="mp3")

# Remove the temporary audio file
os.remove(temp_audio_file)

print("Accelerated audio successfully saved in MP3 format!")
