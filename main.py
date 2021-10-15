import cv2
import numpy as np


picture0 = cv2.imread("1.jpg")
blurredPicture = cv2.GaussianBlur(picture0, (5, 5), 0)
picture1 = cv2.cvtColor(blurredPicture, cv2.COLOR_BGR2HSV) # Converts the first picture to HSV
maskMatrix = np.zeros((5, 5))



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
cv2.imshow("morph", morph_forest)

mask_list = [grass_mask, water_mask, morph_forest, sand_mask, desert_mask, crown_mask]


# iterate over each 100 pixel in and print out the average pixel value if its above or equal to 60
maskNumber = 0

for mask in mask_list:
    maskNumber = maskNumber + 1
    y1 = 0
    for y in range(0, 500, 100):
        y1 = y1 + 1
        x1 = 0
        for x in range(0, 500, 100):
            x1 = x1 + 1
            tile = mask[y: y + 100, x: x + 100]
            if np.average(tile) >= 60:
                print(f"{maskNumber}: {np.average(tile)}")
                maskMatrix[y1-1, x1-1] = maskNumber
#print(y1, x1)
print(maskMatrix)




#contours
while True:
#masks displayed on the screen
    cv2.imshow("grass", grass_mask)

    cv2.imshow("forest", forest_mask)
    cv2.imshow("sand", sand_mask)
    cv2.imshow("desert", desert_mask)
    cv2.imshow("crown", crown_mask)



    #add contours around the tiles, and apply a white line around the given tiles
    contours, hierarchy = cv2.findContours(water_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #for contour in contours: #prøver at kun tegne contours rundt om de store brikker
        #area = cv2.contourArea(contour)
        #if area > 5000:
            #cv2.drawContours(picture0, contour, -1, (255, 255, 255), 3)

    cv2.drawContours(picture0, contours, -1, (255, 255, 255), 3)
    cv2.imshow("water", water_mask)
    cv2.imshow("RGB", picture0)

    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()
