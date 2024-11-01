import cv2

# Configurações do vídeo
largura = 640
altura = 480
fps = 30.0

# Inicializar o objeto de captura da webcam
capture = cv2.VideoCapture(0)

# Definir as configurações de vídeo
capture.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
capture.set(cv2.CAP_PROP_FPS, fps)

# Definir o codec de vídeo e o objeto de gravação
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video.avi', fourcc, fps, (largura, altura))

while True:
    # Ler o próximo frame da webcam
    ret, frame = capture.read()

    if ret:
        # Escrever o frame no arquivo de vídeo
        out.write(frame)

        # Exibir o frame capturado em tempo real
        cv2.imshow("Webcam", frame)

    # Aguardar o pressionamento da tecla 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos utilizados
capture.release()
out.release()
cv2.destroyAllWindows()
