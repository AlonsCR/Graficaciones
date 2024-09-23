import math
import numpy as np
import cv2 as cv2

img = cv2.imread('/Users/alonsocortes/Downloads/unnamed.jpg',1)
height, width = img.shape[:2]  # Get the dimensions of the image
cx = width // 2  # Calculate the center of the width
cy = height // 2 # Calculate the center of the height
angle = -60
theta = math.radians(angle)
x,y = img.shape[:2]
rotated_img = np.zeros((height, width, img.shape[2]), dtype=img.dtype)  # Matriz vacía del mismo tamaño que la imagen original

for i in range(x):
    for j in range(y):
        new_x = ((int ((j-cx)*math.cos(theta)-(i-cy)*math.sin(theta)+cx))+10)*int(2)
        new_y = ((int ((j-cx)*math.sin(theta)+(i-cy)*math.cos(theta)+cy))+10)*int(2)
        #new_x = ((int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)) + 10) * int(2)
        #new_y = ((int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)) + 10) * int(2)
        if 0 <= new_x < y and 0 <= new_y < x:
            rotated_img[new_x,new_y] = img[i,j]
cv2.imshow('ejemplo',img)
cv2.imshow('rotacion',rotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#com