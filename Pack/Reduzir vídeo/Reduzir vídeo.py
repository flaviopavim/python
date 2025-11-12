from moviepy.editor import *

# Carrega o vídeo
video = VideoFileClip("video.mp4")

# Define a nova resolução (diminui a qualidade)
new_resolution = (320, 180)

# Redimensiona o vídeo
resized_video = video.resize(new_resolution)

# Define o bitrate para 500kbps
bitrate = "500k"

# Salva o vídeo com a nova resolução e o bitrate
resized_video.write_videofile("video_reduzido.mp4", bitrate=bitrate)
