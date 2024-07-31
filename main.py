from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Ancho de la captura de video
cap.set(4, 720)   # Alto de la captura de video
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5053)

while True:
    # Obtener el marco de la imagen
    success, img = cap.read()
    # Encontrar la mano y sus puntos de referencia
    hands, img = detector.findHands(img)  # con dibujo
    # hands = detector.findHands(img, draw=False)  # sin dibujo
    data = []

    if hands:
        # Mano 1
        hand = hands[0]
        lmList = hand["lmList"]  # Lista de 21 puntos de referencia
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)

    # Redimensionar la imagen para que se muestre más pequeña
    # Redimensionar a la mitad (640x360)
    img_small = cv2.resize(img, (640, 360))

    # Mostrar la imagen redimensionada
    cv2.imshow("Image", img_small)
    cv2.waitKey(1)
