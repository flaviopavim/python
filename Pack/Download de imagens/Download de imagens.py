import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import os
from gtts import gTTS
from moviepy.editor import *
import random
import shutil
from urllib.parse import urlencode
from http import client
import urllib.request
import urllib
import urllib.parse

# Função para obter o conteúdo HTML de uma URL
def getHtml(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"})).read().decode("utf8")
    except:
        return ""

# Define as dimensões desejadas para o vídeo
width = 640
height = 360

# Define o termo de busca para as imagens
imagem = "hacker"

# Gera a URL de busca no Freepik
url = "https://br.freepik.com/search?format=search&query=" + urllib.parse.quote(imagem + " jpg")
response = getHtml(url)
soup = BeautifulSoup(response, 'html.parser')
image_tags = soup.find_all('img')

# Cria a pasta "video" se ela não existir
if not os.path.exists("video"):
    os.makedirs("video")

# Configuração das variáveis para o nome das imagens
img_str = "image-"
img_count = 0

# Percorre todas as imagens encontradas
for img in image_tags:
    if 'width' in img.attrs and 'height' in img.attrs:
        img_width = int(img.attrs['width'])
        img_height = int(img.attrs['height'])
        if img_width > 400 and img_height > 300:
            if img_width / img_height > 1:
                img_count = img_count + 1
                try:
                    if img['src'].endswith((".jpg", ".jpeg", ".png")):
                        # Faz o download da imagem
                        response = requests.get(img['src'])
                        img = Image.open(BytesIO(response.content))

                        # Salva a imagem no disco com a extensão apropriada
                        extension = ".jpg"
                        if img.format == "JPEG":
                            extension = ".jpeg"
                        elif img.format == "PNG":
                            extension = ".png"
                        img_path = os.path.join("video", img_str + str(img_count) + extension)
                        img.save(img_path)
                        print(img_path)
                except Exception as e:
                    print(f"Error: {e}")

folder_path = "./video/"

texto = ""
with open('inicio.txt', encoding='utf-8') as file:
    texto = texto+file.read()+".\n\n"
with open('texto.txt', encoding='utf-8') as file:
    texto = texto+file.read()+".\n\n"
with open('final.txt', encoding='utf-8') as file:
    texto = texto+file.read()
print(texto)

# Converte o texto em áudio usando a biblioteca gTTS
tts = gTTS(text=texto, lang='pt-br', slow=False)
tts.save('./video/audio.mp3')
print('Áudio criado')

image_extensions = (".jpg", ".jpeg", ".png", ".gif")
imagens = []

# Redimensiona as imagens para as dimensões desejadas
for filename in os.listdir(folder_path):
    if filename.endswith(image_extensions):
        with Image.open(os.path.join(folder_path, filename)) as img:
            img_resized = img.resize((width, height))
            img_resized.save(os.path.join(folder_path, filename))
        imagens.append(folder_path + filename)
random.shuffle(imagens)
clips_imagem = [ImageClip(imagem).set_duration(5) for imagem in imagens]
video_imagem = concatenate_videoclips(clips_imagem)
audio = AudioFileClip('./video/audio.mp3')
video_imagem = video_imagem.set_duration(audio.duration).resize((width, height))
audio = audio.set_duration(audio.duration)
video_final = video_imagem.set_audio(audio)
print('Salvando vídeo')

# Define o nome e o caminho do arquivo de vídeo final
video_output_path = './video.mp4'

# Define o nome e o caminho do arquivo de introdução (se necessário)
intro_path = './intro.mp4'

# Carrega o vídeo de introdução (se existir)
intro = VideoFileClip(intro_path).resize((width, height)) if os.path.exists(intro_path) else None

# Acelera o vídeo com o áudio gerado
accelerated_video = video_final.fx(vfx.speedx, factor=1.1)

# Concatena a introdução com o vídeo acelerado
intro_video = concatenate_videoclips([intro, accelerated_video]) if intro else accelerated_video
intro_video.write_videofile(video_output_path)

# Concatena o vídeo com a introdução
final_clip = concatenate_videoclips([intro_video, intro]) if intro else accelerated_video
final_clip.write_videofile(video_output_path)

# Remove a pasta com as imagens e o áudio
shutil.rmtree('./video')

print('Vídeo gerado com sucesso!')
print('Finalizado')
