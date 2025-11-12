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

video_width = 854
video_height = 480
image_width = 854
image_height = 480

# Cria uma nova pasta para as imagens redimensionadas
resized_folder_path = "./resized_images/"
if not os.path.exists(resized_folder_path):
    os.makedirs(resized_folder_path)

# Itera sobre cada imagem na pasta original
folder_path = "./imagens/"
image_extensions = (".jpg", ".jpeg", ".png", ".gif")
for filename in os.listdir(folder_path):
    if filename.endswith(image_extensions):
        # Carrega a imagem original
        img_path = os.path.join(folder_path, filename)
        with Image.open(img_path) as img:
            # Redimensiona a imagem mantendo a proporção
            img_resized = img.resize((image_width, image_height))
            # Centraliza a imagem no tamanho do vídeo
            background = Image.new('RGB', (video_width, video_height), (0, 0, 0))
            offset = ((video_width - image_width) // 2, (video_height - image_height) // 2)
            background.paste(img_resized, offset)
            # Salva a imagem redimensionada e centralizada na nova pasta
            resized_img_path = os.path.join(resized_folder_path, filename)
            background.save(resized_img_path)

# Gera a lista de caminhos das imagens redimensionadas
imagens = [os.path.join(resized_folder_path, filename) for filename in os.listdir(resized_folder_path)]

# Em seguida, o restante do código permanece o mesmo...
texto = ""
with open('inicio.txt', encoding='utf-8') as file:
    texto = texto + file.read() + ".\n\n"
with open('texto.txt', encoding='utf-8') as file:
    texto = texto + file.read() + ".\n\n"
with open('final.txt', encoding='utf-8') as file:
    texto = texto + file.read()

print(texto)

tts = gTTS(text=texto, lang='pt-br', slow=False)
tts.save('temp.mp3')

print('Áudio criado')

clips_imagem = [ImageClip(imagem).set_duration(5) for imagem in imagens]
video_imagem = concatenate_videoclips(clips_imagem)
audio = AudioFileClip('temp.mp3')
video_imagem = video_imagem.set_duration(audio.duration).resize((video_width, video_height))
audio = audio.set_duration(audio.duration)
video_final = video_imagem.set_audio(audio)

print('Salvando vídeo')

if not os.path.exists('./'):
    os.mkdir('./')
video_final.write_videofile('./video.mp4', fps=24, codec='libx264')

video = VideoFileClip('./video.mp4')
accelerated_video = video.fx(vfx.speedx, factor=1.1)

now = datetime.datetime.now()
hour_formatted = now.strftime("%Y-%m-%d-%H-%M")

accelerated_video.write_videofile(str(hour_formatted) + ".mp4")

if os.path.exists('temp.mp3'):
    os.remove('temp.mp3')
if os.path.exists('./video.mp4'):
    os.remove('./video.mp4')
if os.path.exists(resized_folder_path):
    shutil.rmtree(resized_folder_path)

print('Vídeo gerado com sucesso!')
print('Finalizado')
