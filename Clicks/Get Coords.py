import pyautogui
import time

try:
    while True:
        # Capture the current position of the mouse cursor
        x, y = pyautogui.position()
        
        # Print the (x, y) coordinates of the mouse
        print(f"x: {x}, y: {y}")
        
        # Small delay to reduce CPU usage
        time.sleep(0.5)

except KeyboardInterrupt:
    # Handle keyboard interruption (Ctrl + C) gracefully
    print("\nProgram terminated.")
