from collections import deque
import cv2
import numpy as np
import templateMatching


'''
Below the first picture is read, blurred through Gaussian blur and converted to HSV colors.
In addition we create an empty 5x5 matrix, which is used later on to perform the Grassfire algorithm.
'''
inputPicture = cv2.imread("Images/1.jpg")
blurredPicture = cv2.GaussianBlur(inputPicture, (5, 5), 0)
HSVPicture = cv2.cvtColor(blurredPicture, cv2.COLOR_BGR2HSV)





'''
Below we define the lower and upper-range HSV values to the their associated tile eg. grass, forest etc.
'''
grassLowRange = np.array([35, 154, 140])
grassUpperRange = np.array([50, 249, 176])
waterLowRange = np.array([95, 175, 68])
waterUpperRange = np.array([111, 255, 255])
forestLowRange = np.array([36, 41, 0])
forestUpperRange = np.array([64, 255, 139])
sandLowRange = np.array([22, 230, 181])
sandUpperRange = np.array([31, 255, 255])
desertLowRange = np.array([0, 74, 65])
desertUpperRange = np.array([30, 150, 130])
mineLowerRange = np.array([0, 0, 0])
mineUpperRange = np.array([20, 88, 61])
crownLowRange = np.array([0, 0, 85])
crownUpperRange = np.array([28, 91, 243])





'''
Below we define a mask for each tile matching their HSV values.
'''
grassMask = cv2.inRange(HSVPicture, grassLowRange, grassUpperRange)
waterMask = cv2.inRange(HSVPicture, waterLowRange, waterUpperRange)
forestMask = cv2.inRange(HSVPicture, forestLowRange, forestUpperRange)
sandMask = cv2.inRange(HSVPicture, sandLowRange, sandUpperRange)
desertMask = cv2.inRange(HSVPicture, desertLowRange, desertUpperRange)
mineMask = cv2.inRange(HSVPicture, mineLowerRange, mineUpperRange)
crownMask = cv2.inRange(HSVPicture, crownLowRange, crownUpperRange)




'''
We decided to apply morphology to the various tiles in order to reduce noise.
First we created a kernel with the size of 7x7 , and applied compound operations to reduce noise
surrounding the different masks. The compound operations(Open & close) are chosen by how each tile type has different
noisy elements in their design, such as houses, boats etc. Some of the masks have been morphed twice, 
to further reduce noise
'''
kernel = np.ones((7, 7), np.uint8)
morphedGrassMask = cv2.morphologyEx(grassMask, cv2.MORPH_CLOSE, kernel)
morphedWaterMask = cv2.morphologyEx(waterMask, cv2.MORPH_CLOSE, kernel)
morphedForestMask = cv2.morphologyEx(forestMask, cv2.MORPH_OPEN, kernel)
morphedSandMask = cv2.morphologyEx(sandMask, cv2.MORPH_CLOSE, kernel)
morphedDesertMask = cv2.morphologyEx(desertMask, cv2.MORPH_CLOSE, kernel)
morphedMineMask = cv2.morphologyEx(mineMask, cv2.MORPH_CLOSE, kernel)
morphedCrownMask = cv2.morphologyEx(crownMask, cv2.MORPH_OPEN, kernel)
morphedCrownMask2 = cv2.morphologyEx(morphedCrownMask, cv2.MORPH_CLOSE, kernel)



'''
Below we have three for loops. The first for loop iterates over each mask from mask list. 
We then go through each tile in the mask(increase y and x with 100, every iteration) and calculate an average
bgr value within that range. If the average bgr value is higher than 70 we implement the current mask number 
into the matrix at those coordinates, in the matrix called maskMatrix
When the loop is done, it prints the matrix with matching tile-type in the picture, ranging from 1 to 7
'''
maskMatrix = np.zeros((5, 5), dtype=np.uint8)
maskList = [morphedGrassMask, morphedWaterMask, morphedForestMask, morphedSandMask, morphedDesertMask, morphedCrownMask2, morphedMineMask]
maskNumber = 0
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
print(maskMatrix)



def grassFire (newMaskMatrix, coordinates, currentId, tileValue):
    #we create a deque to append the coordinates we have burned
    #and create variables for keeping track of blobsize and crowns
    burnedQueue = deque([])
    sizeOfBlob = 0
    crownCounter = 0
    burned = False

    #if the coordinate is equal to the current tilevalue, we append those coordinates to the deque
    if newMaskMatrix[coordinates[0], coordinates[1]] == tileValue:
        burnedQueue.append(coordinates)
        burned = True

    while len(burnedQueue) > 0:
        currentPosition = burnedQueue.pop()
        y, x = currentPosition
        if newMaskMatrix[y, x] == tileValue:
        # Burn currentPosition with currentId and increment current blobSize and crowncounter
            sizeOfBlob += 1
            newMaskMatrix[y, x] = currentId
            crownCounter += templateMatching.crownMatrix[y, x]


        # check if the surroundings of the current coordinate has the same tilevalue
        if (y - 1 >= 0) and (newMaskMatrix[y - 1, x] == tileValue):
            burnedQueue.append((y - 1, x))
        if (x - 1 >= 0) and (newMaskMatrix[y, x - 1] == tileValue):
            burnedQueue.append((y, x - 1))
        if (y + 1 < newMaskMatrix.shape[0]) and (newMaskMatrix[y + 1, x] == tileValue):
            burnedQueue.append((y + 1, x))
        if (x + 1 < newMaskMatrix.shape[1]) and (newMaskMatrix[y, x + 1] == tileValue):
            burnedQueue.append((y, x + 1))
    #increment currentId with 10, after the blob has been located, to avoid reading the same blob again next time
    if burned:
        currentId += 10
    return currentId, newMaskMatrix, tileValue, sizeOfBlob, crownCounter

nextId = 10
totalScoreCount = 0
'''
if the middle tile has a crown in it(crown tile is number 6), we add 10 to the final score.
the reason why we also say if maskmatrix[2,2] == 0 is because we don't have a mask for the crown tiles where there is
a castle brick placed over it, and since we don't have a mask for that tile, the algorithm sets it to 0 
'''
if maskMatrix[2, 2] == 6 or maskMatrix[2, 2] == 0:
    totalScoreCount += 10

'''
We start with a for loop looping from 0 to 8. We start by looking for blobs which have a tileValue of 0, then 1, 
and so on. We iterate through each coordinate with the grassFire algorithm on the maskMatrix.
After each blob has been accounted for we take their size and multiply it with how many crowns were on that blob
as well and add that to the totalScore, which we print out lastly.

'''
for i in range(8):
    for y, row in enumerate(maskMatrix):
        for x, pixel in enumerate(row):
            nextId, maskMatrix, tileValue, blobSize, crownCount = grassFire(maskMatrix, (y, x), nextId, i)
            totalScoreCount += blobSize * crownCount
            if blobSize > 0:
                print("tileValue with number:", tileValue, "has the size of", blobSize, "\n",
                      "number of crowns on current tile:", crownCount, "Current score:", totalScoreCount, "\n")

print("Total score is:", totalScoreCount)







while True:
    cv2.imshow("Input picture", inputPicture)
    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()
