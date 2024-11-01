import pyautogui
import time

try:
    while True:
        # Captura a posição atual do mouse
        x, y = pyautogui.position()
        
        # Imprime as coordenadas (x, y)
        print(f"x: {x}, y: {y}")
        
        # Pequeno intervalo para evitar sobrecarregar a CPU
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nPrograma finalizado.")
