import cv2
import pickle
import cvzone
import numpy as np

# Carregar o vídeo
video = cv2.VideoCapture('carPark.mp4')

# Tamanho da região de interesse (ROI)
width, height = 107, 48

# Função para verificar as vagas de estacionamento
def checkParkSpace(imgPro):
    for pos in posList:
        x, y = pos

        # Recortar a região de interesse (ROI)
        imgCrop = imgPro[y:y + height, x:x + width]

        # Contar os pixels brancos na ROI
        count = cv2.countNonZero(imgCrop)

        # Exibir o número de pixels brancos sobre a vaga
        cvzone.putTextRect(frame, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=(0,0,255))

        # Determinar a cor do retângulo com base na contagem de pixels
        if count < 800:
            color = (0, 255, 0)  # Verde
            thickness = 5
        else:
            color = (0, 0, 255)  # Vermelho
            thickness = 2

        # Desenhar um retângulo ao redor da vaga
        cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, thickness)

# Carregar as posições das vagas de estacionamento a partir de um arquivo pickle
with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    # Ler o próximo quadro do vídeo
    success, frame = video.read()

    # Verificar se o vídeo chegou ao final e reiniciar, se necessário
    if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Converter o quadro para tons de cinza
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar um desfoque Gaussiano
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # Aplicar threshold adaptativo
    imgTreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Aplicar um desfoque mediano
    imgMedian = cv2.medianBlur(imgTreshold, 5)

    # Aplicar dilatação para melhorar a detecção de bordas
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Verificar as vagas de estacionamento
    checkParkSpace(imgDilate)

    # Exibir o quadro resultante com as marcações das vagas
    cv2.imshow('Image', frame)

    # Encerrar o programa se a tecla 'f' for pressionada
    if cv2.waitKey(10) == ord('f'):
        break
