from collections import deque
import cv2
import numpy as np
import templateMatching


#read the first image, add blur and convert its colors to HSV
picture0 = cv2.imread("1.jpg")
blurredPicture = cv2.GaussianBlur(picture0, (5, 5), 0)
picture1 = cv2.cvtColor(blurredPicture, cv2.COLOR_BGR2HSV) # Converts the first picture to HSV
maskMatrix = np.zeros((5, 5), dtype=np.uint8) #lav en 5x5 tom matrice
#



#Ranges of the certain tiles within the game
grass_lowRange = np.array([35, 154, 140])
grass_upperRange = np.array([50, 249, 176])
water_lowRange = np.array([95, 175, 68])
water_upperRange = np.array([111, 255, 255])
forest_lowRange = np.array([30, 0, 0])
forest_upperRange = np.array([87, 255, 120])
sand_lowRange = np.array([22, 230, 181])
sand_upperRange = np.array([31, 255, 255])
desert_lowRange = np.array([0, 0, 50])
desert_upperRange = np.array([30, 255, 112])
crown_lowRange = np.array([0, 0, 151])
crown_upperRange = np.array([35, 217, 195])

#masks that cover the certain ranges of the tiles
grass_mask = cv2.inRange(picture1, grass_lowRange, grass_upperRange)
water_mask = cv2.inRange(picture1, water_lowRange, water_upperRange)
forest_mask = cv2.inRange(picture1, forest_lowRange, forest_upperRange)
sand_mask = cv2.inRange(picture1, sand_lowRange, sand_upperRange)
desert_mask = cv2.inRange(picture1, desert_lowRange, desert_upperRange)
crown_mask = cv2.inRange(picture1, crown_lowRange, crown_upperRange)

#morpher forest
kernel = np.ones((7, 7), np.uint8)
morph_forest = cv2.morphologyEx(forest_mask, cv2.MORPH_OPEN, kernel)

mask_list = [grass_mask, water_mask, morph_forest, sand_mask, desert_mask, crown_mask]
maskNumber = 0

#for mask in mask_list:
for maskNumber, mask in enumerate(mask_list, 1):
    y1 = 0
    for y in range(0, 500, 100):
        y1 = y1 + 1
        x1 = 0
        for x in range(0, 500, 100):
            x1 = x1 + 1
            tile = mask[y: y + 100, x: x + 100]
            if np.average(tile) >= 60:
                maskMatrix[y1-1, x1-1] = maskNumber


cv2.imshow("before", maskMatrix)
print(maskMatrix)

def grassFire (newMaskMatrix, coordinates, currentId, tileValue):
    #create burnedQueue deque to keep track of positions to burn
    burnedQueue = deque([])
    somethingBurned = False
    sizeOfBlob = 0
    crownCounter = 0

    if newMaskMatrix[coordinates[0], coordinates[1]] == tileValue:
        burnedQueue.append(coordinates)
        somethingBurned = True

    while len(burnedQueue) > 0:
        current_pos = burnedQueue.pop()
        y, x = current_pos
        if newMaskMatrix[y, x] == tileValue:
        # Burn current_pos with current id and increment current blobSize
            sizeOfBlob += 1
            newMaskMatrix[y, x] = currentId
            crownCounter += templateMatching.crownMatrix[y, x]


        # Add connections to burn_queue
        if (y - 1 >= 0) and (newMaskMatrix[y - 1, x] == tileValue):
            burnedQueue.append((y - 1, x))
        if (x - 1 >= 0) and (newMaskMatrix[y, x - 1] == tileValue):
            burnedQueue.append((y, x - 1))
        if (y + 1 < newMaskMatrix.shape[0]) and (newMaskMatrix[y + 1, x] == tileValue):
            burnedQueue.append((y + 1, x))
        if (x + 1 < newMaskMatrix.shape[1]) and (newMaskMatrix[y, x + 1] == tileValue):
            burnedQueue.append((y, x + 1))

    if somethingBurned:
        currentId += 10
    return currentId, newMaskMatrix, tileValue, sizeOfBlob, crownCounter

nextId = 10

totalScoreCount = 0
if maskMatrix[2, 2] == 6:
    totalScoreCount += 10
for i in range(7):
    for y, row in enumerate(maskMatrix):
        for x, pixel in enumerate(row):
            nextId, maskMatrix, tileValue, blobSize, crownCount = grassFire(maskMatrix, (y, x), nextId, i)
            totalScoreCount += blobSize * crownCount
            if blobSize > 0:
                print("tileValue with number:", tileValue, "has the size of", blobSize, crownCount, "Score is:", totalScoreCount)





while True:
    cv2.imshow("mask", maskMatrix)
    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()
