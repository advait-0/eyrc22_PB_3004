import cv2
import numpy as np
img = cv2.imread('public_test_images/maze_0.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
corners=cv2.goodFeaturesToTrack(gray,50,0.1, 70)
corners=np.int0(corners)

for corner in corners:
    x,y =corner.ravel()
    cv2.circle(img,(x,y),5, (0,255,0), -1)
cv2.imshow('Frame',img)
cv2.waitKey(0)
