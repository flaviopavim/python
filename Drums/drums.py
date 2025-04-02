import pygame
import time

# Initialize pygame
pygame.init()

# Load drum sounds
kick_sound = pygame.mixer.Sound("audio/kick.wav")
snare_sound = pygame.mixer.Sound("audio/snare.wav")
hihat_sound = pygame.mixer.Sound("audio/hihat.wav")

# Define drum positions on the screen
kick_position = (100, 100)
snare_position = (200, 100)
hihat_position = (300, 100)

# Define the drum beat patterns
kick_pattern = [
    ("kick", 0),
    ("", 1),
    ("", 2),
    ("", 3),
    ("kick", 4),
    ("", 5),
    ("", 6),
    ("", 7),
    ("kick", 8),
    ("", 9),
    ("", 10),
    ("", 11),
    ("kick", 12),
    ("", 13),
    ("", 14),
    ("", 15),
]

snare_pattern = [
    ("", 0),
    ("", 1),
    ("", 2),
    ("", 3),
    ("snare", 4),
    ("", 5),
    ("", 6),
    ("", 7),
    ("", 8),
    ("", 9),
    ("", 10),
    ("", 11),
    ("snare", 12),
    ("", 13),
    ("", 14),
    ("", 15),
]

hihat_pattern = [
    ("hihat", 0),
    ("hihat", 1),
    ("hihat", 2),
    ("hihat", 3),
    ("hihat", 4),
    ("hihat", 5),
    ("hihat", 6),
    ("hihat", 7),
    ("hihat", 8),
    ("hihat", 9),
    ("hihat", 10),
    ("hihat", 11),
    ("hihat", 12),
    ("hihat", 13),
    ("hihat", 14),
    ("hihat", 15),
]

# Set the tempo (in beats per minute)
tempo = 880
beat_duration = 60 / tempo  # duration of each beat in seconds

# Game loop
running = True
beat_index = 0
start_time = time.time()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the elapsed time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Check if it's time to play the next beat
    if elapsed_time >= beat_duration:
        kick_drum, kick_beat_number = kick_pattern[beat_index]
        snare_drum, snare_beat_number = snare_pattern[beat_index]
        hihat_drum, hihat_beat_number = hihat_pattern[beat_index]

        if kick_drum == "kick":
            kick_sound.play()
        if snare_drum == "snare":
            snare_sound.play()
        if hihat_drum == "hihat":
            hihat_sound.play()

        beat_index = (beat_index + 1) % len(kick_pattern)
        start_time = current_time

# Quit the game
pygame.quit()
