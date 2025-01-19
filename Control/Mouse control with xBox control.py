import pygame
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# Function to reconnect the joystick if disconnected
def reconnect_joystick():
    pygame.joystick.quit()  # Disconnects the joystick
    pygame.joystick.init()  # Reinitializes the joystick connection
    if pygame.joystick.get_count() == 0:
        print("No joystick connected!")
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to joystick: {joystick.get_name()}")
    return joystick

# Pygame initialization
pygame.init()

# Attempt to connect to the Xbox controller
joystick = reconnect_joystick()
if joystick is None:
    exit()

# Initialize mouse and keyboard controllers
mouse = Controller()
keyboard = KeyboardController()

# Sensitivity and control settings
base_sensitivity = 5  # Default mouse sensitivity
accelerated_sensitivity = 15  # Increased sensitivity when a button is held
current_sensitivity = base_sensitivity
dead_zone = 0.2  # Dead zone to prevent minor joystick drift
dragging = False  # Tracks if the left mouse button is being held
alt_tabbing = False  # Tracks if Alt+Tab is being held for window switching

# Main loop
running = True
while running:
    try:
        # Reconnect joystick if disconnected
        if pygame.joystick.get_count() == 0:
            print("Joystick disconnected! Attempting to reconnect...")
            joystick = reconnect_joystick()
            if joystick is None:
                print("Failed to reconnect joystick.")
                time.sleep(1)  # Wait before retrying
                continue

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button presses
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:  # X button pressed
                    if not dragging:
                        mouse.press(Button.left)  # Hold left mouse button
                        dragging = True
                elif event.button == 1:  # B button pressed
                    mouse.click(Button.right)  # Perform a right-click
                elif event.button == 0:  # A button pressed
                    current_sensitivity = accelerated_sensitivity  # Increase sensitivity
                elif event.button == 3:  # Y button pressed
                    alt_tabbing = True
                    keyboard.press(Key.alt)  # Hold the Alt key

            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 2:  # X button released
                    if dragging:
                        mouse.release(Button.left)  # Release left mouse button
                        dragging = False
                elif event.button == 0:  # A button released
                    current_sensitivity = base_sensitivity  # Reset sensitivity
                elif event.button == 3:  # Y button released
                    alt_tabbing = False
                    keyboard.release(Key.alt)  # Release Alt key

        # Handle continuous Alt+Tab switching
        if alt_tabbing:
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.5)  # Slow down window switching

        # Update mouse position based on joystick input
        if joystick is not None:
            x_axis = joystick.get_axis(0)  # Horizontal movement
            y_axis = joystick.get_axis(1)  # Vertical movement

            # Only move the mouse if joystick is outside the dead zone
            if abs(x_axis) > dead_zone or abs(y_axis) > dead_zone:
                current_pos = mouse.position
                new_x = current_pos[0] + (x_axis * current_sensitivity)
                new_y = current_pos[1] + (y_axis * current_sensitivity)
                mouse.position = (new_x, new_y)

        # Pause to avoid overloading the loop
        time.sleep(0.01)

    except Exception as e:
        print(f"Error during event processing: {e}")
        time.sleep(1)  # Wait before retrying

# Quit Pygame
pygame.quit()
