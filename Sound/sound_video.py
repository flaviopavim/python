import pygame
import numpy as np

# Inicialize o pygame
pygame.init()

# Configuração básica do som
pygame.mixer.init(channels=1)  # Configura o mixer para um único canal

# Mapeia as notas para frequências (três oitavas)
notas_para_frequencias = {
    "C": [130.81, 261.63, 523.25],  # Dó
    "D": [146.83, 293.66, 587.33],  # Ré
    "E": [164.81, 329.63, 659.25],  # Mi
    "F": [174.61, 349.23, 698.46],  # Fá
    "G": [196.00, 392.00, 783.99],  # Sol
    "A": [220.00, 440.00, 880.00],  # Lá
    "B": [246.94, 493.88, 987.77],  # Si
}

# Define a duração do som em segundos e a taxa de amostragem
duracao = 1/3  # duração do som em segundos
taxa_amostragem = 44100  # taxa de amostragem em Hz

# Cria a melodia como um array de tuplas contendo as notas e os tempos de duração
melodia = [("E", 0.5), ("E", 0.5), ("E", 1), ("E", 0.5), ("E", 0.5), ("E", 1),
           ("E", 0.5), ("G", 0.5), ("C", 1), ("D", 0.5), ("E", 0.5), ("F", 0.5),
           ("F", 0.5), ("F", 0.5), ("F", 0.5), ("F", 0.5), ("E", 0.5), ("E", 0.5),
           ("E", 0.5), ("E", 0.5), ("D", 0.5), ("D", 0.5), ("E", 0.5), ("D", 0.5),
           ("G", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5),
           ("E", 0.5), ("D", 0.5), ("D", 0.5), ("E", 0.5), ("D", 0.5), ("C", 1)]

# Função para converter uma nota em um array de onda senoidal
def nota_para_onda(nota, duracao_nota, oitava):
    frequencia = notas_para_frequencias[nota][oitava]
    numero_de_amostras = int(duracao_nota * taxa_amostragem)
    tempo = np.linspace(0, duracao_nota, numero_de_amostras)
    return np.sin(2 * np.pi * frequencia * tempo)

# Função para tocar a melodia
def tocar_melodia(melodia, oitava):
    for nota, duracao_nota in melodia:
        onda = nota_para_onda(nota, duracao_nota, oitava)
        pygame.mixer.Sound(onda.astype(np.float32)).play()
        pygame.time.wait(int(duracao_nota * 1000))  # Aguarda o tempo de duração da nota

# Tocar a melodia em diferentes oitavas
tocar_melodia(melodia, 0)  # Primeira oitava
pygame.time.wait(500)  # Aguarda um pouco entre as oitavas
tocar_melodia(melodia, 1)  # Segunda oitava
pygame.time.wait(500)  # Aguarda um pouco entre as oitavas
tocar_melodia(melodia, 2)  # Terceira oitava

# Aguarda um pouco após o término da música
pygame.time.wait(500)

# Finaliza o pygame
pygame.quit()
