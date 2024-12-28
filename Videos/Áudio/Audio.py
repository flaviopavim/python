from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import os
import random

diretorio = "./"

for arquivo in os.listdir(diretorio):
    if arquivo.endswith(".txt"):
        nome_arquivo, extensao = os.path.splitext(arquivo)
        with open(os.path.join(diretorio, arquivo), "r") as f:
            conteudo = f.read()
            print(nome_arquivo)
            with open(diretorio+nome_arquivo+".txt", encoding='utf-8') as file:
                texto = file.read()
            print('Salvando audio')
            tts = gTTS(text=texto, lang='pt-br', slow=False)
            tts.save(nome_arquivo+'.mp3')
            print('Áudio salvo')
