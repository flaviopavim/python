import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Basic sound configuration
pygame.mixer.init(channels=1)  # Sets the mixer for a single channel

# Maps notes to frequencies (three octaves)
notes_to_frequencies = {
    "C": [130.81, 261.63, 523.25],  # C
    "D": [146.83, 293.66, 587.33],  # D
    "E": [164.81, 329.63, 659.25],  # E
    "F": [174.61, 349.23, 698.46],  # F
    "G": [196.00, 392.00, 783.99],  # G
    "A": [220.00, 440.00, 880.00],  # A
    "B": [246.94, 493.88, 987.77],  # B
}

# Define the duration of the sound in seconds and the sampling rate
duration = 1/3  # duration of the sound in seconds
sampling_rate = 44100  # sampling rate in Hz

# Create the melody as an array of tuples containing notes and duration times
melody = [("E", 0.5), ("E", 0.5), ("E", 1), ("E", 0.5), ("E", 0.5), ("E", 1),
          ("E", 0.5), ("G", 0.5), ("C", 1), ("D", 0.5), ("E", 0.5), ("F", 0.5),
          ("F", 0.5), ("F", 0.5), ("F", 0.5), ("F", 0.5), ("E", 0.5), ("E", 0.5),
          ("E", 0.5), ("E", 0.5), ("D", 0.5), ("D", 0.5), ("E", 0.5), ("D", 0.5),
          ("G", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5), ("E", 0.5),
          ("E", 0.5), ("D", 0.5), ("D", 0.5), ("E", 0.5), ("D", 0.5), ("C", 1)]

# Function to convert a note into a sine wave array
def note_to_wave(note, note_duration, octave):
    frequency = notes_to_frequencies[note][octave]
    num_samples = int(note_duration * sampling_rate)
    time = np.linspace(0, note_duration, num_samples)
    return np.sin(2 * np.pi * frequency * time)

# Function to play the melody
def play_melody(melody, octave):
    for note, note_duration in melody:
        wave = note_to_wave(note, note_duration, octave)
        pygame.mixer.Sound(wave.astype(np.float32)).play()
        pygame.time.wait(int(note_duration * 1000))  # Waits for the note duration

# Play the melody in different octaves
play_melody(melody, 0)  # First octave
pygame.time.wait(500)  # Waits a bit between octaves
play_melody(melody, 1)  # Second octave
pygame.time.wait(500)  # Waits a bit between octaves
play_melody(melody, 2)  # Third octave

# Wait a bit after the music ends
pygame.time.wait(500)

# Quit pygame
pygame.quit()
