#1080 x 1920
#720 x 1280
#480 x 854
#360 x 640
#240 x 426
#120 x 213


import os
from moviepy.editor import VideoFileClip

def recortar_e_centralizar(nome_arquivo, nome_saida):
    # Carrega o vídeo original
    video = VideoFileClip(nome_arquivo)

    # Obtém as dimensões do Reels
    largura_reels = 1080
    altura_reels = 1920

    # Calcula as dimensões do vídeo ajustado ao Reels
    proporcao_reels = largura_reels / altura_reels
    proporcao_video = video.size[0] / video.size[1]

    if proporcao_video > proporcao_reels:
        # O vídeo é mais largo que o Reels, então ajustamos a largura
        nova_largura = proporcao_reels * video.size[1]
        video = video.crop(x1=(video.size[0] - nova_largura) // 2, x2=(video.size[0] + nova_largura) // 2)
    else:
        # O vídeo é mais alto que o Reels, então ajustamos a altura
        nova_altura = video.size[0] / proporcao_reels
        video = video.crop(y1=(video.size[1] - nova_altura) // 2, y2=(video.size[1] + nova_altura) // 2)

    # Redimensiona o vídeo para as dimensões do Reels
    video = video.resize((largura_reels, altura_reels))

    # Salva o vídeo recortado e centralizado no Reels com a mesma duração do vídeo original
    video.write_videofile(nome_saida, codec='libx264', audio_codec="aac")

# Obtém a lista de arquivos na pasta raiz
pasta_raiz = "./videos/"  # Caminho para a pasta raiz
pasta_destino = "./videos_recortados/"
if not os.path.exists(pasta_destino):
    # Criar a pasta
    os.makedirs(pasta_destino)
arquivos = os.listdir(pasta_raiz)

# Filtra os arquivos de vídeo
videos = [arquivo for arquivo in arquivos if arquivo.endswith((".mpeg", ".mp4", ".avi", ".mov"))]

# Recorta e salva cada vídeo com sufixo "_reels"
for video in videos:
    nome_arquivo = os.path.join(pasta_raiz, video)
    nome_saida = os.path.join(pasta_destino, video.split(".")[0] + "_recortado.mp4")
    recortar_e_centralizar(nome_arquivo, nome_saida)
