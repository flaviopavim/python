import os
import librosa
import soundfile as sf
import pygame
import re
from gtts import gTTS
import time
from datetime import datetime


def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)[:20]  # Limita o tamanho do nome

def voice(texto):
    # Gerar um nome de arquivo seguro
    safe_filename = sanitize_filename(texto)
    output_file = f"{safe_filename}.mp3"
    temp_audio_file = "temp_audio.mp3"

    # Gerar o áudio com gTTS
    tts = gTTS(text=texto, lang="pt-br", slow=False)
    tts.save(temp_audio_file)

    # Carregar o áudio
    y, sr = librosa.load(temp_audio_file, sr=None)

    # 1. Acelerar o áudio em 1.8x (diminui a duração)
    y_fast = librosa.effects.time_stretch(y, rate=1.8)

    # 2. Ajustar o pitch para 1.1x com um pequeno ajuste para evitar distorções
    y_pitched = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=0.2)

    # Salvar o áudio processado
    sf.write(output_file, y_pitched, sr, format='MP3')

    # Remover o arquivo temporário
    os.remove(temp_audio_file)

    # Inicializar o pygame e tocar o áudio
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Aguardar a reprodução
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print(f"Áudio '{output_file}' reproduzido com sucesso!")



# Lista de alarmes no formato [("HH:MM:SS", "Mensagem do Alarme")]
alarmes = [
    ("14:30:00", "Teste de um alarme"),
    ("15:30:00", "Reunião importante!"),
    ("18:00:00", "Hora de encerrar o trabalho!"),
]

while True:
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"{agora}")
    
    # Verificar se há algum alarme para o horário atual
    for horario, mensagem in alarmes:
        if agora == horario:
            print(f"🔔 Alarme: {mensagem}")
            voice(f"{mensagem}")
    
    time.sleep(1)
