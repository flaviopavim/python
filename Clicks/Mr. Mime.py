import time
import pyautogui
from pynput import keyboard

def click():
    # Simulates a sequence of mouse clicks at specific coordinates with delays
    pyautogui.click(605, 897)  # Click at position (605, 897)
    time.sleep(3.06)  # Wait for 3.06 seconds
    pyautogui.click(996, 730)  # Click at position (996, 730)
    time.sleep(2.91)  # Wait for 2.91 seconds
    pyautogui.click(952, 576)  # Click at position (952, 576)
    time.sleep(7.05)  # Wait for 7.05 seconds
    pyautogui.click(95, 355)  # Click at position (95, 355)
    time.sleep(1.67)  # Wait for 1.67 seconds
    pyautogui.click(664, 577)  # Click at position (664, 577)
    time.sleep(0.17)  # Wait for 0.17 seconds
    pyautogui.click(664, 577)  # Click again at the same position
    time.sleep(2.81)  # Wait for 2.81 seconds
    pyautogui.click(1195, 961)  # Click at position (1195, 961)
    time.sleep(1.78)  # Wait for 1.78 seconds
    pyautogui.click(1195, 961)  # Click again at the same position

def on_press(key):
    # Listener function triggered when a key is pressed
    try:
        if key.char == "a":  # Checks if the pressed key is 'a'
            print('Key "a" pressed. Starting in 3 seconds...')
            time.sleep(3)  # Wait for 3 seconds before starting the sequence
            click()  # Call the click function to execute the sequence
    except AttributeError:
        # Handles non-character keys without causing an error
        pass

# Start a keyboard listener to detect key presses
with keyboard.Listener(on_press=on_press) as listener:
    print('Press "a" to start the execution.')  # Instruction to the user
    listener.join()  # Keeps the program running and listening for key presses
