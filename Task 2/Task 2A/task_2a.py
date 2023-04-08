'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
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

##############################################################


def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	lproximity = sim.getObjectHandle('distance_sensor_3')
	flag, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
		lproximity)
	# print(flag,distance)

	##################################################
	return distance
def control_logic(sim):
    """
    Purpose:
    ---
    This function should implement the control logic for the given problem statement
    You are required to actuate the rotary joints of the robot in this function, such that
    it traverses the points in given order

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

    lmotor = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
    rmotor = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
    breakcount = 0
    while (breakcount!=1):
         
         distance1 = detect_distance_sensor_1(sim)
         distance2 = detect_distance_sensor_2(sim)
         distance3= detect_distance_sensor_3(sim)

        #  print(distance1,distance2,distance3)
         if (distance1 == 0.0 and distance2 <= 0.26 and distance3<=0.26 and distance3>=0.15 and distance2>=0.15):
           sim.setJointTargetVelocity(lmotor, 4)
           sim.setJointTargetVelocity(rmotor, 4)
         elif(distance2<= 0.18 and distance3>0.14 and distance1==0):
           sim.setJointTargetVelocity(lmotor, 0.7)
           sim.setJointTargetVelocity(rmotor, 1)
           sim.setJointTargetVelocity(lmotor, 1)
           sim.setJointTargetVelocity(rmotor, 1)
           
        #    print("left")
         elif(distance2> 0.14 and distance3<=0.20 and distance1==0):
           sim.setJointTargetVelocity(lmotor, 1)
           sim.setJointTargetVelocity(rmotor, 0.7)
           sim.setJointTargetVelocity(lmotor, 1)
           sim.setJointTargetVelocity(rmotor, 1)

        #    print("right")
         elif(distance1<=0.23 and distance2!=0 and distance3==0.0):
             for i in range(0, 23):
                 sim.setJointTargetVelocity(rmotor, 2)
                 sim.setJointTargetVelocity(lmotor, -2)
             for i in range(0, 12):
                 sim.setJointTargetVelocity(rmotor, 3.5)
                 sim.setJointTargetVelocity(lmotor, 3.5)
            
         elif (distance1 <= 0.23 and distance2 == 0 and distance3 != 0):
             for i in range(0, 24):
                 sim.setJointTargetVelocity(rmotor, -2)
                 sim.setJointTargetVelocity(lmotor, 2)
             for i in range(0, 11):
                 sim.setJointTargetVelocity(rmotor, 3.5)
                 sim.setJointTargetVelocity(lmotor, 3.5)
         elif(distance1<=0.20 and distance2!=0 and distance3!=0 and distance1!=0):
             sim.setJointTargetVelocity(rmotor, 0)
             sim.setJointTargetVelocity(lmotor, 0)
             breakcount=1
             break
             
     
     

        
     
  






                
        

    

    ##################################################

def detect_distance_sensor_1(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_1 = detect_distance_sensor_1(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############
    fproximity = sim.getObjectHandle('distance_sensor_1')
    flag,distance,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.readProximitySensor(fproximity)

    # print(flag,distance)	


    ##################################################
    return distance

def detect_distance_sensor_2(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_2 = detect_distance_sensor_2(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############
    rproximity = sim.getObjectHandle('distance_sensor_2')
    flag,distance,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=sim.readProximitySensor(rproximity)
    # print(flag,distance)


    ##################################################
    return distance


def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	lproximity = sim.getObjectHandle('distance_sensor_3')
	flag, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
		lproximity)
	# print(flag,distance)

	##################################################
	return distance

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
 
