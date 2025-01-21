import pygame
import sys
import json
import os
import copy

# Initial configurations
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 32
CELL_SIZE = 10
LAYERS = 8
FILENAME = "file.draw"
FRAME_DELAY = 0.2  # Frame delay time in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TOOLS_BG = (150, 150, 150)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Layer Editor 32x32")

# Expanded color palette
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128), (255, 165, 0),
    (255, 192, 203), (255, 105, 180), (255, 20, 147), (75, 0, 130)
]
selected_color = BLACK
selected_color_index = 6

# Function to initialize or load the file
def initialize_file():
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return an empty grid if the file is not found
        return [[[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(LAYERS)]

# Save the current state to the file
def save_to_file():
    with open(FILENAME, "w") as f:
        json.dump(grid, f)

# Save the grid to a new file with an incremental name
def save_as_new_file():
    i = 1
    while os.path.exists(f"file{i}.draw"):
        i += 1
    new_filename = f"file{i}.draw"
    with open(new_filename, "w") as f:
        json.dump(grid, f)
    return new_filename

# Clear the grid (reset to default state)
def clear_grid():
    global grid
    grid = [[[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(LAYERS)]
    save_to_file()

# Initialize the 3D grid (layers)
grid = initialize_file()
current_layer = 0
playing = False  # Controls the play button state

# Function to draw the layer bar
def draw_layer_bar():
    for i in range(LAYERS):
        color = GRAY if i == current_layer else TOOLS_BG
        pygame.draw.rect(screen, color, (i * 50 + 100, 10, 40, 40))
        pygame.draw.rect(screen, WHITE, (i * 50 + 100, 10, 40, 40), 2)
        # Display the layer number
        font = pygame.font.Font(None, 24)
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (i * 50 + 115, 20))

# Function to draw the color palette
def draw_palette():
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10, i * 30 + 60, 20, 20))
        if i == selected_color_index:
            pygame.draw.rect(screen, WHITE, (10, i * 30 + 60, 20, 20), 2)

# Function to draw the grid
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

# Function to draw the tools section
def draw_tools():
    pygame.draw.rect(screen, TOOLS_BG, (480, 60, 150, 200))
    
    # Draw the tool buttons
    pygame.draw.rect(screen, BLACK, (490, 70, 30, 30))  # Draw tool
    pygame.draw.rect(screen, WHITE, (490, 110, 30, 30))  # Eraser tool
    pygame.draw.rect(screen, BLUE if playing else TOOLS_BG, (490, 150, 30, 30))  # Play button
    pygame.draw.rect(screen, GRAY, (490, 190, 30, 30))  # Save as button
    
    # Label the buttons
    font = pygame.font.Font(None, 20)
    screen.blit(font.render("Draw", True, WHITE), (530, 75))
    screen.blit(font.render("Eraser", True, WHITE), (530, 115))
    screen.blit(font.render("Play", True, WHITE), (530, 155))
    screen.blit(font.render("Save", True, WHITE), (530, 195))
