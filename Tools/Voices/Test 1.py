import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Teste de um texto pra ver como fica a voz robótica. E aí, tudo bem? Como você está?", "test1.mp3")
engine.runAndWait()
print(f"Áudio salvo")
