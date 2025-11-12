from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import glob
from datetime import date, timedelta
import random

folder_path = "./"
output_folder = "./"

# Verifica se a pasta de saída existe, se não, cria-a
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Obter a data atual
today = date.today()
output_filename = today.strftime("%Y-%m-%d") + "_time.mp4"
output_path = os.path.join(output_folder, output_filename)

video_clips = []
total_duration = timedelta()  # Duração total dos clipes

print("Buscando vídeos...")

# Percorre todas as pastas no diretório especificado
for folder_name in os.listdir(folder_path):
    folder_full_path = os.path.join(folder_path, folder_name)
    
    # Verifica se o item na pasta é uma pasta e não um arquivo
    if os.path.isdir(folder_full_path):

        print("Percorrendo a pasta: " + folder_full_path)
        
        # Percorre todos os arquivos de vídeo na pasta
        video_files = glob.glob(os.path.join(folder_full_path, "*.mpeg"))
        
        for video_file in video_files:
            print("Lendo o vídeo: " + video_file)
            clip = VideoFileClip(video_file)
            video_clips.append(clip)

# Embaralha a ordem dos vídeos
random.shuffle(video_clips)

# Seleciona clipes de vídeo até que a duração total exceda 30 segundos
for clip in video_clips:
    clip_duration = clip.duration  # Duração do clipe em segundos
    if total_duration + timedelta(seconds=int(clip_duration)) < timedelta(seconds=30):
        total_duration += timedelta(seconds=int(clip_duration))
    else:
        break  # Sai do loop quando a duração total exceder 30 segundos

# Combina os clipes de vídeo em um único vídeo
final_clip = concatenate_videoclips(video_clips[:30])

# Define a duração exata do vídeo final como 60 segundos
final_clip = final_clip.subclip(0, 60)

# Salva o vídeo combinado no caminho de saída
final_clip.write_videofile(output_path, codec="libx264")
