from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

# Pasta contendo os vídeos
folder_path = "./videos"

# Caminho de saída do vídeo combinado
output_path = "video.mp4"

video_clips = []

# Percorre todos os arquivos na pasta
for filename in os.listdir(folder_path):
    # Verifica se é um arquivo de vídeo com as extensões desejadas
    if filename.endswith((".mpeg", ".mp4", ".avi", ".mov")):
        # Caminho completo do arquivo
        filepath = os.path.join(folder_path, filename)
        # Carrega o vídeo como um objeto VideoFileClip
        clip = VideoFileClip(filepath)
        # Adiciona o objeto VideoFileClip à lista de clipes de vídeo
        video_clips.append(clip)

# Combina os clipes de vídeo em um único vídeo
final_clip = concatenate_videoclips(video_clips)

# Salva o vídeo combinado no caminho de saída, usando o codec "libx264"
final_clip.write_videofile(output_path, codec="libx264")
