import os
from gtts import gTTS
from moviepy.editor import *

texto=""

# Ler o conteúdo do arquivo de texto
with open("inicio.txt", "r", encoding="utf-8") as file:
    texto = texto+file.read()+".\n\n"
with open("texto.txt", "r", encoding="utf-8") as file:
    texto = texto+file.read()+".\n\n"
with open("final.txt", "r", encoding="utf-8") as file:
    texto = texto+file.read()


# Configurar as opções do gTTS
tts = gTTS(text=texto, lang="pt-br", slow=False)

# Salvar o áudio em um arquivo temporário
temp_audio_file = "temp_audio.mp3"
tts.save(temp_audio_file)

# Obter a duração do áudio em segundos
audio_clip = AudioFileClip(temp_audio_file)
audio_duration = audio_clip.duration

# Criar um vídeo preto com a duração do áudio
video = ColorClip((1280, 720), color=(0, 0, 0), duration=audio_duration)
video_with_audio = video.set_audio(audio_clip)

# Acelerar o vídeo
video_accelerated = video_with_audio.fx(vfx.speedx, factor=1.1)

# Salvar o áudio acelerado em formato MP3
output_file = "audio.mp3"
video_accelerated.audio.write_audiofile(output_file, codec="mp3")

# Remover o arquivo temporário de áudio
os.remove(temp_audio_file)

print("Áudio acelerado salvo em formato MP3 com sucesso!")
