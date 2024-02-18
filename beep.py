import time
import winsound

# Define the frequencies for the tones
c = 261
d = 294
e = 329
f = 349
g = 391
gS = 415
a = 440
aS = 455
b = 466
cH = 523
cSH = 554
dH = 587
dSH = 622
eH = 659
fH = 698
fSH = 740
gH = 784
gSH = 830
aH = 880

# Define the durations for the notes
quarter_note = 150
eighth_note = 50
half_note = 1000

def beep(frequency, duration):
    winsound.Beep(frequency, duration)

def march():
    # First bit
    beep(440, 1300)

while True:
    march()
    time.sleep(2.5)
