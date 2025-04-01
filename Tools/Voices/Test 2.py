import pyttsx3

texto = "Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?"

engine = pyttsx3.init()

# Lista de vozes disponíveis no sistema
voices = engine.getProperty('voices')
    
# Selecionar uma voz feminina ou masculina
engine.setProperty('voice', voices[0].id)

# Ajustar a velocidade e o volume
engine.setProperty('rate', 250)  # Velocidade (padrão: 200)
engine.setProperty('volume', 1)  # Volume (0.0 a 1.0)

engine.save_to_file(texto, "test2.mp3")
engine.runAndWait()

print(f"Áudio salvo")
