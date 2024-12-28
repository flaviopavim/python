import pygame
import time

# Initialize pygame
pygame.init()

# Load drum sounds
kick_sound = pygame.mixer.Sound("kick-tron.wav")
snare_sound = pygame.mixer.Sound("snare.wav")
hihat_sound = pygame.mixer.Sound("hihat.wav")

# Define the drum beat patterns
kick_pattern =  [ 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0 ]
#kick_pattern =  [ 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ]
#kick_pattern = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
snare_pattern = [ 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1 ]
hihat_pattern = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
#hihat_pattern = [ 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ]
#hihat_pattern = [ 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ]

#snare_pattern = [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1]
#snare_pattern = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

# Set the tempo (in beats per minute)
tempo = 400
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
        # Play the drum sounds based on the patterns
        if kick_pattern[beat_index] == 1:
            kick_sound.play()
        if snare_pattern[beat_index] == 1:
            snare_sound.play()
        if hihat_pattern[beat_index] == 1:
            hihat_sound.play()
            
        # Move to the next beat index
        beat_index = (beat_index + 1) % len(kick_pattern)
        start_time = current_time

# Quit the game
pygame.quit()
