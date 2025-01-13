import pygame
import sys
import json
import os
import copy

# Configurações iniciais
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 32
CELL_SIZE = 10
LAYERS = 8
FILENAME = "file.draw"
FRAME_DELAY = 0.2  # Tempo entre quadros em segundos

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TOOLS_BG = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor com Camadas 32x32")

# Paleta de cores expandida
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128), (255, 165, 0),
    (255, 192, 203), (255, 105, 180), (255, 20, 147), (75, 0, 130)
]
selected_color = BLACK
selected_color_index = 6

# Função para inicializar ou carregar o arquivo
def initialize_file():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [[[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(LAYERS)]

# Salva o estado atual no arquivo
def save_to_file():
    with open(FILENAME, "w") as f:
        json.dump(grid, f)

# Função para salvar com nome incremental
def save_as_new_file():
    i = 1
    while os.path.exists(f"file{i}.draw"):
        i += 1
    new_filename = f"file{i}.draw"
    with open(new_filename, "w") as f:
        json.dump(grid, f)
    return new_filename

# Função para limpar o quadro
def clear_grid():
    global grid
    grid = [[[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(LAYERS)]
    save_to_file()

# Inicializa o array 3D (camadas)
grid = initialize_file()
current_layer = 0
playing = False  # Controla o estado do botão "Play"

# Função para desenhar a barra de camadas
def draw_layer_bar():
    for i in range(LAYERS):
        color = GRAY if i == current_layer else TOOLS_BG
        pygame.draw.rect(screen, color, (i * 50 + 100, 10, 40, 40))
        pygame.draw.rect(screen, WHITE, (i * 50 + 100, 10, 40, 40), 2)
        # Exibe o número da camada
        font = pygame.font.Font(None, 24)
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (i * 50 + 115, 20))

# Função para desenhar a paleta de cores
def draw_palette():
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10, i * 30 + 60, 20, 20))
        if i == selected_color_index:
            pygame.draw.rect(screen, WHITE, (10, i * 30 + 60, 20, 20), 2)

# Função para desenhar a área de desenho
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE if grid[current_layer][y][x] == 0 else colors[grid[current_layer][y][x] - 1]
            pygame.draw.rect(
                screen, color,
                (100 + x * CELL_SIZE, 60 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen, GRAY,
                (100 + x * CELL_SIZE, 60 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

# Função para desenhar ferramentas
def draw_tools():
    pygame.draw.rect(screen, TOOLS_BG, (480, 60, 150, 200))
    
    # Desenhando os botões de ferramentas
    pygame.draw.rect(screen, BLACK, (490, 70, 30, 30))  # Desenhar
    pygame.draw.rect(screen, WHITE, (490, 110, 30, 30))  # Borracha
    pygame.draw.rect(screen, BLUE if playing else TOOLS_BG, (490, 150, 30, 30))  # Play
    pygame.draw.rect(screen, GRAY, (490, 190, 30, 30))  # Botão salvar como
    
    # Escrevendo os nomes dos botões
    font = pygame.font.Font(None, 20)
    text_draw = font.render("Desenhar", True, WHITE)
    screen.blit(text_draw, (530, 75))
    text_erase = font.render("Borracha", True, WHITE)
    screen.blit(text_erase, (530, 115))
    text_play = font.render("Play", True, WHITE)
    screen.blit(text_play, (530, 155))
    text_save = font.render("Salvar", True, WHITE)
    screen.blit(text_save, (530, 195))

# Variáveis de controle
drawing = False
using_eraser = False
copied_layer = None  # Camada copiada

# Função de animação
def play_animation():
    global current_layer, playing
    while playing:
        current_layer = (current_layer + 1) % LAYERS
        pygame.time.delay(int(FRAME_DELAY * 1000))
        screen.fill(WHITE)
        draw_layer_bar()
        draw_palette()
        draw_grid()
        draw_tools()
        pygame.display.flip()

# Função para copiar o conteúdo de uma camada
def copy_layer():
    global copied_layer
    copied_layer = copy.deepcopy(grid[current_layer])

# Função para colar o conteúdo copiado em outra camada
def paste_layer():
    global copied_layer
    if copied_layer is not None:
        grid[current_layer] = copy.deepcopy(copied_layer)
        save_to_file()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_to_file()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Verifica seleção na barra de camadas
            if 100 <= x < 100 + LAYERS * 50 and 10 <= y <= 50:
                current_layer = (x - 100) // 50

            # Verifica seleção na paleta de cores
            elif 10 <= x <= 30:
                for i in range(len(colors)):
                    if i * 30 + 60 <= y <= i * 30 + 90:
                        selected_color_index = i
                        selected_color = colors[i]

            # Verifica clique nas ferramentas
            elif 490 <= x <= 520:
                if 70 <= y <= 100:
                    using_eraser = False  # Ferramenta de desenho
                elif 110 <= y <= 140:
                    using_eraser = True  # Ferramenta de borracha
                elif 150 <= y <= 180:
                    playing = not playing
                    if playing:
                        pygame.time.set_timer(pygame.USEREVENT, int(FRAME_DELAY * 1000))
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                elif 190 <= y <= 220:
                    new_filename = save_as_new_file()
                    print(f"Salvo como {new_filename}")
                    clear_grid()  # Limpa o quadro após salvar

            # Verifica clique na área de desenho
            elif 100 <= x < 100 + GRID_SIZE * CELL_SIZE and 60 <= y < 60 + GRID_SIZE * CELL_SIZE:
                drawing = True

        if event.type == pygame.USEREVENT and playing:
            current_layer = (current_layer + 1) % LAYERS

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        # Eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                copy_layer()  # Ctrl+C copia
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                paste_layer()  # Ctrl+V cola
            elif event.key == pygame.K_RETURN:
                playing = not playing  # Enter alterna entre play/pause
                if playing:
                    pygame.time.set_timer(pygame.USEREVENT, int(FRAME_DELAY * 1000))
                else:
                    pygame.time.set_timer(pygame.USEREVENT, 0)

    # Desenho contínuo ao arrastar o mouse
    if drawing:
        x, y = pygame.mouse.get_pos()
        if 100 <= x < 100 + GRID_SIZE * CELL_SIZE and 60 <= y < 60 + GRID_SIZE * CELL_SIZE:
            grid_x = (x - 100) // CELL_SIZE
            grid_y = (y - 60) // CELL_SIZE
            grid[current_layer][grid_y][grid_x] = 0 if using_eraser else selected_color_index + 1
            save_to_file()

    # Atualiza a tela
    screen.fill(WHITE)
    draw_layer_bar()
    draw_palette()
    draw_grid()
    draw_tools()
    pygame.display.flip()
