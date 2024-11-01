import time
import pyautogui
from pynput import keyboard

def click():
    pyautogui.click(605, 897)
    time.sleep(3.06)
    pyautogui.click(996, 730)
    time.sleep(2.91)
    pyautogui.click(952, 576)
    time.sleep(7.05)
    pyautogui.click(95, 355)
    time.sleep(1.67)
    pyautogui.click(664, 577)
    time.sleep(0.17)
    pyautogui.click(664, 577)
    time.sleep(2.81)
    pyautogui.click(1195, 961)
    time.sleep(1.78)
    pyautogui.click(1195, 961)

def on_press(key):
    try:
        if key.char == "a":
            print('Tecla a pressionada. Iniciando em 3 segundos...')
            time.sleep(3)
            click()
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    print('Pressione a para iniciar a execução.')
    listener.join()