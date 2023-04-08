'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 3004 ]
# Author List:		[ Advait Dhamorikar ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_traffic_signals(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals` : [ list ]
            list containing nodes in which traffic signals are present
    
    Example call:
    ---
    traffic_signals = detect_traffic_signals(maze_image)
    """    
    traffic_signals = []

    ##############	ADD YOUR CODE HERE	##############
    img = maze_image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv", hsv)
    list=[]
    # hsv format -> (min hue, min saturation , min value) -> (max hue, max saturation , max value)
    # RED mask =>
    # mask1 = cv2.inRange(hsv, (0, 100, 0), (10,255 ,255))



    # BLUE mask =>
    # font = cv2.FONT_HERSHEY_SIMPLEX
    mask = cv2.inRange(hsv, (0,50,50), (10, 255, 255))
    # cv2.imshow("mask", mask)
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
                # print(n)
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
                traffic_signals=list
    ##################################################
    
    return traffic_signals
    

def detect_horizontal_roads_under_construction(maze_image):
    
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing horizontal links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `horizontal_roads_under_construction` : [ list ]
            list containing missing horizontal links
    
    Example call:
    ---
    horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
    """    
    horizontal_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############
    img = maze_image
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("img", img)
    list=[]
    horizontal_roads_under_construction=[]
    vertical_roads_under_construction=[]
    # road=""
    rot1 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    rot2 = cv2.rotate(rot1, cv2.ROTATE_90_CLOCKWISE)
    rot3 = cv2.rotate(rot2, cv2.ROTATE_90_CLOCKWISE)
    p1=cv2.bitwise_and(img,rot1)
    p2=cv2.bitwise_and(p1,rot2)
    p3=cv2.bitwise_and(p2,rot3)
    # cv2.imshow('rot',p3)
    white_lower=np.array([253,253,253])
    white_higher=np.array([255,255,255])
    blue_lower=np.array([0,0,253])
    blue_higher=np.array([0,0,255])
    red_lower=np.array([253,0,0])
    red_higher=np.array([255,0,0])
    green_lower=np.array([0,253,0])
    green_higher=np.array([0,255,0])
    mask1 = cv2.inRange(p3, white_lower, white_higher)
    # mask2 = cv2.inRange(p3, red_lower, red_higher)
    # mask3 = cv2.inRange(p3, green_lower, green_higher)
    # mask = mask1 | mask2 | mask3
    target = cv2.bitwise_and(p3,p3, mask=mask1)
    # cv2.imshow("target", target)
    tp=cv2.bitwise_xor(target,img)

    kernel = np.ones((5, 5), np.uint8)

    # Using cv2.erode() method 
    image = cv2.erode(tp, kernel) 
    # cv2.imshow("eroded",image)

    # subt=cv2.absdiff(img,tp)
    # cv2.imshow("sub",subt)
    # hsv format -> (min hue, min saturation , min value) -> (max hue, max saturation , max value)
    # RED mask =>
    # mask1 = cv2.inRange(hsv, (0, 100, 0), (10,255 ,255))

    # blue_lower=np.array([0,0,253])
    # blue_higher=np.array([0,0,255])
    # red_lower=np.array([253,0,0])
    # red_higher=np.array([255,0,0])
    # green_lower=np.array([0,253,0])
    # green_higher=np.array([0,255,0])
    # # BLUE mask =>
    # font = cv2.FONT_HERSHEY_SIMPLEX
    mask1 = cv2.inRange(image, white_lower, white_higher)
    mask2 = cv2.inRange(image, red_lower, red_higher)
    mask3 = cv2.inRange(image, green_lower, green_higher)
    mask = mask1 | mask2 | mask3
    gandalf = cv2.bitwise_and(image,image, mask=mask1)
    xrect=[]
    yrect=[]
    horiz_road=[]
    vert_road=[]
    temp=[]
    # # cv2.imshow("mas",mask)




    imgGrey = cv2.cvtColor(gandalf, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4:
            # print(approx.ravel())


            xrect.append(x)
            yrect.append(y)
            x1 ,y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            # print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                pass
            else: 
                cv2.drawContours(gandalf, [approx], 0, (100, 100, 75), 5)
                temp=approx.ravel()
                xcoor=abs(temp[4]-temp[0])
                ycoor=abs(temp[5]-temp[1])
                if(xcoor>ycoor):
                   horiz_road.append(temp)
                else:
                   vert_road.append(temp)

    # print(horiz_road,"\n")
    # print(vert_road)
    for i in range(0,len(horiz_road)):
        len_road=abs(horiz_road[i][0]-horiz_road[i][4])
        if(len_road>30):
             if(horiz_road[i][0]>95 and horiz_road[i][0]<190):
                 road="A-B"
             elif(horiz_road[i][0]>=190 and horiz_road[i][0]<290):
                 road="B-C"
             elif(horiz_road[i][0]>=290 and horiz_road[i][0]<390):
                 road="C-D"
             elif(horiz_road[i][0]>=390 and horiz_road[i][0]<490):
                 road="D-E"
             elif(horiz_road[i][0]>=490 and horiz_road[i][0]<590):
                 road="E-F"
             elif(horiz_road[i][0]>=590 and horiz_road[i][0]<690):
                 road="F-G"
            #  print(road)

             if(horiz_road[i][1]>95 and horiz_road[i][1]<190):
                 way1=road[:1]+"1"+road[1:]+"1"
             elif(horiz_road[i][1]>=190 and horiz_road[i][1]<290):
                 way1=road[:1]+"2"+road[1:]+"2"
             elif(horiz_road[i][1]>=290 and horiz_road[i][1]<390):
                way1=road[:1]+"3"+road[1:]+"3"
             elif(horiz_road[i][1]>=390 and horiz_road[i][1]<490):
                 way1=road[:1]+"4"+road[1:]+"4"
             elif(horiz_road[i][1]>=490 and horiz_road[i][1]<590):
                 way1=road[:1]+"5"+road[1:]+"5"
             elif(horiz_road[i][1]>=590 and horiz_road[i][1]<690):
                 way1=road[:1]+"6"+road[1:]+"6"
             elif(horiz_road[i][1]>=690 and horiz_road[i][1]<790):
                 way1=road[:1]+"7"+road[1:]+"7"
            #  print(way1)
             horizontal_roads_under_construction.append(way1)
             horizontal_roads_under_construction = [*set(horizontal_roads_under_construction)]
             horizontal_roads_under_construction.sort()

    # print(horizontal_roads_under_construction)
    ##################################################
    
    return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links
    
    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """    
    vertical_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############
    img = maze_image
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("img", img)
    list=[]
    # horizontal_roads_under_construction=[]
    vertical_roads_under_construction=[]
    # road=""
    rot1 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    rot2 = cv2.rotate(rot1, cv2.ROTATE_90_CLOCKWISE)
    rot3 = cv2.rotate(rot2, cv2.ROTATE_90_CLOCKWISE)
    p1=cv2.bitwise_and(img,rot1)
    p2=cv2.bitwise_and(p1,rot2)
    p3=cv2.bitwise_and(p2,rot3)
    # cv2.imshow('rot',p3)
    white_lower=np.array([253,253,253])
    white_higher=np.array([255,255,255])
    blue_lower=np.array([0,0,253])
    blue_higher=np.array([0,0,255])
    red_lower=np.array([253,0,0])
    red_higher=np.array([255,0,0])
    green_lower=np.array([0,253,0])
    green_higher=np.array([0,255,0])
    mask1 = cv2.inRange(p3, white_lower, white_higher)
    # mask2 = cv2.inRange(p3, red_lower, red_higher)
    # mask3 = cv2.inRange(p3, green_lower, green_higher)
    # mask = mask1 | mask2 | mask3
    target = cv2.bitwise_and(p3,p3, mask=mask1)
    # cv2.imshow("target", target)
    tp=cv2.bitwise_xor(target,img)

    kernel = np.ones((5, 5), np.uint8)

    # Using cv2.erode() method 
    image = cv2.erode(tp, kernel) 
    # cv2.imshow("eroded",image)

    # subt=cv2.absdiff(img,tp)
    # cv2.imshow("sub",subt)
    # hsv format -> (min hue, min saturation , min value) -> (max hue, max saturation , max value)
    # RED mask =>
    # mask1 = cv2.inRange(hsv, (0, 100, 0), (10,255 ,255))

    # blue_lower=np.array([0,0,253])
    # blue_higher=np.array([0,0,255])
    # red_lower=np.array([253,0,0])
    # red_higher=np.array([255,0,0])
    # green_lower=np.array([0,253,0])
    # green_higher=np.array([0,255,0])
    # # BLUE mask =>
    # font = cv2.FONT_HERSHEY_SIMPLEX
    mask1 = cv2.inRange(image, white_lower, white_higher)
    mask2 = cv2.inRange(image, red_lower, red_higher)
    mask3 = cv2.inRange(image, green_lower, green_higher)
    mask = mask1 | mask2 | mask3
    gandalf = cv2.bitwise_and(image,image, mask=mask1)
    xrect=[]
    yrect=[]
    horiz_road=[]
    vert_road=[]
    temp=[]
    # # cv2.imshow("mas",mask)




    imgGrey = cv2.cvtColor(gandalf, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4:
            # print(approx.ravel())


            xrect.append(x)
            yrect.append(y)
            x1 ,y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            # print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                pass
            else: 
                cv2.drawContours(gandalf, [approx], 0, (100, 100, 75), 5)
                temp=approx.ravel()
                xcoor=abs(temp[4]-temp[0])
                ycoor=abs(temp[5]-temp[1])
                if(xcoor>ycoor):
                   horiz_road.append(temp)
                else:
                   vert_road.append(temp)

    # print(horiz_road,"\n")
    # print(vert_road)
    for i in range(0,len(vert_road)):
        len_road=abs(vert_road[i][1]-vert_road[i][3])
        # print(len_road)
        if(len_road>30):
             if(vert_road[i][1]>85 and vert_road[i][1]<190):
                 road="1-2"
             elif(vert_road[i][1]>=190 and vert_road[i][1]<290):
                 road="2-3"
             elif(vert_road[i][1]>=290 and vert_road[i][1]<390):
                 road="3-4"
             elif(vert_road[i][1]>=390 and vert_road[i][1]<490):
                 road="4-5"
             elif(vert_road[i][1]>=490 and vert_road[i][1]<590):
                 road="5-6"
             elif(vert_road[i][1]>=590 and vert_road[i][1]<690):
                 road="6-7"

            #  print(road)

             if(vert_road[i][0]>85 and vert_road[i][0]<190):
                 way1="A"+road[0:2]+"A"+road[2:]
             elif(vert_road[i][0]>=190 and vert_road[i][0]<290):
                  way1="B"+road[0:2]+"B"+road[2:]
             elif(vert_road[i][0]>=290 and vert_road[i][0]<390):
                way1="C"+road[0:2]+"C"+road[2:]
             elif(vert_road[i][0]>=390 and vert_road[i][0]<490):
                 way1="D"+road[0:2]+"D"+road[2:]
             elif(vert_road[i][0]>=490 and vert_road[i][0]<590):
                 way1="E"+road[0:2]+"E"+road[2:]
             elif(vert_road[i][0]>=590 and vert_road[i][0]<690):
                way1="F"+road[0:2]+"F"+road[2:]
             elif(vert_road[i][0]>=690 and vert_road[i][0]<790):
                 way1="G"+road[0:2]+"G"+road[2:]
            #  print(way1)
             vertical_roads_under_construction.append(way1)
             vertical_roads_under_construction = [*set(vertical_roads_under_construction)]
             vertical_roads_under_construction.sort()
             

    # print(vertical_roads_under_construction)
    ##################################################
    
    return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list of
    details of the medicine packages placed in different shops

    ** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
       as well as in the alphabetical order of colors.
       For example, the list should first have the packages of shop_1 listed. 
       For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `medicine_packages` : [ list ]
            nested list containing details of the medicine packages present.
            Each element of this list will contain 
            - Shop number as Shop_n 
            - Color of the package as a string
            - Shape of the package as a string
            - Centroid co-ordinates of the package
    Example call:
    ---
    medicine_packages = detect_medicine_packages(maze_image)
    """    
    medicine_packages_present = []

    ##############	ADD YOUR CODE HERE	##############
    img = maze_image
    # cv2.imshow('img',img)
    green_lower=np.array([0,255,0])
    green_higher=np.array([0,255,0])
    pink_lower=np.array([180,0,255])
    pink_higher=np.array([180,0,255])
    sb_lower=np.array([255,255,0])
    sb_higher=np.array([255,255,0])
    or_lower=np.array([0,127,255])
    or_higher=np.array([0,127,255])
    med=[]
    centroid=[]
    f_list=[]
    fs_list=[]
    plist=[]
    # green_lower=np.array([0,253,0])
    # green_higher=np.array([0,255,0])
    mask1 = cv2.inRange(img, green_lower, green_higher)
    mask2 = cv2.inRange(img, pink_lower, pink_higher)
    mask3 = cv2.inRange(img, sb_lower, sb_higher)
    mask4 = cv2.inRange(img, or_lower, or_higher)
    mask = mask1 | mask2 | mask3 | mask4

    gandalf = cv2.bitwise_and(img,img, mask=mask)

    cont,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(img,cont,-1,(255,255,0),3)
    for cnt in cont :

        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        n=approx.ravel()
        s_type=len(n)
        centx=int((n[0]+n[2]+n[4])/3)
        centy=int((n[1]+n[3]+n[5])/3)
        img_col=(img[centy][centx])
        if(np.array_equal(img_col,or_higher)==True):
            col_val="Orange"
        elif(np.array_equal(img_col,sb_higher)==True):
            col_val="Skyblue"
        elif(np.array_equal(img_col,pink_higher)==True):
            col_val="Pink"
        elif(np.array_equal(img_col,green_higher)==True):
            col_val="Green"
        else:
            col_val="ded"

        # print(img_col)
        if(s_type==8):
            dist=abs(n[4]-n[0])
            if(dist<=12):
                continue

        # print(col_val)
        # print(centx,centy)
        if(s_type==6):
            s="Triangle"
            centroid=[centx,centy-1]
            # print(centroid)
        elif(s_type==8):
            s="Square"
            centroid=[centx+4,centy-3]
            # print(centroid)
        else:
            s="Circle"
            centroid=[centx+6,centy+10]
            # print(centroid)
        # print(s)
        if(n[0]>90 and n[0]<190 and n[1]>90 and n[1]<190):
            shop="Shop_1"
        elif(n[0]>90 and n[0]<190 and n[1]>=190 and n[1]<290):
            shop="Shop_7"
        elif(n[0]>90 and n[0]<190 and n[1]>=290 and n[1]<390):
            shop="Shop_13"
        elif(n[0]>90 and n[0]<190 and n[1]>=390 and n[1]<490):
            shop="Shop_19"
        elif(n[0]>90 and n[0]<190 and n[1]>=490 and n[1]<590):
            shop="Shop_25"
        elif(n[0]>90 and n[0]<190 and n[1]>=590 and n[1]<699):
            shop="Shop_31"
        elif(n[0]>=190 and n[0]<290 and n[1]>=90 and n[1]<190):
            shop="Shop_2"
        elif(n[0]>=190 and n[0]<290 and n[1]>=190 and n[1]<290):
            shop="Shop_8"
        elif(n[0]>=190 and n[0]<290 and n[1]>=290 and n[1]<390):
            shop="Shop_14"
        elif(n[0]>=190 and n[0]<290 and n[1]>=390 and n[1]<490):
            shop="Shop_20"
        elif(n[0]>=190 and n[0]<290 and n[1]>=490 and n[1]<590):
            shop="Shop_26"
        elif(n[0]>=190 and n[0]<290 and n[1]>=590 and n[1]<699):
            shop="Shop_32"
        elif(n[0]>=290 and n[0]<390 and n[1]>=90 and n[1]<190):
            shop="Shop_3"
        elif(n[0]>=290 and n[0]<390 and n[1]>=190 and n[1]<290):
            shop="Shop_9"
        elif(n[0]>=290 and n[0]<390 and n[1]>=290 and n[1]<390):
            shop="Shop_15"
        elif(n[0]>=290 and n[0]<390 and n[1]>=390 and n[1]<490):
            shop="Shop_21"
        elif(n[0]>=290 and n[0]<390 and n[1]>=490 and n[1]<590):
            shop="Shop_27"
        elif(n[0]>=290 and n[0]<390 and n[1]>=590 and n[1]<699):
            shop="Shop_33"
        elif(n[0]>=390 and n[0]<490 and n[1]>=90 and n[1]<190):
            shop="Shop_4"
        elif(n[0]>=390 and n[0]<490 and n[1]>=190 and n[1]<290):
            shop="Shop_10"
        elif(n[0]>=390 and n[0]<490 and n[1]>=290 and n[1]<390):
            shop="Shop_16"
        elif(n[0]>=390 and n[0]<490 and n[1]>=390 and n[1]<490):
            shop="Shop_22"
        elif(n[0]>=390 and n[0]<490 and n[1]>=490 and n[1]<590):
            shop="Shop_28"
        elif(n[0]>=390 and n[0]<490 and n[1]>=590 and n[1]<699):
            shop="Shop_34"
        elif(n[0]>=490 and n[0]<590 and n[1]>=90 and n[1]<190):
            shop="Shop_5"
        elif(n[0]>=490 and n[0]<590 and n[1]>=190 and n[1]<290):
            shop="Shop_11"
        elif(n[0]>=490 and n[0]<590 and n[1]>=290 and n[1]<390):
            shop="Shop_17"
        elif(n[0]>=490 and n[0]<590 and n[1]>=390 and n[1]<490):
            shop="Shop_23"
        elif(n[0]>=490 and n[0]<590 and n[1]>=490 and n[1]<590):
            shop="Shop_29"
        elif(n[0]>=490 and n[0]<590 and n[1]>=590 and n[1]<699):
            shop="Shop_35"
        elif(n[0]>=590 and n[0]<690 and n[1]>=90 and n[1]<190):
            shop="Shop_6"
        elif(n[0]>=590 and n[0]<690 and n[1]>=190 and n[1]<290):
            shop="Shop_12"
        elif(n[0]>=590 and n[0]<690 and n[1]>=290 and n[1]<390):
            shop="Shop_18"
        elif(n[0]>=590 and n[0]<690 and n[1]>=390 and n[1]<490):
            shop="Shop_24"
        elif(n[0]>=590 and n[0]<690 and n[1]>=490 and n[1]<590):
            shop="Shop_30"
        elif(n[0]>=590 and n[0]<690 and n[1]>=590 and n[1]<699):
            shop="Shop_36"
        else:
            shop="ded"
        # print(n)
        # print(shop)
        med.append(shop)
        # draws boundary of contours.
        cv2.drawContours(img, [approx], 0, (26, 100, 33), 2) 
        flist=[shop,col_val,s,centroid]
        plist.append(flist)
        plist.sort()
        medicine_packages_present=plist
    ##################################################

    return medicine_packages_present

def detect_arena_parameters(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) horizontal_roads_under_construction : list of missing horizontal links
    iii) vertical_roads_under_construction : list of missing vertical links
    iv) medicine_packages : list containing details of medicine packages

    These four categories constitute the four keys of the dictionary

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `arena_parameters` : { dictionary }
            dictionary containing details of the arena parameters
    
    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """    
    arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
    
    arena_parameters={'traffic_signals':detect_traffic_signals(maze_image),'horizontal_roads_under_construction':detect_horizontal_roads_under_construction(maze_image),'vertical_roads_under_construction':detect_vertical_roads_under_construction(maze_image),'medicine_packages_present':detect_medicine_packages(maze_image)}
    return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	


if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

	# read image using opencv
	maze_image = cv2.imread(img_file_path)

	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: ", arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input(
	    '\nDo you want to run your script on all test images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 15):

			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

			# read image using opencv
			maze_image = cv2.imread(img_file_path)

			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')

			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)

			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()
