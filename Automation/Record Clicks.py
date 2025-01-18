"""
This script is a Python-based macro recorder for mouse clicks. It captures mouse click coordinates 
and time intervals between clicks to generate an automated script that can reproduce the recorded actions.

Key Features:
1. Records mouse clicks and intervals upon activation.
2. Saves the recorded actions into a Python script file named "Mr. Mime.py".
3. Listens for keyboard inputs to start recording and finalize the script.
4. Generates an executable Python script with the recorded macro.

Dependencies:
- `pyautogui`: Simulates mouse clicks and other GUI interactions.
- `pynput`: Listens for mouse and keyboard inputs.

Usage:
1. Run the script.
2. Press the 'a' key to start recording.
3. Perform mouse clicks. Right-click to finalize and save the recording.
4. The generated script can be used to replay the recorded actions.
"""

import time
import pyautogui
from pynput import mouse, keyboard

# Global variables
last_click_time = None  # Stores the time of the last click
txt = 'import time\n'  # Initializes the text for the output script
txt += 'import pyautogui\n'
txt += 'from pynput import keyboard\n\n'
txt += 'def click():\n'  # Starts with the click function definition
recording = False  # Indicates if the program is recording

def click(interval, x, y):
    """
    Simulates a mouse click after a specified interval at the given coordinates.
    """
    time.sleep(interval)
    pyautogui.click(x, y)

def on_click(x, y, button, pressed):
    """
    Handles mouse click events. Records the coordinates and intervals between clicks,
    and appends them to the output script.
    """
    global last_click_time, txt, recording

    if recording and pressed:
        current_time = time.time()

        # Calculate time interval between clicks
        if last_click_time is not None:
            interval = round(current_time - last_click_time, 2)
        else:
            interval = 0  # First click, no interval

        last_click_time = current_time

        # Append the interval and click action to the output script
        if interval > 0:
            txt += f"    time.sleep({interval})\n"
            print(f"    time.sleep({interval})")
        
        txt += f"    pyautogui.click({x}, {y})\n"
        print(f"    pyautogui.click({x}, {y})")

        # Save the script and stop the listener on right-click
        if button == mouse.Button.right:
            txt += '\n'
            txt += 'def on_press(key):\n'
            txt += '    try:\n'
            txt += '        if key.char == "a":\n'
            txt += '            print(\'Key "a" pressed. Starting in 3 seconds...\')\n'
            txt += '            time.sleep(3)\n'
            txt += '            click()\n'
            txt += '    except AttributeError:\n'
            txt += '        pass\n\n'
            txt += 'with keyboard.Listener(on_press=on_press) as listener:\n'
            txt += '    print(\'Press "a" to start execution.\')\n'
            txt += '    listener.join()'
            
            with open('Mr. Mime.py', 'w', encoding='utf-8') as file:
                file.write(txt)
            print("Coordinates saved to 'Mr. Mime.py'.")
            listener.stop()  # Stops the listener

def on_press(key):
    """
    Handles keyboard press events. Starts recording when 'a' is pressed.
    """
    global recording

    try:
        if key.char == 'a':  # Start recording on 'a' key press
            recording = True
            print("Recording started. Click to register coordinates.")
    except AttributeError:
        pass  # Ignore other keys

# Activate listeners for mouse clicks and keyboard input
with mouse.Listener(on_click=on_click) as listener:
    with keyboard.Listener(on_press=on_press) as key_listener:
        print("Press 'a' to start recording. Right-click to save the recorded coordinates.")
        key_listener.join()

print("Program terminated.")
