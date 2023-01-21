'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2


##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def BFS(g, src, dest, v, pred, dist):
    visited = {}
    for i in g:
        visited[i] = 0
        pred[i] = -1
        dist[i] = 32167
    visited[src] = 1
    dist[src] = 0
    q = [src]

    while len(q) != 0:
        p = q.pop(0)
        for i in range(len(g[p])):
            for j in g[p]:
                if visited[j] == 0:
                    visited[j] = 1
                    dist[j] = dist[p] + 1
                    pred[j] = p
                    q.append(j)
                    if j == dest:
                        return True
    return False


def shortestPath(g, src, dest):
    pred = {}
    dist = {}
    if not BFS(g, src, dest, len(g), pred, dist):
        print("NOT CONNECTED")
        return
    path = []
    crawl = dest
    path.append(crawl)
    while pred[crawl] != -1:
        path.append(pred[crawl])
        crawl = pred[crawl]
    return path


def printDirection(a, b, face, directions, traffic_signal, faceB):
    if b[0] < a[0] and a[1] == b[1] and face == a[0] and faceB == a[0] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("LEFT")
        face = a[1]
        faceB = a[1] + "_"
    elif b[0] < a[0] and a[1] == b[1] and face == a[1] and faceB == a[1] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("STRAIGHT")
        face = a[1]
        faceB = a[1] + "_"
    elif b[0] < a[0] and a[1] == b[1] and face == a[0] + "_" and faceB == a[0]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("RIGHT")
        face = a[1]
        faceB = a[1] + "_"
    elif b[0] < a[0] and a[1] == b[1] and face == a[1] + "_" and faceB == a[1]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("REVERSE")
        face = a[1]
        faceB = a[1] + "_"

    if b[0] == a[0] and b[1] < a[1] and face == a[0] and faceB == a[0] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("STRAIGHT")
        face = a[0]
        faceB = a[0] + "_"
    elif b[0] == a[0] and b[1] < a[1] and face == a[1] and faceB == a[1] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("RIGHT")
        face = a[0]
        faceB = a[0] + "_"
    elif b[0] == a[0] and b[1] < a[1] and face == a[1] + "_" and faceB == a[1]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("LEFT")
        face = a[0]
        faceB = a[0] + "_"
    elif b[0] == a[0] and b[1] < a[1] and face == a[0] + "_" and faceB == a[0]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("REVERSE")
        face = a[0]
        faceB = a[0] + "_"

    if b[0] > a[0] and a[1] == b[1] and face == a[1] and faceB == a[1] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("REVERSE")
        face = a[1] + "_"
        faceB = a[1]
    elif b[0] > a[0] and a[1] == b[1] and face == a[0] and faceB == a[0] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("RIGHT")
        face = a[1] + "_"
        faceB = a[1]
    elif b[0] > a[0] and a[1] == b[1] and face == a[0] + "_" and faceB == a[0]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("LEFT")
        face = a[1] + "_"
        faceB = a[1]
    elif b[0] > a[0] and a[1] == b[1] and face == a[1] + "_" and faceB == a[1]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("STRAIGHT")
        face = a[1] + "_"
        faceB = a[1]

    if b[0] == a[0] and b[1] > a[1] and face == a[1] and faceB == a[1] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("LEFT")
        face = a[0] + "_"
        faceB = a[0]
    elif b[0] == a[0] and b[1] > a[1] and face == a[0] + "_" and faceB == a[0]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("STRAIGHT")
        face = a[0] + "_"
        faceB = a[0]
    elif b[0] == a[0] and b[1] > a[1] and face == a[0] and faceB == a[0] + "_":
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("REVERSE")
        face = a[0] + "_"
        faceB = a[0]
    elif b[0] == a[0] and b[1] > a[1] and face == a[1] + "_" and faceB == a[1]:
        if a in traffic_signal:
            directions.append("WAIT_5")
        directions.append("RIGHT")
        face = a[0] + "_"
        faceB = a[0]
    return face, faceB


##############################################################

