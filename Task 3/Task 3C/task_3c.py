'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[PB_3004]
# Author List:		[Advait Dhamorikar]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
#


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2
import numpy
from numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################
x_coor=0
y_coor=0
angle_prev=0
prev_image=0


#####################################################################################

def perspective_transform(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array

    Example call:
    ---
    warped_image = perspective_transform(image)
    """
    warped_image = []
#################################  ADD YOUR CODE HERE  ###############################
    # image = cv2.resize(image, (800, 800))
    # print(image)
    global prev_image
    dict1, corners1 = task_1b.detect_ArUco_details(image)
    if (len(corners1)==5):
        h, w = image.shape[:2]
        # Specify destination points to obtain a straightened image
        dst_points = np.array([[0, 0], [w, 0], [0, h], [w, h]], dtype=np.float32)
        # Compute the perspective transform matrix
        c4 = (corners1[1][2][0], corners1[1][2][1])
        c3 = (corners1[2][0][0], corners1[2][0][1])
        c2 = (corners1[4][1][0], corners1[4][1][1])
        c1 = (corners1[3][0][0], corners1[3][0][1])
        # print(c1, c2, c3, c4)
        src_points = np.array([c1, c2, c3, c4], dtype=np.float32)
        M = cv2.getPerspectiveTransform(src_points, dst_points)
        # print(
            # f"src_points: {corners1[4][1], corners1[1][2],corners1[2][2], corners1[3][0]}")
        for x in range(0, 4):
            # print(src_points[x][0], src_points[x][1])
            cv2.circle(
                    image, (int(src_points[x][0]), int(src_points[x][1])), 5, (0, 0, 255), cv2.FILLED)
            # Apply the perspective transform
            # cv2.imshow("circle", image)
        # cv2.imshow("here!", image)
            # image= cv2.rotate(image, cv2.ROTATE_180)
        img_straight = cv2.warpPerspective(image, M, (w, h))
        img_straight = cv2.resize(img_straight, (800, 800))
        warped_image=img_straight
        prev_image=warped_image

            # warped_image= cv2.rotate(img_straight, cv2.ROTATE_180)
        # cv2.imshow("warped_image", warped_image)
        # cv2.waitKey(0)
    else:
        warped_image=prev_image
        # warped_image=cv2.resize(image, (800, 800))
    

######################################################################################

    return warped_image


def transform_values(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]

    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.

    Example call:
    ---
    scene_parameters = transform_values(image)
    """
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    crop = perspective_transform(image)
    if isinstance(crop,int) and crop==0:
        return
    global x_coor, y_coor, angle_prev
    # print(f"crop:{crop}")

    dict1, corners1 = task_1b.detect_ArUco_details(crop)
    # print(dict1, corners1)
    # print(dict1,corners1)
    # print(f"corners1:{corners1}")
    angle=0
    if(len(corners1)==1):
            x_coor = int(dict1[5][0][0])
            y_coor = int(dict1[5][0][1])
            cv2.circle(crop, (x_coor,y_coor), 5, (0, 0, 255), cv2.FILLED)
            # cv2.imshow("warp", crop)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            angle = int(dict1[5][1])
            # print("x=",x_coor,"y=", y_coor,"z=", angle)
            if (x_coor > 400):
                copp_x = ((x_coor-400)/400)*(0.955)
            elif (x_coor <= 400):
                copp_x = ((400-x_coor)/400)*-0.955
            if (y_coor <= 400):
                copp_y = ((400-y_coor)/400)*(0.955)
            elif (y_coor > 400):
                copp_y = ((y_coor-400)/400)*-0.955
            if (angle > 90):
                angle = -(180-(angle-90))+90
            elif (angle < 90):
                angle = (180-(90-angle))+90
            scene_parameters = [copp_x, copp_y, angle]
            x_coor, y_coor, angle_prev=scene_parameters
            # print(scene_parameters)
    else:
        scene_parameters=[x_coor,y_coor,angle_prev]
        # print(scene_parameters)

    # sim.setObjectPosition(medicine, arena, [x, 0, 0.015])
    # print(scene_parameters)
    return scene_parameters


######################################################################################



def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.

    Example call:
    ---
    set_values(scene_parameters)
    """
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    arena = sim.getObject('/Arena')
    x, y, angle = scene_parameters
    # sim.setObjectParent(aruco_handle, arena, False)
    # sim.setObjectAlias(aruco_handle, "marker")
    sim.setObjectPosition(aruco_handle, arena, [x, y, 0.00])
    sim.setObjectOrientation(aruco_handle, -1, [0, 0, (angle*3.14)/180])
######################################################################################

    return None


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################
    cam=cv2.VideoCapture(3)
    while(1):
        success,image=cam.read()
        # image = cv2.imread(frame)
        image = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imshow('og',image)
        try:
            p=transform_values(image)
            # p = [0.7472875, -0.3461875, 3.142]
            # p = [-0.26978749999999996, 0.4464625, 3.142]
            # print(f"p: {p}")
            set_values(p)
            # print(p)
        except Exception as e:
            pass
        if(cv2.waitKey(1) and 0xFF==ord("q")):
            break
    cam.release()
    cv2.destroyAllWindows()
    # mask = cv2.inRange(image, (130, 130, 130), (220, 220, 220))
    # cont, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # for cnt in cont:
    #     approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    #     cv2.drawContours(mask, [approx], 0, (0, 255, 255), 2)
    # image_marked=perspective_transform(image)
    # cv2.imshow('marked', image_marked)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
#######################################################################################
