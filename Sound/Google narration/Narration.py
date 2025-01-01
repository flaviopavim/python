from gtts import gTTS

texto="";
with open('text.txt', encoding='utf-8') as file:
    texto = file.read()

print(texto)
    
tts = gTTS(text=texto, lang='pt-br', slow=False)
tts.save('audio.mp3')

print('Áudio criado')
