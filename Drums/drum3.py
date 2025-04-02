import pygame

# Inicializa o pygame
pygame.init()

# Carrega os sons
kick_sound = pygame.mixer.Sound("audio/kick.wav")
snare_sound = pygame.mixer.Sound("audio/snare.wav")
hihat_sound = pygame.mixer.Sound("audio/hihat.wav")

# Define os padrões de batida (todos com o mesmo tamanho)
kick_pattern = ["kick", "", "", "", "kick", "", "", "", "kick", "", "", "", "kick", "", "", ""]
snare_pattern = ["", "", "", "", "snare", "", "", "", "", "", "", "", "snare", "", "", ""]
hihat_pattern = ["hihat", "", "hihat", "", "hihat", "", "hihat", "", "hihat", "", "hihat", "", "hihat", "", "hihat", ""]

# Configuração de tempo (similar a teclados)
BPM = 280  # Pode ser ajustado dinamicamente como nos teclados
PPQ = 96  # Padrão de muitos teclados MIDI
steps_per_beat = 4  # Como um sequenciador de bateria (16 passos no total)

# Calcula a duração de cada passo
beat_duration = 60000 / BPM  # Tempo de 1 batida (milissegundos)
step_duration = beat_duration / steps_per_beat  # Tempo de cada subdivisão

# Variáveis de tempo
running = True
step_index = 0
start_time = pygame.time.get_ticks()  # Tempo inicial mais preciso

# Loop principal
while running:
    # Verifica eventos (para fechar a janela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tempo atual
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Verifica se é hora de tocar o próximo som
    if elapsed_time >= step_duration:
        if kick_pattern[step_index] == "kick":
            kick_sound.play()
        if snare_pattern[step_index] == "snare":
            snare_sound.play()
        if hihat_pattern[step_index] == "hihat":
            hihat_sound.play()

        # Avança para o próximo step e reinicia o tempo de referência
        step_index = (step_index + 1) % len(kick_pattern)
        start_time = current_time

# Encerra o pygame
pygame.quit()
