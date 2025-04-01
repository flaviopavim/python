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
y_fast = librosa.effects.time_stretch(y, rate=1.5)

# Criar a versão com pitch grave (n_steps negativo)
y_grave1 = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=-8)  # Pitch grave

# Criar uma segunda versão com pitch grave (n_steps ainda mais negativo)
y_grave2 = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=-5)  # Pitch grave

# Criar a versão com pitch agudo (n_steps positivo)
y_agudo = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=5)  # Pitch agudo

# Ajustar o comprimento para que todas as versões tenham o mesmo tamanho
max_length = max(len(y_grave1), len(y_grave2), len(y_agudo))

# Preencher com zeros para garantir que todas as versões tenham o mesmo comprimento
y_grave1 = np.pad(y_grave1, (0, max_length - len(y_grave1)), mode='constant')
y_grave2 = np.pad(y_grave2, (0, max_length - len(y_grave2)), mode='constant')
y_agudo = np.pad(y_agudo, (0, max_length - len(y_agudo)), mode='constant')

# Combinar as três versões: duas graves e uma aguda
combined_audio = y_grave1 + y_grave2 + y_agudo  # Juntando as três faixas

# Salvar o áudio combinado
output_file = "triple.mp3"
sf.write(output_file, combined_audio, sr, format='MP3')

# Remover o arquivo temporário
os.remove(temp_audio_file)

print("Áudio combinado (grave e agudo) salvo em:", output_file)
