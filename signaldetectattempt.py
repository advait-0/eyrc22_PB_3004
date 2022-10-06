import cv2
import numpy as np
img = cv2.imread('public_test_images/maze_0.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("hsv", hsv)
list=[]
# hsv format -> (min hue, min saturation , min value) -> (max hue, max saturation , max value)
# RED mask =>
# mask1 = cv2.inRange(hsv, (0, 100, 0), (10,255 ,255))



# BLUE mask =>
font = cv2.FONT_HERSHEY_SIMPLEX
mask = cv2.inRange(hsv, (0,50,50), (10, 255, 255))
cv2.imshow("mask", mask)
cont,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(img,cont,-1,(255,255,0),3)
for cnt in cont :
  
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
  
    # draws boundary of contours.
    cv2.drawContours(img, [approx], 0, (0, 255, 255), 2) 
  
    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = approx.ravel() 
    i = 0
    print(n)
    for i in range(0,len(n)):
        if(i%2==0):
            if(n[i]>90 and n[i]<180):
                char1="A"
            elif(n[i]>180 and n[i]<280):
                char1="B"
            elif(n[i]>280 and n[i]<380):
                char1="C"
            elif(n[i]>380 and n[i]<480):
                char1="D"
            elif(n[i]>480 and n[i]<580):
                char1="E"
            elif(n[i]>580 and n[i]<680):
                char1="F"
            elif(n[i]>680 and n[i]<780):
                char1="G"
        elif(i%3==0 and i>0):
            if(n[i]>90 and n[i]<180):
                char2="1"
            elif(n[i]>180 and n[i]<280):
                char2="2"
            elif(n[i]>280 and n[i]<380):
                char2="3"
            elif(n[i]>380 and n[i]<480):
                char2="4"
            elif(n[i]>480 and n[i]<580):
                char2="5"
            elif(n[i]>580 and n[i]<680):
                char2="6"
            elif(n[i]>680 and n[i]<780):
                char2="7"
    signal=char1+char2
    list.append(signal)
    
    list.sort()
    print(list)
    # for j in n :
    #     if(i % 2 == 0):
    #         x = n[i]
    #         y = n[i + 1]
  
    #         # String containing the co-ordinates.
    #         string = str(x) + " " + str(y) 
  
    #         if(i == 0):
    #             # text on topmost co-ordinate.
    #             cv2.putText(img, "Arrow tip", (x, y),
    #                             font, 0.5, (255, 0, 0)) 
    #         else:
    #             # text on remaining co-ordinates.
    #             cv2.putText(img, string, (x, y), 
    #                       font, 0.1, (0, 255, 0)) 
    #     i = i + 1
  
cv2.imshow("n",img)
## final mask and masked





cv2.waitKey(0)
cv2.destroyAllWindows()
