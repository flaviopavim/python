import os
import numpy as np
import librosa
import soundfile as sf
import scipy.signal as sig
from gtts import gTTS

texto = "Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?"

# Gerar o áudio com gTTS
temp_audio_file = "temp_audio.mp3"
tts = gTTS(text=texto, lang="pt-br", slow=False)
tts.save(temp_audio_file)

# Carregar o áudio
y, sr = librosa.load(temp_audio_file, sr=None)

# 1. Acelerar o áudio (1.8x)
y_fast = librosa.effects.time_stretch(y, rate=1.8)

# 2. Ajustar o pitch levemente (0.2 semitons)
y_pitched = librosa.effects.pitch_shift(y_fast, sr=sr, n_steps=0.2)

# 3. Adicionar Reverb
def apply_reverb(audio, sr, decay=0.1):
    """Aplica um efeito de reverb simples usando convolução."""
    # Criar um impulso para simular reverb
    impulse_response = np.exp(-np.linspace(0, 3, int(sr * decay)))  # Decaimento do reverb
    impulse_response /= np.max(impulse_response)  # Normalizar

    # Aplicar convolução para adicionar reverb
    audio_reverb = sig.fftconvolve(audio, impulse_response, mode='full')
    return audio_reverb[:len(audio)]  # Ajustar tamanho final

y_reverb = apply_reverb(y_pitched, sr)

# Salvar o áudio processado
output_file = "reverb.mp3"
sf.write(output_file, y_reverb, sr, format='MP3')

# Remover o arquivo temporário
os.remove(temp_audio_file)

print("Áudio processado e salvo com reverb!")
