import cv2
import numpy as np

picture0 = cv2.imread("1.jpg")



#Converter RGB til HSV
cv2.COLOR_BGR2HSV



#for y, col in enumerate picture0:
    #for x, px in enumerate col:

for y in range(0, 100):
    for x in range(0, 100):
        print(f"pixel value at ({x}, {y}): {picture0[y,x]}")



cv2.waitKey(0)