import cv2
import numpy as np

picture0 = cv2.imread("1.jpg")
blurredPicture = cv2.GaussianBlur(picture0, (5, 5), 0)
picture1 = cv2.cvtColor(blurredPicture, cv2.COLOR_BGR2HSV) # Converts the first picture to HSV

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

kernel = np.ones((7, 7), np.uint8)
morph_grass = cv2.morphologyEx(forest_mask, cv2.MORPH_OPEN, kernel)
cv2.imshow("morph", morph_grass)

mask_list = [grass_mask, water_mask, forest_mask, sand_mask , desert_mask, crown_mask]

#iterate over each 100 pixel in and print out the average pixel value if its above or equal to 50
counter = 0 # Variable for counting means
for y in range(0, 500, 100):
    for x in range(0, 500, 100):
        for mask in mask_list:
            tile = mask[y: y+100, x: x+100]
            if np.average(tile) >= 60:
                counter += 1
                print(f"Mean {counter}: {np.average(tile)}")








while True:
    #add contours around the tiles, and apply a white line around the given tiles
    contours,hierarchy = cv2.findContours(water_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #for contour in contours: #prøver at kun tegne contours rundt om de store brikker
        #area = cv2.contourArea(contour)
        #if area > 5000:
            #cv2.drawContours(picture0, contour, -1, (255, 255, 255), 3)

    cv2.drawContours(picture1, contours, -1, (255, 255, 255), 3)
    cv2.imshow("grass", grass_mask)
    cv2.imshow("water", water_mask)
    cv2.imshow("sand", sand_mask)
    cv2.imshow("HSV", picture1)
    cv2.imshow("forest", forest_mask)
            #avg_col = np.average(picture1, axis=None)
            #avg_color = np.average(avg_col, axis=None)
            #print(f"avg_color: {avg_color}")

    key = cv2.waitKey(1) #when the user presses esc key, the program shuts down
    if key == 27:
        break
cv2.destroyAllWindows()


cropped_picture = grass_mask[0:100, 0:100]
cv2.imshow("Cropped", cropped_picture)
#cv2.imshow("Cropped image", cropped_picture)q
#cv2.imshow("original", picture0)

#for y in 100(picture1):
 #   for x in 100(picture1):




#average RGB i croppede billede
#avg_col = np.average(cropped_picture, axis=None)
#avg_color = np.average(avg_col, axis = None)
#print(f"avg_color: {avg_color}")

#for y, row in enumerate (picture0): #med enumerate får vi også koordinaterne med
    #for x, pixel in enumerate (row):

#for y in range(0, 100):
    #for x in range(0, 100):
        #print(f"pixel value at ({x}, {y}): {picture0[y,x]}")




