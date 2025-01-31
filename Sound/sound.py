import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Basic sound configuration
pygame.mixer.init(channels=1)  # Set the mixer to a single channel

# Map notes to frequencies
notes_to_frequencies = {
    "A": 440.00,
    "B": 493.88,
    "C#": 554.37,
    "D": 587.33,
    "E": 659.25,
    "F#": 739.99,
    "G": 783.99,
}

# Define the duration of the sound in seconds and the sample rate
duration = 0.5  # sound duration in seconds
sample_rate = 44100  # sample rate in Hz

# Jingle Bells melody
jingle_bells_melody = [
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
    ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1), ("E", 0.1),
]

# Function to convert a note to a sine wave array
def note_to_wave(note, note_duration):
    frequency = notes_to_frequencies[note]
    num_samples = int(note_duration * sample_rate)
    time = np.linspace(0, note_duration, num_samples)
    return np.sin(2 * np.pi * frequency * time)

# Function to play the melody
def play_melody(melody):
    for note, note_duration in melody:
        wave = note_to_wave(note, note_duration)
        pygame.mixer.Sound(wave.astype(np.float32)).play()
        pygame.time.wait(int(note_duration * 1000))  # Wait for the note duration

# Play the Jingle Bells melody
play_melody(jingle_bells_melody)

# Wait a bit after the music ends
pygame.time.wait(500)

# Quit pygame
pygame.quit()
