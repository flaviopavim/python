import pygame
import time

# Initialize pygame
pygame.init()

# Load drum sounds
kick_sound = pygame.mixer.Sound("kick.wav")
snare_sound = pygame.mixer.Sound("snare.wav")
hihat_sound = pygame.mixer.Sound("hihat.wav")

# Define drum positions on the screen
kick_position = (100, 100)
snare_position = (200, 100)
hihat_position = (300, 100)

# Define drum patterns using a dictionary
drum_patterns = {
    "kick": [("kick", 0), ("", 1), ("", 2), ("", 3), ("kick", 4), ("", 5), ("", 6), ("", 7), ("kick", 8), ("", 9), ("", 10), ("", 11), ("kick", 12), ("", 13), ("", 14), ("", 15)],
    "snare": [("snare", 4), ("snare", 12)],
    "hihat": [("hihat", i) for i in range(16)],
}

# Set the tempo (in beats per minute)
tempo = 880
beat_duration = 60 / tempo  # duration of each beat in seconds

# Function to play sounds
def play_sound(sound, volume=1.0):
    sound.set_volume(volume)
    sound.play()

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
        for drum, pattern in drum_patterns.items():
            drum_type, drum_beat_number = pattern[beat_index]
            if drum_type:
                play_sound(eval(f"{drum}_sound"))

        beat_index = (beat_index + 1) % len(drum_patterns["kick"])
        start_time = current_time

    # Rest of the game loop

# Quit the game
pygame.quit()
