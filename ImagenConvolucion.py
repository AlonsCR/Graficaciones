import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('/Users/alonsocortes/Downloads/bears.png', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

imagen_filtrada = np.zeros((y, x), np.uint8)

# Definir el factor de escala
scale_x, scale_y =2,2

# Crear una nueva imagen para almacenar el escalado
scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)

# Aplicar el escalado
for i in range(int(x * scale_y)):
    for j in range(int(y * scale_x)):
        orig_x = int(i * scale_y)
        orig_y = int(j * scale_x)
        if 0 <= orig_x < x and 0 <= orig_y < y:
            scaled_img[i, j] = img[orig_x, orig_y]

for i in range(1, y - 1):
    for j in range(1, x - 1):
        ventana = img[i - 1:i + 2, j - 1:j + 2]


        r = np.sum(ventana) *(1/ 9)
        imagen_filtrada[i, j] = r

# Mostrar la imagen original y la escalada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Filtrada', imagen_filtrada)
cv.waitKey(0)
cv.destroyAllWindows()