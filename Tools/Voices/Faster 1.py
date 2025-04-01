import os
import librosa
import soundfile as sf
from gtts import gTTS

texto="Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?"

# Gerar o áudio com gTTS
temp_audio_file = "temp_audio.mp3"
tts = gTTS(text=texto, lang="pt-br", slow=False)
tts.save(temp_audio_file)

# Carregar o áudio
y, sr = librosa.load(temp_audio_file, sr=None)

# 1. Acelerar o áudio em 1.8x (diminui a duração)
y_fast = librosa.effects.time_stretch(y, rate=1.8)

# 2. Ajustar o pitch para 1.1x com um pequeno ajuste para evitar distorções
y_pitched = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=0.2)

# Salvar o áudio processado
output_file = "faster1.mp3"
sf.write(output_file, y_pitched, sr, format='MP3')

# Remover o arquivo temporário
os.remove(temp_audio_file)

print("Audio successfully saved in MP3 format!")
