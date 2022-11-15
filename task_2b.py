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
import sys
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
odel = 0
pdel = 0
bdel = 0
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
    lno = 0
    tcount = 0
    count = 0
    arena_dummy_handle = sim.getObject("/Arena_dummy")

    # Retrieve the handle of the child script attached to the Arena_dummy scene object.
    childscript_handle = sim.getScript(
        sim.scripttype_childscript, arena_dummy_handle, "")

    ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
    sim.callScriptFunction(
        "activate_qr_code", childscript_handle, "checkpoint E")

    ## Retrieve the handle of the Arena_dummy scene object.
    arena_dummy_handle = sim.getObject("/Arena_dummy")

    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
    childscript_handle = sim.getScript(
        sim.scripttype_childscript, arena_dummy_handle, "")

    ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
    sim.callScriptFunction(
        "activate_qr_code", childscript_handle, "checkpoint I")

    ## Retrieve the handle of the Arena_dummy scene object.
    arena_dummy_handle = sim.getObject("/Arena_dummy")

    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
    childscript_handle = sim.getScript(
        sim.scripttype_childscript, arena_dummy_handle, "")

    ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
    sim.callScriptFunction(
        "activate_qr_code", childscript_handle, "checkpoint M")

    while (1):

        # arena_dummy_handle = sim.getObject("/Arena_dummy")

        # ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        # childscript_handle = sim.getScript(
        #     sim.scripttype_childscript, arena_dummy_handle, "")

        # ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
        # sim.callScriptFunction(
        #     "activate_qr_code", childscript_handle, "checkpoint E")

        # ## Retrieve the handle of the Arena_dummy scene object.
        # arena_dummy_handle = sim.getObject("/Arena_dummy")

        # ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        # childscript_handle = sim.getScript(
        #     sim.scripttype_childscript, arena_dummy_handle, "")

        # ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
        # sim.callScriptFunction(
        #     "activate_qr_code", childscript_handle, "checkpoint I")

        # ## Retrieve the handle of the Arena_dummy scene object.
        # arena_dummy_handle = sim.getObject("/Arena_dummy")

        # ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        # childscript_handle = sim.getScript(
        #     sim.scripttype_childscript, arena_dummy_handle, "")

        # ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
        # sim.callScriptFunction(
        #     "activate_qr_code", childscript_handle, "checkpoint M")
        sumforavg = 0
        n = 1
        totalarr = []
        ravcount = 0

        # read_qr_code(sim)
        global odel
        global pdel
        global bdel
        node = 0
        x_ele = 0
        y_ele = 0
        white_lower = np.array([253, 253, 253])
        white_higher = np.array([255, 255, 255])
        yellow_lower = np.array([75, 75, 75])
        yellow_higher = np.array([76, 76, 76])
        blue_lower = np.array([253, 204, 4])
        blue_higher = np.array([253, 204, 4])
        lmotor = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
        rmotor = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
        visionSensorHandle = sim.getObject('/Diff_Drive_Bot/vision_sensor')
        img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # threshold, thresh = cv2.threshold(gray, 127.5, 255, cv2.THRESH_BINARY)

        # print(lno)
        mask1 = cv2.inRange(img, white_lower, white_higher)
        mask2 = cv2.inRange(img, yellow_lower, yellow_higher)
        mask3 = cv2.inRange(img, blue_lower, blue_higher)
        mask = mask1 | mask3
        target = cv2.bitwise_and(img, img, mask=mask)
        target = cv2.flip(cv2.cvtColor(target, cv2.COLOR_BGR2RGB), 0)
        gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        # Find the top 20 corners using the cv2.goodFeaturesToTrack()
        imgGrey = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(imgGrey, [approx], 0, (193, 153, 38), 5)
            x = approx.ravel()
            if (len(x) > 6):
                totalarr.append(x)
            # print(x)
            ravcount += 1
        # print(ravcount)
        # print(totalarr)
        if (ravcount >= 25):
            if (count == 4 or count == 8 or count == 12):
                for i in range(0, 12):
                    sim.setJointTargetVelocity(rmotor, 0.8)
                    sim.setJointTargetVelocity(lmotor, 0.8)
                for i in range(0, 12):
                    sim.setJointTargetVelocity(rmotor, -0.8)
                    sim.setJointTargetVelocity(lmotor, -0.8)
                # read_qr_code(sim)

            if (tcount < 1):
                qrmsg1 = read_qr_code(sim)
                # for i in range(0, 100):
                #     # print(qrm
                for i in range(0, 14):
                    sim.setJointTargetVelocity(rmotor, 1.6)
                    sim.setJointTargetVelocity(lmotor, 1.6)
                tcount += 1

        elif (ravcount < 8 and tcount == 0):
            for i in range(0, len(totalarr)-1):
                for j in range(0, 7, 2):
                    if (totalarr[i][j] > 10 and totalarr[i][j] < 400):
                        sumforavg = sumforavg+totalarr[i][j]
                        n += 1

            avg = sumforavg/(n-1)
            sumforavg = 0
            # print(sumforavg, n-1)
            # print("average = ", avg)
            if (avg > 272):
                sim.setJointTargetVelocity(rmotor, 0)
                sim.setJointTargetVelocity(lmotor, 0.22)
            elif (avg < 235):
                sim.setJointTargetVelocity(rmotor, 0.2)
                sim.setJointTargetVelocity(lmotor, 0)
            else:
                sim.setJointTargetVelocity(rmotor, 1)
                sim.setJointTargetVelocity(lmotor, 1)
                # if(count==3):
                #     sim.wait(5, True)

        elif (tcount >= 1):
            sim.setJointTargetVelocity(rmotor, 0)
            sim.setJointTargetVelocity(lmotor, 0)
            if (count == 0 or count == 2 or count == 6 or count == 10 or count == 14):
                for i in range(0, 4):
                    sim.setJointTargetVelocity(rmotor, 8)
                    sim.setJointTargetVelocity(lmotor, -8)
                tcount = 0
                count += 1

            elif (count == 1 or count == 3 or count == 7 or count == 11 or count == 5 or count == 9 or count == 13 or count==15):
                for i in range(0, 4):
                    sim.setJointTargetVelocity(rmotor, -8)
                    sim.setJointTargetVelocity(lmotor, 8)
                tcount = 0
                count += 1
            elif(count==16):
                break
            # elif(count==15):
            #     for i in range(0, 11):
            #         sim.setJointTargetVelocity(rmotor, -4)
            #         sim.setJointTargetVelocity(lmotor, 4)
            #     for i in range(0,11):
            #         sim.setJointTargetVelocity(rmotor, 1)
            #         sim.setJointTargetVelocity(lmotor, 1)
                    
            #     tcount = 0
            #     count += 1
            # elif(count==16):
            #     for i in range(0, 11):
            #         sim.setJointTargetVelocity(rmotor, -4)
            #         sim.setJointTargetVelocity(lmotor, 4)
            #     for i in range(0, 11):
            #         sim.setJointTargetVelocity(rmotor, 1)
            #         sim.setJointTargetVelocity(lmotor, 1)
            #     # read_qr_code(sim)
            elif (count == 4):
                ## Retrieve the handle of the Arena_dummy scene object.

                arena_dummy_handle = sim.getObject("/Arena_dummy")

                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(
                    sim.scripttype_childscript, arena_dummy_handle, "")

                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
                sim.callScriptFunction(
                    "activate_qr_code", childscript_handle, "checkpoint E")
                # sim.wait(5,True)
                qrmess = read_qr_code(sim)
                # print(qrmess)
                currimg = img
                # for i in range(0, 90):
                #     qrmsg = read_qr_code(sim)
                #     sim.setJointTargetVelocity(rmotor, 0.1)
                #     sim.setJointTargetVelocity(lmotor, 0.1)
                for i in range(0, 6):
                    # qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, -3.2)
                    sim.setJointTargetVelocity(lmotor, -3.2)

                qrmess = read_qr_code(sim)

                if (qrmess == "Orange Cone" and odel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_1", "checkpoint E")
                    odel += 1
                elif (qrmess == "Blue Cylinder" and bdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_2", "checkpoint E")
                    bdel += 1
                elif (qrmess == "Pink Cuboid" and pdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_3", "checkpoint E")
                    pdel += 1

                for i in range(0, 11):
                    # qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, 1.6)
                    sim.setJointTargetVelocity(lmotor, 1.6)

                tcount = 0
                count += 1
            elif (count == 8):
                ## Retrieve the handle of the Arena_dummy scene object.
                arena_dummy_handle = sim.getObject("/Arena_dummy")

                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(
                    sim.scripttype_childscript, arena_dummy_handle, "")

                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
                sim.callScriptFunction(
                    "activate_qr_code", childscript_handle, "checkpoint I")

                qrmsg = read_qr_code(sim)
                # print(qrmsg)

                currimg = img
                # for i in range(0, 90):
                #     qrmsg = read_qr_code(sim)
                #     sim.setJointTargetVelocity(rmotor, 0.1)
                #     sim.setJointTargetVelocity(lmotor, 0.1)

                for i in range(0, 6):
                    qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, -1.6)
                    sim.setJointTargetVelocity(lmotor, -1.6)
                # read_qr_code(sim)

                qrmess = read_qr_code(sim)

                if (qrmess == "Orange Cone" and odel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_1", "checkpoint I")
                    odel += 1
                elif (qrmess == "Blue Cylinder" and bdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_2", "checkpoint I")
                    bdel += 1
                elif (qrmess == "Pink Cuboid" and pdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_3", "checkpoint I")
                    pdel += 1

                for i in range(0, 7):
                    qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, 1.6)
                    sim.setJointTargetVelocity(lmotor, 1.6)
                tcount = 0
                count += 1
            elif (count == 12):
                ## Retrieve the handle of the Arena_dummy scene object.
                arena_dummy_handle = sim.getObject("/Arena_dummy")

                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(
                    sim.scripttype_childscript, arena_dummy_handle, "")

                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
                sim.callScriptFunction(
                    "activate_qr_code", childscript_handle, "checkpoint M")

                qrmsg = read_qr_code(sim)
                # print(qrmsg)
                # for i in range(0, 90):
                #     qrmsg = read_qr_code(sim)
                #     print(qrmsg)
                #     sim.setJointTargetVelocity(rmotor, 0.1)
                #     sim.setJointTargetVelocity(lmotor, 0.1)

                for i in range(0, 6):
                    qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, -1.6)
                    sim.setJointTargetVelocity(lmotor, -1.6)
                # read_qr_code(sim)

                qrmess = read_qr_code(sim)

                if (qrmess == "Orange Cone" and odel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_1", "checkpoint M")
                    odel += 1
                elif (qrmess == "Blue Cylinder" and bdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_2", "checkpoint M")
                    bdel += 1
                elif (qrmess == "Pink Cuboid" and pdel == 0):
                    arena_dummy_handle = sim.getObject("/Arena_dummy")

                    ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                    childscript_handle = sim.getScript(
                        sim.scripttype_childscript, arena_dummy_handle, "")

                    ## Deliver package_1 at checkpoint E
                    sim.callScriptFunction(
                        "deliver_package", childscript_handle, "package_3", "checkpoint M")
                    pdel += 1

                for i in range(0, 12):
                    qrmsg = read_qr_code(sim)
                    sim.setJointTargetVelocity(rmotor, 1.6)
                    sim.setJointTargetVelocity(lmotor, 1.6)
                tcount = 0
                count += 1
            # elif (count == 16):
            #     sim.setJointTargetVelocity(rmotor, 0.1)
            #     sim.setJointTargetVelocity(lmotor, 0.1)
            #     # break

        else:
            # read_qr_code(sim)
            sim.setJointTargetVelocity(rmotor, 1)
            sim.setJointTargetVelocity(lmotor, 1)

        # print("count=", count)

        # cv2.imshow('road', imgGrey)
        # cv2.waitKey(1)
        # cv2.destroyAllWindows

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
    visionSensorHandle = sim.getObject('/Diff_Drive_Bot/vision_sensor')
    img1, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
    img1 = np.frombuffer(img1, dtype=np.uint8).reshape(resY, resX, 3)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img1 = cv2.flip(img1, 0)
    listy = []

    # # global qrcount
    # odel=0
    # bdel=0
    # pdel=0

    # if(qrcount==0):
    #     checkp = "checkpoint E"
    #     qrcount+=1
    # elif(qrcount==1):
    #     checkp = "checkpoint I"
    #     qrcount+=1
    # elif(qrcount==2):
    #     checkp ="checkpoint M"
    #     qrcount+=1
    # print("qrcount =",qrcount)

    # detector = cv2.QRCodeDetector()
    # data, bbox, straight_qrcode = detector.detectAndDecode(gray)
    qrmsg = decode(img1)
    # if(qr_message==True):
    #     listy.append(qr_message)
    # for i in range(0, 100):
    #      print(qr_message[0].data.decode())
    # print(qrmsg)

    if (len(qrmsg) > 0):
        qr_message = qrmsg[0].data.decode()
        # print(objname)
        # if(objname=="Orange Cone" and odel==0):
        #     ## Retrieve the handle of the Arena_dummy scene object.
        # arena_dummy_handle = sim.getObject("/Arena_dummy")

        # ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        # childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

        # ## Deliver package_1 at checkpoint E
        # sim.callScriptFunction("deliver_package", childscript_handle, "package_1", checkp)
        # odel+=1
        #     print(checkp)
        # elif(objname=="Blue Cylinder" and bdel==0):
        #     ## Retrieve the handle of the Arena_dummy scene object.
        #     arena_dummy_handle = sim.getObject("/Arena_dummy")

        #     ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        #     childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

        #     ## Deliver package_1 at checkpoint E
        #     sim.callScriptFunction("deliver_package", childscript_handle, "package_2", checkp)
        #     bdel+=1
        #     print(checkp)
        # elif(objname=="Pink Cuboid" and pdel==0) :
        #     ## Retrieve the handle of the Arena_dummy scene object.
        #     arena_dummy_handle = sim.getObject("/Arena_dummy")

        #     ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
        #     childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

        #     ## Deliver package_1 at checkpoint E
        #     sim.callScriptFunction("deliver_package", childscript_handle, "package_3", checkp)
        #     pdel+=1
        #     print(checkp)

    # print(listy)

    # cv2.imshow('qr', img1)
    # cv2.waitKey(1)
    # cv2.destroyAllWindows

    # for i in range(0,100):
    #     print(data)
    ##################################################
    return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
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
            control_logic(sim)
            time.sleep(5)

        except Exception:
            print(
                '\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
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
