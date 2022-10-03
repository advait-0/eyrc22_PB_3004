import cv2
import numpy as np
img = cv2.imread('public_test_images/maze_1.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv", hsv)

# hsv format -> (min hue, min saturation , min value) -> (max hue, max saturation , max value)
# RED mask =>
# mask1 = cv2.inRange(hsv, (0, 100, 0), (10,255 ,255))



# BLUE mask =>
mask = cv2.inRange(hsv, (0,50,50), (10, 255, 255))
cv2.imshow("mask", mask)

## final mask and masked





cv2.waitKey(0)
cv2.destroyAllWindows()
