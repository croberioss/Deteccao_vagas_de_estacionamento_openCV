import cv2
import pickle

# Tamanho da região de interesse (ROI)
width, height = 107, 48

# Tente carregar as posições das vagas de estacionamento de um arquivo pickle
try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []  # Se o arquivo não existe, crie uma lista vazia para as posições das vagas

# Função de callback de mouse para adicionar ou remover posições das vagas
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))  # Adicionar posição ao clicar com o botão esquerdo do mouse
    
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            # Remover posição se o botão direito do mouse for clicado dentro de uma vaga
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Salvar a lista de posições das vagas em um arquivo pickle
    with open('carParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    # Carregar uma imagem de um estacionamento
    img = cv2.imread('carParking.png')

    # Desenhar retângulos nas posições das vagas
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 30), 2)  # Cor e espessura do retângulo

    # Exibir a imagem com as marcações das vagas
    cv2.imshow("Image", img)

    # Configurar o callback do mouse para adicionar ou remover posições das vagas
    cv2.setMouseCallback("Image", mouseClick)

    # Encerrar o programa se a tecla 'f' for pressionada
    if cv2.waitKey(1) == ord('f'):
        break

# Exibir as posições das vagas após a interação do usuário
print(posList)
