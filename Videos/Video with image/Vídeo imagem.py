import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import os
from gtts import gTTS
from moviepy.editor import *
import random
import shutil
import datetime

# 1080 x 1920
# 720 x 1280
# 480 x 854
# 360 x 640
# 240 x 426
# 120 x 213

width = 480
height = 854

img_str = "image-"
img_count = 0

texto = ""
with open('inicio.txt', encoding='utf-8') as file:
    texto = texto + file.read() + '.\n\n'
with open('texto.txt', encoding='utf-8') as file:
    texto = texto + file.read() + '.\n\n'
with open('final.txt', encoding='utf-8') as file:
    texto = texto + file.read()

print(texto)

tts = gTTS(text=texto, lang='pt-br', slow=False)
tts.save('temp.mp3')

print('Áudio criado')

imagens = [os.path.join("./", "logo.png")]

audio_clip = AudioFileClip('temp.mp3')
audio_duration = audio_clip.duration

clips_imagem = [ImageClip(imagem).set_duration(audio_duration) for imagem in imagens]
video_imagem = concatenate_videoclips(clips_imagem)
video_imagem = video_imagem.resize((width, height))
video_final = video_imagem.set_audio(audio_clip)

print('Salvando vídeo')

if not os.path.exists('./'):
    os.mkdir('./')
video_final.write_videofile('./video.avi', fps=24, codec='libx264')

video = VideoFileClip('./video.avi')
accelerated_video = video.fx(vfx.speedx, factor=1.1)

now = datetime.datetime.now()
hour_formatted = now.strftime("%Y-%m-%d-%H-%M")

#acelera o vídeo pra melhorar a voz do google
accelerated_video.write_videofile(str(hour_formatted) + ".mp4")

if os.path.exists('./temp.mp3'):
    os.remove('./temp.mp3')
if os.path.exists('./video.avi'):
    os.remove('./video.avi')

print('Vídeo gerado com sucesso!')
print('Finalizado')
