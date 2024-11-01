import pygame
import numpy as np

# Inicialize o pygame
pygame.init()

# Configuração básica do som
pygame.mixer.init(channels=1)  # Configura o mixer para um único canal

# Mapeia as notas para frequências
notas_para_frequencias = {
    "A": 440.00,
    "B": 493.88,
    "C#": 554.37,
    "D": 587.33,
    "E": 659.25,
    "F#": 739.99,
    "G": 783.99,
}

# Define a duração do som em segundos e a taxa de amostragem
duracao = 0.5  # duração do som em segundos
taxa_amostragem = 44100  # taxa de amostragem em Hz

# Melodia de Jingle Bells
melodia_jingle_bells = [
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
]

# Função para converter uma nota em um array de onda senoidal
def nota_para_onda(nota, duracao_nota):
    frequencia = notas_para_frequencias[nota]
    numero_de_amostras = int(duracao_nota * taxa_amostragem)
    tempo = np.linspace(0, duracao_nota, numero_de_amostras)
    return np.sin(2 * np.pi * frequencia * tempo)

# Função para tocar a melodia
def tocar_melodia(melodia):
    for nota, duracao_nota in melodia:
        onda = nota_para_onda(nota, duracao_nota)
        pygame.mixer.Sound(onda.astype(np.float32)).play()
        pygame.time.wait(int(duracao_nota * 1000))  # Aguarda o tempo de duração da nota

# Tocar a melodia de Jingle Bells
tocar_melodia(melodia_jingle_bells)

# Aguarda um pouco após o término da música
pygame.time.wait(500)

# Finaliza o pygame
pygame.quit()
