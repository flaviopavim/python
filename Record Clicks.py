import time
import pyautogui
from pynput import mouse, keyboard

last_click_time = None  # Armazena o tempo do último clique
txt = 'import time\n'
txt += 'import pyautogui\n'
txt += 'from pynput import keyboard\n'
txt += '\n'
txt += 'def click():\n'  # Inicializa o texto com a definição da função
recording = False  # Flag para indicar se estamos gravando

def click(interval, x, y):
    time.sleep(interval)
    pyautogui.click(x, y)

def on_click(x, y, button, pressed):
    global last_click_time, txt, recording

    if recording and pressed:
        current_time = time.time()

        # Calcula o intervalo de tempo entre cliques
        if last_click_time is not None:
            interval = round(current_time - last_click_time, 2)
        else:
            interval = 0  # Primeiro clique, intervalo é 0

        last_click_time = current_time

        if interval > 0:
            txt += f"    time.sleep({interval})\n"
            print(f"    time.sleep({interval})")
        
        txt += f"    pyautogui.click({x}, {y})\n"
        print(f"    pyautogui.click({x}, {y})")

        # Grava as coordenadas e intervalos no arquivo quando o botão direito é pressionado
        if button == mouse.Button.right:
            txt += '\n'
            txt += 'def on_press(key):\n'
            txt += '    try:\n'
            txt += '        if key.char == "a":\n'
            txt += '            print(\'Tecla a pressionada. Iniciando em 3 segundos...\')\n'
            txt += '            time.sleep(3)\n'
            txt += '            click()\n'
            txt += '    except AttributeError:\n'
            txt += '        pass\n'
            txt += '\n'
            txt += 'with keyboard.Listener(on_press=on_press) as listener:\n'
            txt += '    print(\'Pressione a para iniciar a execução.\')\n'
            txt += '    listener.join()'
            
            with open('Mr. Mime.py', 'w', encoding='utf-8') as file:
                file.write(txt)
            print("Coordenadas gravadas em 'Mr. Mime.py'.")
            listener.stop()  # Encerra o listener

def on_press(key):
    global recording

    try:
        if key.char == 'a':  # Inicia a gravação ao pressionar 'a'
            recording = True
            print("Gravação iniciada. Clique para registrar as coordenadas.")
    except AttributeError:
        pass  # Ignora outras teclas

# Ativa o listener para detectar cliques e teclas
with mouse.Listener(on_click=on_click) as listener:
    with keyboard.Listener(on_press=on_press) as key_listener:
        print("Pressione 'a' para iniciar a gravação. Clique com o botão direito para registrar as coordenadas.")
        key_listener.join()

print("Programa encerrado.")
