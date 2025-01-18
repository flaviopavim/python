import time
import pyautogui
from pynput import mouse, keyboard

# Global variables
last_click_time = None  # Stores the time of the last click
txt = 'import time\n'  # Initializes the script to be written
txt += 'import pyautogui\n'
txt += 'from pynput import keyboard\n'
txt += '\n'
txt += 'def click():\n'  # Adds the definition of the function
recording = False  # Flag to indicate if recording is active

# Function to simulate a click with a delay
def click(interval, x, y):
    time.sleep(interval)
    pyautogui.click(x, y)

# Function triggered on mouse click events
def on_click(x, y, button, pressed):
    global last_click_time, txt, recording

    if recording and pressed:  # Only record clicks when recording is active
        current_time = time.time()

        # Calculate the interval between clicks
        if last_click_time is not None:
            interval = round(current_time - last_click_time, 2)
        else:
            interval = 0  # First click, interval is 0

        last_click_time = current_time

        if interval > 0:
            # Record the interval in the script
            txt += f"    time.sleep({interval})\n"
            print(f"    time.sleep({interval})")
        
        # Record the click coordinates in the script
        txt += f"    pyautogui.click({x}, {y})\n"
        print(f"    pyautogui.click({x}, {y})")

        # If right mouse button is clicked, finalize and save the script
        if button == mouse.Button.right:
            txt += '\n'
            txt += 'def on_press(key):\n'
            txt += '    try:\n'
            txt += '        if key.char == "a":\n'
            txt += '            print(\'Key "a" pressed. Starting in 3 seconds...\')\n'
            txt += '            time.sleep(3)\n'
            txt += '            click()\n'
            txt += '    except AttributeError:\n'
            txt += '        pass\n'
            txt += '\n'
            txt += 'with keyboard.Listener(on_press=on_press) as listener:\n'
            txt += '    print(\'Press "a" to start execution.\')\n'
            txt += '    listener.join()'
            
            # Save the recorded script to a file
            with open('Mr. Mime.py', 'w', encoding='utf-8') as file:
                file.write(txt)
            print("Coordinates saved to 'Mr. Mime.py'.")
            listener.stop()  # Stop the mouse listener

# Function triggered on keyboard press events
def on_press(key):
    global recording

    try:
        if key.char == 'a':  # Start recording when 'a' is pressed
            recording = True
            print("Recording started. Click to record coordinates.")
    except AttributeError:
        pass  # Ignore non-character keys

# Activate listeners for mouse clicks and keyboard presses
with mouse.Listener(on_click=on_click) as listener:
    with keyboard.Listener(on_press=on_press) as key_listener:
        print("Press 'a' to start recording. Left-click to record coordinates.")
        key_listener.join()

print("Program terminated.")
