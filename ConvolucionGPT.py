from symbol import tfpdef

import cv2 as cv
import numpy as np
import time

img = cv.imread('/Users/alonsocortes/Downloads/bears.png',0)

img_array = np.array(img)

kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
])

img_height, img_width = img_array.shape
kernel_height, kernel_width = kernel.shape

pad_height = kernel_height // 2
pad_width = kernel_width // 2

padded_img = np.pad(img_array, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)

filtered_img = np.zeros_like(img_array)

Ti= time.time()

for i in range(img_height):
    for j in range(img_width):
        region = padded_img[i:i + kernel_height, j:j + kernel_width]
        filtered_value = np.sum(region * kernel)
        filtered_img[i, j] = min(max(filtered_value, 0), 255)

Tf = time.time()
T = Tf - Ti
print(T)
cv.imshow('Imagen Filtrada', filtered_img)

kernel_col2 = np.array([[1], [2], [1]])
kernel_row2 = np.array([[1, 2, 1]])
temp_img2 = np.zeros_like(img, dtype=np.float32)
filtered_img2 = np.zeros_like(img, dtype=np.uint8)
ti2 = time.time()
pad_height2 = kernel_col2.shape[0] // 2
padded_img2 = np.pad(img, ((pad_height, pad_height), (0, 0)), mode='constant', constant_values=0)


for i in range(img_height):
    for j in range(img_width):
        region = padded_img2[i:i + kernel_col2.shape[0], j]
        temp_img2[i, j] = np.sum(region * kernel_col2)

pad_width2 = kernel_row2.shape[1] // 2
padded_temp_img = np.pad(temp_img2, ((0, 0), (pad_width, pad_width)), mode='constant', constant_values=0)

for i in range(img_height):
    for j in range(img_width):
        region2 = padded_temp_img[i, j:j + kernel_row2.shape[1]]
        filtered_value2 = np.sum(region2 * kernel_row2)
        filtered_img2[i, j] = min(max(int(filtered_value2), 0), 255)
tf2 = time.time()
T2 = tf2 - ti2
print(T2)

cv.imshow('Imagen Original', img)
cv.imshow('Imagen Filtrada2', filtered_img2)
cv.waitKey(0)
cv.destroyAllWindows()