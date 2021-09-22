import cv2
import numpy as np

picture0 = cv2.imread("1.jpg")
picture1 = cv2.cvtColor(picture0, cv2.COLOR_BGR2HSV)
cropped_picture = picture1[0:100, 0:100]


cv2.imshow("RGB", picture0)
cv2.imshow("HSV", picture1)

lower_range = np.array([35, 154, 140])
upper_range = np.array([50, 249, 176])



mask = cv2.inRange(picture1, lower_range, upper_range)
cropped_picture = mask[0:100, 0:100]
cv2.imshow("Cropped", cropped_picture)
cv2.imshow("Grass Tiles", mask)
#cv2.imshow("Cropped image", cropped_picture)
#cv2.imshow("original", picture0)




#average RGB i croppede billede
avg_col = np.average(cropped_picture, axis=None)
avg_color = np.average(avg_col, axis = None)
print(f"avg_color: {avg_color}")

#En prøve i at convertere billedet til HSV og så ændre V værdien
#picture1 = cv2.imread("1.jpg")
#picture1hsv = cv2.cvtColor(picture1, cv2.COLOR_BGR2HSV)
#mask = cv2.inRange(picture1hsv,(0, 0, 0), (180, 255, 255))
#cv2.imshow("picture1", mask)

#Converter RGB til HSV
#cv2.COLOR_BGR2HSV





#for y, col in enumerate picture0:
    #for x, px in enumerate col:

#for y in range(0, 100):
    #for x in range(0, 100):
        #print(f"pixel value at ({x}, {y}): {picture0[y,x]}")



cv2.waitKey(0)
cv2.destroyAllWindows()
