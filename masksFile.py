import cv2
import numpy as np


picture0 = cv2.imread("1.jpg")
blurredPicture = cv2.GaussianBlur(picture0, (5, 5), 0)
picture1 = cv2.cvtColor(blurredPicture, cv2.COLOR_BGR2HSV) # Converts the first picture to HSV
maskMatrix = np.zeros((5, 5))
print(maskMatrix)

class TileType:

    def getGras(self):
        grass_lowRange = np.array([35, 154, 140])
        grass_upperRange = np.array([50, 249, 176])
        grass_mask = cv2.inRange(picture1, grass_lowRange, grass_upperRange)
        return 0
    def getWater(self):
        water_lowRange = np.array([95, 175, 68])
        water_upperRange = np.array([111, 255, 255])
        water_mask = cv2.inRange(picture1, water_lowRange, water_upperRange)
        return 1

    def getForest(self):
        forest_lowRange = np.array([30, 0, 0])
        forest_upperRange = np.array([87, 255, 120])
        forest_mask = cv2.inRange(picture1, forest_lowRange, forest_upperRange)
        kernel = np.ones((7, 7), np.uint8)
        morph_forest = cv2.morphologyEx(forest_mask, cv2.MORPH_OPEN, kernel)
        return 2

    def getSand(self):
        sand_lowRange = np.array([22, 230, 181])
        sand_upperRange = np.array([31, 255, 255])
        sand_mask = cv2.inRange(picture1, sand_lowRange, sand_upperRange)
        return 3

    def getDesert(self):
        desert_lowRange = np.array([0, 0, 50])
        desert_upperRange = np.array([30, 255, 112])
        desert_mask = cv2.inRange(picture1, desert_lowRange, desert_upperRange)
        return 4

    def getCrown(self):
        crown_lowRange = np.array([0, 0, 151])
        crown_upperRange = np.array([35, 217, 195])
        crown_mask = cv2.inRange(picture1, crown_lowRange, crown_upperRange)
        return 5


currentTile = TileType()


mask_list = [currentTile.getGras().water_mask, currentTile.getWater(), currentTile.getForest(), currentTile.getSand(), currentTile.getDesert(), currentTile.getCrown()]


counter = 0  # Variable for counting means

for i in mask_list:
    for y in range(0, 500, 100):
        for x in range(0, 500, 100):
            tile = i[y: y + 100, x: x + 100]
            if np.average(tile) >= 60:
                print(f"{counter}: {np.average(tile)}")
                counter += 1


while True:
    contours, hierarchy = cv2.findContours(currentTile.getWater(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(picture0, contours, -1, (255, 255, 255), 3)
    cv2.imshow("water", currentTile.getWater())
    cv2.imshow("RGB", picture0)

    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()

cropped_picture = grass_mask[0:100, 0:100]
cv2.imshow("Cropped", cropped_picture)

avg_col = np.average(cropped_picture, axis=None)
avg_color = np.average(avg_col, axis = None)
print(f"avg_color: {avg_color}")

