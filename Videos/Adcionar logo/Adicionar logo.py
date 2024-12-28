import pycuda.autoinit

import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def adicionar_logo_videos_na_pasta(pasta_raiz, logo_path):
    # Obtém a lista de arquivos na pasta raiz
    arquivos = os.listdir(pasta_raiz)

    # Filtra os arquivos de vídeo
    videos = [arquivo for arquivo in arquivos if arquivo.endswith((".mpeg", ".mp4", ".avi", ".mov"))]

    # Para cada vídeo, adiciona o logo e salva com o mesmo nome do vídeo, mas com o sufixo "_logo"
    for video in videos:
        nome_arquivo = os.path.join(pasta_raiz, video)
        nome_saida = os.path.join(pasta_raiz, video.split(".")[0] + "_logo.mp4")
        adicionar_logo_video(nome_arquivo, logo_path, nome_saida)

def adicionar_logo_video(video_path, logo_path, output_path):
    # Carrega o vídeo original
    video = VideoFileClip(video_path)

    # Carrega a imagem do logo em formato PNG com transparência
    logo = ImageClip(logo_path).set_duration(video.duration)

    # Define a posição do logo 10 pixels do top e 10 pixels da direita
    logo = logo.set_position(lambda t: (video.size[0] - logo.size[0] - 10, 10))
    # Define a posição do logo 10 pixels do bottom e 10 pixels da direita
    #logo = logo.set_position(lambda t: (video.size[0] - logo.size[0] - 10, video.size[1] - logo.size[1] - 10))


    # Componha o vídeo original com o logo
    video_com_logo = CompositeVideoClip([video, logo])

    # Salva o vídeo resultante
    video_com_logo.write_videofile(output_path, codec='libx264', audio_codec="aac")

# Exemplo de uso
pasta_raiz = "./"
logo_path = "./logo.png"

adicionar_logo_videos_na_pasta(pasta_raiz, logo_path)
