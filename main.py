import cv2
import numpy as np

picture0 = cv2.imread("1.jpg")
cropped_picture = picture0[0:100, 100:200]
cv2.imshow("Cropped image", cropped_picture)
cv2.imshow("original", picture0)

avg_col = np.average(cropped_picture, axis=0)
avg_color = np.average(avg_col, axis = 0)
print(f"avg_color: {avg_color}")


#Converter RGB til HSV
cv2.COLOR_BGR2HSV



#for y, col in enumerate picture0:
    #for x, px in enumerate col:

#for y in range(0, 100):
    #for x in range(0, 100):
        #print(f"pixel value at ({x}, {y}): {picture0[y,x]}")



cv2.waitKey(0)