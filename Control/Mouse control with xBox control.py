import pygame
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# Função para reconectar o controle
def reconnect_joystick():
    pygame.joystick.quit()  # Desconecta o joystick
    pygame.joystick.init()  # Reabre a conexão
    if pygame.joystick.get_count() == 0:
        print("Nenhum controle conectado!")
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Conectado ao controle: {joystick.get_name()}")
    return joystick

# Inicialização do Pygame
pygame.init()

# Inicialização do controle Xbox
joystick = reconnect_joystick()
if joystick is None:
    exit()

# Inicialização do mouse e teclado
mouse = Controller()
keyboard = KeyboardController()

# Configurações de controle
base_sensitivity = 5  # Sensibilidade padrão
accelerated_sensitivity = 15  # Sensibilidade acelerada
current_sensitivity = base_sensitivity
dead_zone = 0.2  # Zona morta para evitar movimentos involuntários
dragging = False  # Estado do arrasta e solta
alt_tabbing = False  # Estado para alternância contínua de janelas

# Loop principal
running = True
while running:
    try:
        # Verifica se o joystick está desconectado e tenta reconectar
        if pygame.joystick.get_count() == 0:
            print("Controle desconectado! Tentando reconectar...")
            joystick = reconnect_joystick()
            if joystick is None:
                print("Falha ao reconectar o controle.")
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
                continue

        # Processa os eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Verifica botões pressionados
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:  # Botão X pressionado
                    if not dragging:
                        mouse.press(Button.left)  # Pressiona o botão esquerdo
                        dragging = True
                elif event.button == 1:  # Botão B pressionado
                    mouse.click(Button.right)  # Clique direito
                elif event.button == 0:  # Botão A pressionado
                    current_sensitivity = accelerated_sensitivity  # Aumenta a sensibilidade
                elif event.button == 3:  # Botão Y pressionado
                    alt_tabbing = True
                    keyboard.press(Key.alt)  # Segura Alt

            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 2:  # Botão X solto
                    if dragging:
                        mouse.release(Button.left)  # Solta o botão esquerdo
                        dragging = False
                elif event.button == 0:  # Botão A solto
                    current_sensitivity = base_sensitivity  # Volta à sensibilidade normal
                elif event.button == 3:  # Botão Y solto
                    alt_tabbing = False
                    keyboard.release(Key.alt)  # Solta Alt

        # Alternância contínua de janelas enquanto Y estiver pressionado
        if alt_tabbing:
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)  # Aumenta o intervalo para alternância mais lenta

        # Verifica se o joystick está conectado antes de capturar os eixos
        if joystick is not None:
            # Captura os valores dos eixos do analógico esquerdo
            x_axis = joystick.get_axis(0)  # Eixo X (esquerda/direita)
            y_axis = joystick.get_axis(1)  # Eixo Y (cima/baixo)

            # Verifica se os valores estão fora da zona morta
            if abs(x_axis) > dead_zone or abs(y_axis) > dead_zone:
                # Atualiza as coordenadas do mouse
                current_pos = mouse.position
                new_x = current_pos[0] + (x_axis * current_sensitivity)
                new_y = current_pos[1] + (y_axis * current_sensitivity)
                mouse.position = (new_x, new_y)

        # Adiciona uma pausa para suavizar o loop
        time.sleep(0.01)
    
    except Exception as e:
        print(f"Erro durante o processamento de eventos: {e}")
        time.sleep(1)  # Espera 1 segundo antes de tentar novamente

# Encerra o Pygame
pygame.quit()