def detect_all_nodes(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals, start_node and end_node are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals, start_node, end_node` : [ list ], str, str
            list containing nodes in which traffic signals are present, start and end node too
    
    Example call:
    ---
    traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
    """
    traffic_signals = []
    start_node = ""
    end_node = ""

    ##############	ADD YOUR CODE HERE	##############
    img = image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    list = []
    all_signals = []
    purple_lower = np.array([189, 43, 105])
    purple_higher = np.array([189, 43, 105])
    green_lower = np.array([0, 255, 0])
    green_higher = np.array([0, 255, 0])
    mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    endmask = cv2.inRange(img, purple_lower, purple_higher)
    startmask = cv2.inRange(img, green_lower, green_higher)

    startcont, _ = cv2.findContours(
        startmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in startcont:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 255), 2)

        n = approx.ravel()
        diff = n[3] - n[1]
        if (len(n) == 8 and diff < 20):
            i = 0
            for i in range(0, len(n)):
                if (i % 2 == 0):
                    if (n[i] > 90 and n[i] < 180):
                        char1 = "A"
                    elif (n[i] > 180 and n[i] < 280):
                        char1 = "B"
                    elif (n[i] > 280 and n[i] < 380):
                        char1 = "C"
                    elif (n[i] > 380 and n[i] < 480):
                        char1 = "D"
                    elif (n[i] > 480 and n[i] < 580):
                        char1 = "E"
                    elif (n[i] > 580 and n[i] < 680):
                        char1 = "F"
                elif (i % 3 == 0 and i > 0):
                    if (n[i] > 90 and n[i] < 180):
                        char2 = "1"
                    elif (n[i] > 180 and n[i] < 280):
                        char2 = "2"
                    elif (n[i] > 280 and n[i] < 380):
                        char2 = "3"
                    elif (n[i] > 380 and n[i] < 480):
                        char2 = "4"
                    elif (n[i] > 480 and n[i] < 580):
                        char2 = "5"
                    elif (n[i] > 580 and n[i] < 680):
                        char2 = "6"
            signal = char1 + char2
            start_node = signal

    endcont, _ = cv2.findContours(
        endmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in endcont:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 255), 2)

        n = approx.ravel()
        i = 0
        for i in range(0, len(n)):
            if i % 2 == 0:
                if (n[i] > 90 and n[i] < 180):
                    char1 = "A"
                elif (n[i] > 180 and n[i] < 280):
                    char1 = "B"
                elif (n[i] > 280 and n[i] < 380):
                    char1 = "C"
                elif (n[i] > 380 and n[i] < 480):
                    char1 = "D"
                elif (n[i] > 480 and n[i] < 580):
                    char1 = "E"
                elif (n[i] > 580 and n[i] < 680):
                    char1 = "F"
            elif (i % 3 == 0 and i > 0):
                if (n[i] > 90 and n[i] < 180):
                    char2 = "1"
                elif (n[i] > 180 and n[i] < 280):
                    char2 = "2"
                elif (n[i] > 280 and n[i] < 380):
                    char2 = "3"
                elif (n[i] > 380 and n[i] < 480):
                    char2 = "4"
                elif (n[i] > 480 and n[i] < 580):
                    char2 = "5"
                elif (n[i] > 580 and n[i] < 680):
                    char2 = "6"
        signal = char1 + char2
        end_node = signal

    endcont, _ = cv2.findContours(
        endmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in endcont:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 255), 2)

        n = approx.ravel()
        i = 0
        for i in range(0, len(n)):
            if (i % 2 == 0):
                if (n[i] > 90 and n[i] < 180):
                    char1 = "A"
                elif (n[i] > 180 and n[i] < 280):
                    char1 = "B"
                elif (n[i] > 280 and n[i] < 380):
                    char1 = "C"
                elif (n[i] > 380 and n[i] < 480):
                    char1 = "D"
                elif (n[i] > 480 and n[i] < 580):
                    char1 = "E"
                elif (n[i] > 580 and n[i] < 680):
                    char1 = "F"
            elif (i % 3 == 0 and i > 0):
                if (n[i] > 90 and n[i] < 180):
                    char2 = "1"
                elif (n[i] > 180 and n[i] < 280):
                    char2 = "2"
                elif (n[i] > 280 and n[i] < 380):
                    char2 = "3"
                elif (n[i] > 380 and n[i] < 480):
                    char2 = "4"
                elif (n[i] > 480 and n[i] < 580):
                    char2 = "5"
                elif (n[i] > 580 and n[i] < 680):
                    char2 = "6"
        signal = char1 + char2
        # print(signal)
        # all_signals.append(signal)

    cont, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in cont:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 255), 2)

        n = approx.ravel()
        i = 0
        for i in range(0, len(n)):
            if (i % 2 == 0):
                if (n[i] > 90 and n[i] < 180):
                    char1 = "A"
                elif (n[i] > 180 and n[i] < 280):
                    char1 = "B"
                elif (n[i] > 280 and n[i] < 380):
                    char1 = "C"
                elif (n[i] > 380 and n[i] < 480):
                    char1 = "D"
                elif (n[i] > 480 and n[i] < 580):
                    char1 = "E"
                elif (n[i] > 580 and n[i] < 680):
                    char1 = "F"
            elif (i % 3 == 0 and i > 0):
                if (n[i] > 90 and n[i] < 180):
                    char2 = "1"
                elif (n[i] > 180 and n[i] < 280):
                    char2 = "2"
                elif (n[i] > 280 and n[i] < 380):
                    char2 = "3"
                elif (n[i] > 380 and n[i] < 480):
                    char2 = "4"
                elif (n[i] > 480 and n[i] < 580):
                    char2 = "5"
                elif (n[i] > 580 and n[i] < 680):
                    char2 = "6"
        signal = char1 + char2
        list.append(signal)
        list.sort()
    traffic_signals = list
    ##################################################

    return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary of the
    connect path from a node to other nodes and will be used for path planning

    HINT: Check for the road besides the nodes for connectivity 

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `paths` : { dictionary }
            Every node's connection to other node and set it's value as edge value 
            Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
                    "D5":{"C5":1, "D2":1, "D6":1 }  }

            Why edge value 1? -->> since every road is equal

    Example call:
    ---
    paths = detect_paths_to_graph(maze_image)
    """

    # paths = {}

    ##############	ADD YOUR CODE HERE	##############
    list = []
    horizontal_roads_under_construction = []
    vertical_roads_under_construction = []
    rot1 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    rot2 = cv2.rotate(rot1, cv2.ROTATE_90_CLOCKWISE)
    rot3 = cv2.rotate(rot2, cv2.ROTATE_90_CLOCKWISE)
    p1 = cv2.bitwise_and(image, rot1)
    p2 = cv2.bitwise_and(p1, rot2)
    p3 = cv2.bitwise_and(p2, rot3)
    white_lower = np.array([253, 253, 253])
    white_higher = np.array([255, 255, 255])
    blue_lower = np.array([0, 0, 253])
    blue_higher = np.array([0, 0, 255])
    red_lower = np.array([253, 0, 0])
    red_higher = np.array([255, 0, 0])
    green_lower = np.array([0, 253, 0])
    green_higher = np.array([0, 255, 0])
    mask1 = cv2.inRange(p3, white_lower, white_higher)
    target = cv2.bitwise_and(p3, p3, mask=mask1)
    tp = cv2.bitwise_xor(target, image)

    kernel = np.ones((5, 5), np.uint8)

    # Using cv2.erode() method
    image = cv2.erode(tp, kernel)
    mask1 = cv2.inRange(image, white_lower, white_higher)
    mask2 = cv2.inRange(image, red_lower, red_higher)
    mask3 = cv2.inRange(image, green_lower, green_higher)
    mask = mask1 | mask2 | mask3
    gandalf = cv2.bitwise_and(image, image, mask=mask1)
    xrect = []
    yrect = []
    horiz_road = []
    vert_road = []
    temp = []

    imgGrey = cv2.cvtColor(gandalf, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4:
            xrect.append(x)
            yrect.append(y)
            x1, y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w) / h
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                pass
            else:
                cv2.drawContours(gandalf, [approx], 0, (100, 100, 75), 5)
                temp = approx.ravel()
                xcoor = abs(temp[4] - temp[0])
                ycoor = abs(temp[5] - temp[1])
                if (xcoor > ycoor):
                    horiz_road.append(temp)
                else:
                    vert_road.append(temp)

    for i in range(0, len(horiz_road)):
        len_road = abs(horiz_road[i][0] - horiz_road[i][4])
        if (len_road > 30):
            if (horiz_road[i][0] > 95 and horiz_road[i][0] < 190):
                road = "A-B"
            elif (horiz_road[i][0] >= 190 and horiz_road[i][0] < 290):
                road = "B-C"
            elif (horiz_road[i][0] >= 290 and horiz_road[i][0] < 390):
                road = "C-D"
            elif (horiz_road[i][0] >= 390 and horiz_road[i][0] < 490):
                road = "D-E"
            elif (horiz_road[i][0] >= 490 and horiz_road[i][0] < 590):
                road = "E-F"

            if (horiz_road[i][1] > 95 and horiz_road[i][1] < 190):
                way1 = road[:1] + "1" + road[1:] + "1"
            elif (horiz_road[i][1] >= 190 and horiz_road[i][1] < 290):
                way1 = road[:1] + "2" + road[1:] + "2"
            elif (horiz_road[i][1] >= 290 and horiz_road[i][1] < 390):
                way1 = road[:1] + "3" + road[1:] + "3"
            elif (horiz_road[i][1] >= 390 and horiz_road[i][1] < 490):
                way1 = road[:1] + "4" + road[1:] + "4"
            elif (horiz_road[i][1] >= 490 and horiz_road[i][1] < 590):
                way1 = road[:1] + "5" + road[1:] + "5"
            elif (horiz_road[i][1] >= 590 and horiz_road[i][1] < 690):
                way1 = road[:1] + "6" + road[1:] + "6"
            horizontal_roads_under_construction.append(way1)
            horizontal_roads_under_construction.sort()

    list = []
    vertical_roads_under_construction = []
    rot1 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    rot2 = cv2.rotate(rot1, cv2.ROTATE_90_CLOCKWISE)
    rot3 = cv2.rotate(rot2, cv2.ROTATE_90_CLOCKWISE)
    p1 = cv2.bitwise_and(image, rot1)
    p2 = cv2.bitwise_and(p1, rot2)
    p3 = cv2.bitwise_and(p2, rot3)
    white_lower = np.array([253, 253, 253])
    white_higher = np.array([255, 255, 255])
    blue_lower = np.array([0, 0, 253])
    blue_higher = np.array([0, 0, 255])
    red_lower = np.array([253, 0, 0])
    red_higher = np.array([255, 0, 0])
    green_lower = np.array([0, 253, 0])
    green_higher = np.array([0, 255, 0])
    mask1 = cv2.inRange(p3, white_lower, white_higher)
    target = cv2.bitwise_and(p3, p3, mask=mask1)
    tp = cv2.bitwise_xor(target, image)

    kernel = np.ones((5, 5), np.uint8)

    # Using cv2.erode() method
    image = cv2.erode(tp, kernel)
    mask1 = cv2.inRange(image, white_lower, white_higher)
    mask2 = cv2.inRange(image, red_lower, red_higher)
    mask3 = cv2.inRange(image, green_lower, green_higher)
    mask = mask1 | mask2 | mask3
    gandalf = cv2.bitwise_and(image, image, mask=mask1)
    xrect = []
    yrect = []
    horiz_road = []
    vert_road = []
    temp = []

    imgGrey = cv2.cvtColor(gandalf, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        # cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4:
            xrect.append(x)
            yrect.append(y)
            x1, y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w) / h
            # print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                pass
            else:
                cv2.drawContours(gandalf, [approx], 0, (100, 100, 75), 5)
                temp = approx.ravel()
                xcoor = abs(temp[4] - temp[0])
                ycoor = abs(temp[5] - temp[1])
                if (xcoor > ycoor):
                    horiz_road.append(temp)
                else:
                    vert_road.append(temp)

    for i in range(0, len(vert_road)):
        len_road = abs(vert_road[i][1] - vert_road[i][3])
        if (len_road > 30):
            if (vert_road[i][1] > 95 and vert_road[i][1] < 190):
                road = "1-2"
            elif (vert_road[i][1] >= 190 and vert_road[i][1] < 290):
                road = "2-3"
            elif (vert_road[i][1] >= 290 and vert_road[i][1] < 390):
                road = "3-4"
            elif (vert_road[i][1] >= 390 and vert_road[i][1] < 490):
                road = "4-5"
            elif (vert_road[i][1] >= 490 and vert_road[i][1] < 590):
                road = "5-6"
            elif (vert_road[i][1] >= 590 and vert_road[i][1] < 690):
                road = "6-7"

            if (vert_road[i][0] > 85 and vert_road[i][0] < 190):
                way1 = "A" + road[0:2] + "A" + road[2:]
            elif (vert_road[i][0] >= 190 and vert_road[i][0] < 290):
                way1 = "B" + road[0:2] + "B" + road[2:]
            elif (vert_road[i][0] >= 290 and vert_road[i][0] < 390):
                way1 = "C" + road[0:2] + "C" + road[2:]
            elif (vert_road[i][0] >= 390 and vert_road[i][0] < 490):
                way1 = "D" + road[0:2] + "D" + road[2:]
            elif (vert_road[i][0] >= 490 and vert_road[i][0] < 590):
                way1 = "E" + road[0:2] + "E" + road[2:]
            elif (vert_road[i][0] >= 590 and vert_road[i][0] < 690):
                way1 = "F" + road[0:2] + "F" + road[2:]
            elif (vert_road[i][0] >= 690 and vert_road[i][0] < 790):
                way1 = "G" + road[0:2] + "G" + road[2:]
            vertical_roads_under_construction.append(way1)
            vertical_roads_under_construction.sort()

    all_construction = vertical_roads_under_construction + \
        horizontal_roads_under_construction
    all_construction = [*set(all_construction)]
    all_nodes = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5",
                 "C6",
                 "D1", "D2", "D3", "D4", "D5", "D6", "E1", "E2", "E3", "E4", "E5", "E6", "F1", "F2", "F3", "F4", "F5",
                 "F6"]
    charlist = []
    neighbourlist = []
    finlist = []
    for i in range(0, len(all_nodes)):
        el = all_nodes[i]
        char_ = el[0]
        num_ = int(el[1])
        if (el == "A1"):
            charlist.append(el)
            n1 = "A2"
            n2 = "B1"
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            # neighbourlist.append(n3)

            finlist.append(neighbourlist)
            neighbourlist = []
        elif (el == "A6"):
            charlist.append(el)
            n1 = "A5"
            n2 = "B6"
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            # neighbourlist.append(n3)

            finlist.append(neighbourlist)
            neighbourlist = []
        elif (el == "F1"):
            charlist.append(el)
            n1 = "F2"
            n2 = "E1"
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            # neighbourlist.append(n3)

            finlist.append(neighbourlist)
            neighbourlist = []
        elif (el == "F6"):
            charlist.append(el)
            n1 = "F5"
            n2 = "E6"
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            # neighbourlist.append(n3)

            finlist.append(neighbourlist)
            neighbourlist = []
        elif (char_ == "A" and el != "A1" and el != "A6"):
            charlist.append(el)
            n1 = "A" + str(num_ - 1)
            n2 = "A" + str(num_ + 1)
            n3 = "B" + str(num_)
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            neighbourlist.append(n3)

            finlist.append(neighbourlist)
            neighbourlist = []
        elif (char_ == "F" and el != "F1" and el != "F6"):
            charlist.append(el)
            n1 = "F" + str(num_ - 1)
            n2 = "F" + str(num_ + 1)
            n3 = "E" + str(num_)
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            neighbourlist.append(n3)
            finlist.append(neighbourlist)
            neighbourlist = []
        elif (char_ != "A" and char_ != "F" and num_ != 1 and num_ != 6):
            charlist.append(el)
            n1 = char_ + str(num_ - 1)
            n2 = char_ + str(num_ + 1)
            n3 = chr(ord(char_) + 1) + str(num_)
            n4 = chr(ord(char_) - 1) + str(num_)
            neighbourlist.append(n1)
            neighbourlist.append(n2)
            neighbourlist.append(n3)
            neighbourlist.append(n4)
            finlist.append(neighbourlist)
            neighbourlist = []
        elif (num_ == 1 and char_ != "A" and char_ != "F" and el != "A1" and el != "F1"):
            charlist.append(el)
            n2 = char_ + str(num_ + 1)
            n3 = chr(ord(char_) + 1) + str(num_)
            n4 = chr(ord(char_) - 1) + str(num_)
            neighbourlist.append(n2)
            neighbourlist.append(n3)
            neighbourlist.append(n4)
            finlist.append(neighbourlist)
            neighbourlist = []

        elif (num_ == 6 and char_ != "A" and char_ != "F" and el != "A1" and el != "F1"):
            charlist.append(el)
            n1 = char_ + str(num_ - 1)
            # n2 = char_+str(num_+1)
            n3 = chr(ord(char_) + 1) + str(num_)
            n4 = chr(ord(char_) - 1) + str(num_)
            neighbourlist.append(n1)
            # neighbourlist.append(n2)
            neighbourlist.append(n3)
            neighbourlist.append(n4)
            # neighbourlist=[]
            finlist.append(neighbourlist)
            neighbourlist = []
        # print(charlist)
    m = 0
    l = 0
    # Path Subtraction
    for i in range(0, len(all_nodes)):
        for j in range(0, len(all_construction)):

            all_el = all_construction[j]
            rem_el1 = all_el[0:2]
            rem_el2 = all_el[3:]

            if (rem_el2 == all_nodes[i]):
                finlist[i].remove(str(rem_el1))
            elif (rem_el1 == all_nodes[i]):
                finlist[i].remove(str(rem_el2))

    ones = [1 for x in range(len(all_nodes))]
    finlist = [dict(zip(finlist[i], ones)) for i in range(len(finlist))]
    paths = dict(zip(all_nodes, finlist))
    ##################################################

    return paths


def detect_arena_parameters(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) start_node : Start node which is mark in light green
    iii) end_node : End node which is mark in Purple
    iv) paths : list containing paths

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

    Eg. arena_parameters={"traffic_signals":[], 
                          "start_node": "E4", 
                          "end_node":"A3", 
                          "paths": {}}
    """
    arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
    paths = detect_paths_to_graph(maze_image)
    traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
    arena_parameters["traffic_signals"] = traffic_signals
    arena_parameters["start_node"] = start_node
    arena_parameters["end_node"] = end_node
    arena_parameters["paths"] = paths
    ##################################################

    return arena_parameters


def path_planning(graph, start, end):
    """
    Purpose:
    ---
    This function takes the graph(dict), start and end node for planning the shortest path

    ** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
    list given below **

    Input Arguments:
    ---
    `graph` :	{ dictionary }
            dict of all connecting path
    `start` :	str
            name of start node
    `end` :		str
            name of end node


    Returns:
    ---
    `backtrace_path` : [ list of nodes ]
            list of nodes, produced using path planning algorithm

        eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
    
    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """

    backtrace_path = []

    ##############	ADD YOUR CODE HERE	##############
    backtrace_path = shortestPath(graph, start, end)
    backtrace_path.reverse()
    ##################################################

    return backtrace_path


def paths_to_moves(paths, traffic_signal):
    """
    Purpose:
    ---
    This function takes the list of all nodes produces from the path planning algorithm
    and connecting both start and end nodes

    Input Arguments:
    ---
    `paths` :	[ list of all nodes ]
            list of all nodes connecting both start and end nodes (SHORTEST PATH)
    `traffic_signal` : [ list of all traffic signals ]
            list of all traffic signals
    ---
    `moves` : [ list of moves from start to end nodes ]
            list containing moves for the bot to move from start to end

            Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
    
    Example call:
    ---
    moves = paths_to_moves(paths, traffic_signal)
    """

    list_moves = []

    ##############	ADD YOUR CODE HERE	##############
    face = paths[0][0]
    faceB = paths[0][0] + "_"
    for i in range(len(paths)):
        lis = paths[i:i + 2]
        if len(lis) != 1:
            face, faceB = printDirection(
                lis[0], lis[1], face, list_moves, traffic_signal, faceB)
    # print(directions)
    ##################################################

    return list_moves


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########

if __name__ == "__main__":

    # # path directory of images
    img_dir_path = "random_mazes/"

    for file_num in range(0, 10):
        img_key = 'maze_00' + str(file_num)
        img_file_path = img_dir_path + img_key + '.png'
        # read image using opencv
        image = cv2.imread(img_file_path)
        # detect the arena parameters from the image
        arena_parameters = detect_arena_parameters(image)
        print('\n============================================')
        print("IMAGE: ", file_num)
        print(arena_parameters["start_node"],
              "->>> ", arena_parameters["end_node"])

        # path planning and getting the moves
        back_path = path_planning(arena_parameters["paths"], arena_parameters["start_node"],
                                  arena_parameters["end_node"])
        moves = paths_to_moves(back_path, arena_parameters["traffic_signals"])

        print("PATH PLANNED: ", back_path)
        print("MOVES TO TAKE: ", moves)

        # display the test image
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
