from gtts import gTTS

texto="Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?"

# Gerar o áudio com gTTS
temp_audio_file = "normal.mp3"
tts = gTTS(text=texto, lang="pt-br", slow=False)
tts.save(temp_audio_file)

print('Audio created')