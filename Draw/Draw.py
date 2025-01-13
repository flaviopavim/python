import pygame
import sys

# Configurações iniciais
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 32
CELL_SIZE = 10

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TOOLS_BG = (150, 150, 150)

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor 32x32")

# Paleta de cores
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
    (0, 255, 255), (255, 0, 255), BLACK, WHITE
]
selected_color = BLACK

# Função para desenhar a paleta de cores
def draw_palette():
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10, i * 40 + 10, 30, 30))
        if color == selected_color:
            pygame.draw.rect(screen, WHITE, (10, i * 40 + 10, 30, 30), 2)

# Função para desenhar a área de desenho
def draw_grid(grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(
                screen, grid[y][x], 
                (100 + x * CELL_SIZE, 10 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen, GRAY, 
                (100 + x * CELL_SIZE, 10 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
            )

# Função para desenhar ferramentas
def draw_tools():
    pygame.draw.rect(screen, TOOLS_BG, (480, 10, 150, 100))
    pygame.draw.rect(screen, BLACK, (490, 20, 30, 30))  # Desenhar
    pygame.draw.rect(screen, WHITE, (490, 60, 30, 30))  # Borracha

# Inicializa a área de desenho
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Variáveis de controle
drawing = False
using_eraser = False

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Verifica seleção na paleta de cores
            if 10 <= x <= 40:
                for i, color in enumerate(colors):
                    if i * 40 + 10 <= y <= i * 40 + 40:
                        selected_color = color

            # Verifica clique nas ferramentas
            elif 490 <= x <= 520:
                if 20 <= y <= 50:
                    using_eraser = False  # Ferramenta de desenho
                elif 60 <= y <= 90:
                    using_eraser = True  # Ferramenta de borracha

            # Verifica clique na área de desenho
            elif 100 <= x < 100 + GRID_SIZE * CELL_SIZE and 10 <= y < 10 + GRID_SIZE * CELL_SIZE:
                drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    # Desenho contínuo ao arrastar o mouse
    if drawing:
        x, y = pygame.mouse.get_pos()
        if 100 <= x < 100 + GRID_SIZE * CELL_SIZE and 10 <= y < 10 + GRID_SIZE * CELL_SIZE:
            grid_x = (x - 100) // CELL_SIZE
            grid_y = (y - 10) // CELL_SIZE
            grid[grid_y][grid_x] = WHITE if using_eraser else selected_color

    # Atualiza a tela
    screen.fill(WHITE)
    draw_palette()
    draw_grid(grid)
    draw_tools()
    pygame.display.flip()
