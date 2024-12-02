import numpy as np
import cv2 as cv

# Cargar la imagen para superponer y redimensionarla
overlay_image = cv.imread('/Users/alonsocortes/Downloads/Chicago-Bears-Logo.png', cv.IMREAD_UNCHANGED)

if overlay_image is None:
    print("Error: ¡No se pudo cargar la imagen!")
    exit()

# Reducir el tamaño original de la imagen al 50%
overlay_image = cv.resize(overlay_image, (overlay_image.shape[1] // 2, overlay_image.shape[0] // 2), interpolation=cv.INTER_AREA)

# Iniciar la captura de video desde la cámara
cap = cv.VideoCapture(0)

# Parámetros para el flujo óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer camara
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Posición inicial de la bola
ball_pos = np.array([[550, 500]], dtype=np.float32)
ball_pos = ball_pos[:, np.newaxis, :]

# Punto fijo para la imagen
fixed_point = (1500, 700)

# Ángulo inicial de rotación
rotation_angle = 0

while True:
    # Capturar el siguiente frame
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico para mover la bola
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    # Si se detecta el nuevo movimiento, actualizar la posición de la bola
    if new_ball_pos is not None:
        ball_pos = new_ball_pos
        a, b = ball_pos.ravel()
        frame = cv.circle(frame, (int(a), int(b)), 20, (120, 255, 0), -1)

        # Calcular el tamaño de la imagen superpuesta según el movimiento horizontal
        dist_from_center = np.linalg.norm(np.array([a, b]) - np.array([frame.shape[1] / 2, frame.shape[0] / 2]))
        scale_factor = max(0.5, min(2.0, 1.5 - dist_from_center / 400))  # Escalar según la distancia
        new_width = int(overlay_image.shape[1] * scale_factor)
        new_height = int(overlay_image.shape[0] * scale_factor)
        resized_image = cv.resize(overlay_image, (new_width, new_height), interpolation=cv.INTER_AREA)

        # Rotar la imagen según el movimiento vertical
        delta_y = b - frame.shape[0] / 2
        rotation_angle = int(max(-180, min(180, delta_y / 10)))  # Ángulo entre -90 y 90 grados  # Ángulo entre -45 y 45 grados

        # Crear la matriz de rotación
        center = (resized_image.shape[1] // 2, resized_image.shape[0] // 2)
        rotation_matrix = cv.getRotationMatrix2D(center, rotation_angle, 1)
        rotated_image = cv.warpAffine(resized_image, rotation_matrix, (resized_image.shape[1], resized_image.shape[0]),
                                       flags=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

        x_offset = fixed_point[0] - new_width // 2
        y_offset = fixed_point[1] - new_height // 2
        x1, x2 = max(x_offset, 0), min(x_offset + new_width, frame.shape[1])
        y1, y2 = max(y_offset, 0), min(y_offset + new_height, frame.shape[0])
        overlay_x1, overlay_x2 = max(0, -x_offset), min(new_width, frame.shape[1] - x_offset)
        overlay_y1, overlay_y2 = max(0, -y_offset), min(new_height, frame.shape[0] - y_offset)

        alpha_channel = rotated_image[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
        for c in range(3):
            frame[y1:y2, x1:x2, c] = (alpha_channel * rotated_image[overlay_y1:overlay_y2, overlay_x1:overlay_x2, c] +
                                      (1 - alpha_channel) * frame[y1:y2, x1:x2, c])

    cv.imshow('Da Bears', frame)

    prev_gray = gray_frame.copy()

    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()