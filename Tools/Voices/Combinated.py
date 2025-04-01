import os
import numpy as np
import librosa
import soundfile as sf
from gtts import gTTS

texto = "Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?"

# Gerar o áudio com gTTS
temp_audio_file = "temp_audio.mp3"
tts = gTTS(text=texto, lang="pt-br", slow=False)
tts.save(temp_audio_file)

# Carregar o áudio original
y, sr = librosa.load(temp_audio_file, sr=None)

# Acelerar o áudio em 1.5x (diminui a duração)
y_fast = librosa.effects.time_stretch(y, rate=1.3)

# Criar a versão com pitch grave (n_steps negativo)
y_grave = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=-4)  # Pitch grave

# Criar a versão com pitch agudo (n_steps positivo)
y_agudo = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=1.1)  # Pitch agudo

# Ajustar o comprimento para que ambas as versões tenham o mesmo tamanho (se necessário)
# Caso as durações sejam diferentes, cortamos ou preenchemos com zeros para que fiquem iguais
min_length = min(len(y_grave), len(y_agudo))
y_grave = y_grave[:min_length]
y_agudo = y_agudo[:min_length]

# Combinar as duas versões: grave + agudo
combined_audio = y_grave + y_agudo  # Juntando as duas faixas

# Salvar o áudio combinado
output_file = "combinated.mp3"
sf.write(output_file, combined_audio, sr, format='MP3')

# Remover o arquivo temporário
os.remove(temp_audio_file)

print("Áudio combinado (grave e agudo) salvo em:", output_file)
