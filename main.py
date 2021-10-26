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



'''
Below we define the lower and upper-range HSV values to the their associated tile eg. grass etc.
'''
grassLowRange = np.array([35, 154, 140])
grassUpperRange = np.array([50, 249, 176])
waterLowRange = np.array([95, 175, 68])
waterUpperRange = np.array([111, 255, 255])
forestLowRange = np.array([30, 0, 0])
forestUpperRange = np.array([87, 255, 120])
sandLowRange = np.array([22, 230, 181])
sandUpperRange = np.array([31, 255, 255])
desertLowRange = np.array([0, 0, 50])
desertUpperRange = np.array([30, 255, 112])
mineLowerRange = np.array([0, 0, 0])
mineUpperRange = np.array([20, 88, 61])
crownLowRange = np.array([0, 0, 85])
crownUpperRange = np.array([28, 91, 243])




'''
Below we define a mask for each tile matching their HSV values.
'''
grassMask = cv2.inRange(picture1, grassLowRange, grassUpperRange)
waterMask = cv2.inRange(picture1, waterLowRange, waterUpperRange)
forestMask = cv2.inRange(picture1, forestLowRange, forestUpperRange)
sandMask = cv2.inRange(picture1, sandLowRange, sandUpperRange)
desertMask = cv2.inRange(picture1, desertLowRange, desertUpperRange)
mineMask = cv2.inRange(picture1, mineLowerRange, mineUpperRange)
crownMask = cv2.inRange(picture1, crownLowRange, crownUpperRange)



'''
We decided to apply morphology to the forest tile in order to reduce noise, since the forest tile had the most noise
compared to the neighbour tiles.
First we created a kernel with the size of 7x7 , and applied a compound operation(Opening) to reduce noise
sourrounding the forest masks.  
'''
kernel = np.ones((7, 7), np.uint8)
morphForest = cv2.morphologyEx(forestMask, cv2.MORPH_OPEN, kernel)
morphMine = cv2.morphologyEx(mineMask, cv2.MORPH_CLOSE, kernel)
morphDesert = cv2.morphologyEx(desertMask, cv2.MORPH_OPEN, kernel)
morphSand = cv2.morphologyEx(sandMask, cv2.MORPH_CLOSE, kernel)


'''
Below we have three for loops. The first for loop iterates over each mask from mask list. 
We then go through each tile in the mask(increase y and x with 100, every iteration and calculate an average
bgr value. If the average bgr value is higher than 60 we implement the current mask number into the matrix
called maskMatrix)
When the loop is done, it prints the matrix with matching tile-type in the picture, ranging from 1 to 6
'''
maskList = [grassMask, waterMask, morphForest, morphSand, desertMask, crownMask, morphMine]
maskNumber = 0
#for mask in maskList:
for maskNumber, mask in enumerate(maskList, 1):
    y1 = 0
    for y in range(0, 500, 100):
        y1 = y1 + 1
        x1 = 0
        for x in range(0, 500, 100):
            x1 = x1 + 1
            tile = mask[y: y + 100, x: x + 100]
            if np.average(tile) >= 70:
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
        currentPosition = burnedQueue.pop()
        y, x = currentPosition
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
for i in range(8):
    for y, row in enumerate(maskMatrix):
        for x, pixel in enumerate(row):
            nextId, maskMatrix, tileValue, blobSize, crownCount = grassFire(maskMatrix, (y, x), nextId, i)
            totalScoreCount += blobSize * crownCount
            if blobSize > 0:
                print("tileValue with number:", tileValue, "has the size of", blobSize, crownCount, "Score is:", totalScoreCount)





while True:
    cv2.imshow("mine", mineMask)
    cv2.imshow("morphMine", morphMine)
    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()
