import math
from collections import deque
import cv2
import numpy as np

picture = cv2.imread("Images/2.jpg", 0) #Change here to find the crowns in another photo!!
templateOriginal = cv2.imread("Images/EditedTemplateForcrown.png", 0)
templateRotate90 = cv2.rotate(cv2.imread("Images/EditedTemplateForcrown.png", 0), cv2.ROTATE_90_CLOCKWISE)
templateRotate180 = cv2.rotate(cv2.imread("Images/EditedTemplateForcrown.png", 0), cv2.ROTATE_180)
templateRotate270 = cv2.rotate(cv2.imread("Images/EditedTemplateForcrown.png", 0), cv2.ROTATE_90_COUNTERCLOCKWISE)
templateList = [templateOriginal, templateRotate90, templateRotate180, templateRotate270]
crownMatrix = np.zeros((5, 5), np.uint8)
w, h = templateOriginal.shape[::-1]

# res = cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED, mask = template)
threshold = 0.68 # Secures how accurate the template should be in comparisson with the picture. set to 80%
crownCoordinates = []
coordinatesAreClose = False
#loc = np.where(res >= threshold)
for template in templateList: #itererer over de fire retninger af konge kronen
    res = cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED) #comparer vores almindelige billede med vores template
    loc = np.where(res >= threshold) #returns the x and y coordinates where template has matched if they are above the treshold


    for pt in zip(*loc[::-1]):# we zip the x and y coordinates that we get from loc, and iterate over them
        cv2.rectangle(picture, pt, (pt[0] + w, pt[1] + h), (255,255,255), -1)#draw a square on each crown

        for [x, y] in crownCoordinates:#iterate over each coordinate in the list crownCoordinates
            coordinatesAreClose = False
            #if the coordinate of the tuple is close to any of the coordinates
            #in the list crownCoordinates, then dont append this coordinate in the list
            #this is to avoid that the same coordinates get appended, and we get a wrong count of crowns
            #if x and y coordinates are within 5 of the x and y in the tuple then coordinatesAreClose = True. This is what we use abs_tol for
            if(math.isclose(x, pt[0], abs_tol=5)) and (math.isclose(y, pt[1], abs_tol=5)):
                coordinatesAreClose = True
                break
            else:
                continue
        if coordinatesAreClose == False: #append the coordinates if they aren't close to any other coordinates.
            crownCoordinates.append(pt)
            crownMatrix[pt[1] // 100, pt[0] // 100] +=1 #increment the point in the matrix with the given coordinates with 1
print(crownMatrix)
cv2.imshow("game maps", picture)
cv2.imshow("template", templateOriginal)

cv2.waitKey(0)



