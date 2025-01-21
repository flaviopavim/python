from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import os
import random

directory = "./"

# Loop through the files in the directory
for file in os.listdir(directory):
    if file.endswith(".txt"):  # Check if the file has a .txt extension
        file_name, extension = os.path.splitext(file)  # Split the file name and its extension
        
        # Open and read the content of the .txt file
        with open(os.path.join(directory, file), "r") as f:
            content = f.read()
            print(file_name)
            
            # Read the text file content with UTF-8 encoding
            with open(directory + file_name + ".txt", encoding='utf-8') as text_file:
                text = text_file.read()
            
            # Generate audio from the text
            print('Saving audio')
            tts = gTTS(text=text, lang='pt-br', slow=False)
            tts.save(file_name + '.mp3')  # Save the audio as an MP3 file
            print('Audio saved')
