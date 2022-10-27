'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
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
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def control_logic(sim):    
    """
    Purpose:
    ---
    This function should implement the control logic for the given problem statement
    You are required to make the robot follow the line to cover all the checkpoints
    and deliver packages at the correct locations.

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    None

    Example call:
    ---
    control_logic(sim)
    """
    ##############  ADD YOUR CODE HERE  ##############
    while 1:
        counter=0
        white_lower = np.array([253, 253, 253])
        white_higher = np.array([255, 255, 255])
        yellow_lower = np.array([75, 75, 75])
        yellow_higher = np.array([76, 76, 76])
        lmotor = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
        rmotor = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
        visionSensorHandle = sim.getObject('/Diff_Drive_Bot/vision_sensor')
        img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        mask1 = cv2.inRange(img, white_lower, white_higher)
        mask2 = cv2.inRange(img, yellow_lower, yellow_higher)
        mask =  mask1
        target = cv2.bitwise_and(img, img, mask=mask)
        target = cv2.flip(cv2.cvtColor(target, cv2.COLOR_BGR2RGB), 0)
        gray = cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)

        # Find the top 20 corners using the cv2.goodFeaturesToTrack()
        corners = cv2.goodFeaturesToTrack(gray,8,0.01,10)
        corners = np.int0(corners)
        # sim.setJointTargetVelocity(rmotor, 0.1)
        # sim.setJointTargetVelocity(lmotor, 0.1)
        print(corners.ravel())
        pp=corners.ravel()
        yavg=int((pp[1]+pp[3]+pp[5]+pp[7]+pp[9]+pp[11]+pp[13]+pp[15])/8)
        print(yavg)
        # Iterate over the corners and draw a circle at that location
        for i in corners:
            x,y = i.ravel()
            print(x,y)
            cv2.circle(target,(x,y),5,(0,0,255),-1)
        if(pp[1] < 250 or pp[3] < 250 or pp[5] < 250 or pp[7] < 250 or pp[9] < 250 or pp[11] < 250 or pp[13] < 250 or pp[15] < 250):
            boolvar=True
        else:
            boolvar=False
        if(int((pp[0]+pp[2])/2)>255 and yavg<320):
            sim.setJointTargetVelocity(rmotor, 0)
            sim.setJointTargetVelocity(lmotor, 0.1)
        elif(int((pp[0]+pp[2])/2)<255 and yavg<320):
            sim.setJointTargetVelocity(rmotor, 0.1)
            sim.setJointTargetVelocity(lmotor, 0)
        elif (yavg > 325 and boolvar==True):
            sim.setJointTargetVelocity(rmotor, 0)
            sim.setJointTargetVelocity(lmotor, 0)
            if(counter==0 or counter==2 or counter==6 or counter==10 or counter==4):
                sim.setJointTargetVelocity(rmotor, 0.1)
                sim.setJointTargetVelocity(lmotor, -0.1)
                
        else:
            sim.setJointTargetVelocity(rmotor, 0.1)
            sim.setJointTargetVelocity(lmotor, 0.1)
        
        # imgGrey = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        # _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
        # contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        # # approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        # print(approx.ravel())
        # cv2.drawContours(target, [approx], 0, (0, 0, 0), 5)
            
        #     cv2.drawContours(target, [approx], 0, (0, 0, 0), 5)
        #     x = approx.ravel()[0]
        #     y = approx.ravel()[1] 
        # for contour in contours:
        #     approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
            
        #     cv2.drawContours(target, [approx], 0, (0, 0, 0), 5)
        #     x = approx.ravel()[0]
        #     y = approx.ravel()[1] 
        #     print(x, y)
            
            
        # print(approx.ravel())
   
        cv2.imshow('hello world', target)
        cv2.waitKey(1)
        cv2.destroyAllWindows
        
        # print(lmotor,rmotor)
    # In CoppeliaSim images are left to right (x-axis), and bottom to top (y-axis)
    # (consistent with the axes of vision sensors, pointing Z outwards, Y up)
    # and color format is RGB triplets, whereas OpenCV uses BGR:
        
    ##################################################

def read_qr_code(sim):
    """
    Purpose:
    ---
    This function detects the QR code present in the camera's field of view and
    returns the message encoded into it.

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    `qr_message`   :    [ string ]
        QR message retrieved from reading QR code

    Example call:
    ---
    control_logic(sim)
    """
    qr_message = None
    ##############  ADD YOUR CODE HERE  ##############

    ##################################################
    return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    lmotor = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
    rmotor = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
    sim.setJointTargetVelocity(rmotor, 0)
    sim.setJointTargetVelocity(lmotor, 0)
    	

    try:

        ## Start the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.startSimulation()
            if sim.getSimulationState() != sim.simulation_stopped:
                print('\nSimulation started correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be started correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be started !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

        ## Runs the robot navigation logic written by participants
        try:
            time.sleep(5)
            control_logic(sim)

        except Exception:
            print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
            print('Stop the CoppeliaSim simulation manually if required.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()

        
        ## Stop the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.stopSimulation()
            time.sleep(0.5)
            if sim.getSimulationState() == sim.simulation_stopped:
                print('\nSimulation stopped correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be stopped correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be stopped !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    except KeyboardInterrupt:
        ## Stop the simulation using ZeroMQ RemoteAPI
        return_code = sim.stopSimulation()
        time.sleep(0.5)
        if sim.getSimulationState() == sim.simulation_stopped:
            print('\nSimulation interrupted by user in CoppeliaSim.')
        else:
            print('\nSimulation could not be interrupted. Stop the simulation manually .')
            sys.exit()
