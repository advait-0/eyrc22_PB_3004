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
	
	vel = 1.5
	j = 1
	error = 0
	prev_error = 0.18
	P_Term = 0
	D_Term = 0
	kp = 3
	kd = 1
	dt = 1
	error_before_zero = 0.18
	while 1:

		distance1 = detect_distance_sensor_1(sim)
		distance2 = detect_distance_sensor_2(sim)
		
		dmin = 0.21
		# rmax = 0.255
		# rmin = 0.16

		if(distance1<=dmin and distance1!=0):
			sim.setJointTargetVelocity(lmotor,0)
			sim.setJointTargetVelocity(rmotor,0)

			if j<10:	
				if distance2<=0.5 and distance2!=0:
					vel = 0.5
					j+=1
					for i in range(93):
						sim.setJointTargetVelocity(lmotor,-vel)
						sim.setJointTargetVelocity(rmotor,vel)
					
					sim.setJointTargetVelocity(lmotor,0)
					sim.setJointTargetVelocity(rmotor,0)	
					vel = 1.5
					
				else:
					vel = 0.5
					j+=1
					for i in range(91):
						sim.setJointTargetVelocity(lmotor,vel)
						sim.setJointTargetVelocity(rmotor,-vel)
					
					sim.setJointTargetVelocity(lmotor,0)
					sim.setJointTargetVelocity(rmotor,0)	
					vel = 1.5
			else :
				break
		else:
			if distance2 == 0:
				distance2 = error_before_zero

			error = distance2 - prev_error
			P_Term = kp * error
			diff_error = error/dt
			
			# print(error)

			if diff_error > 0.1:
				diff_error = 0.1
			elif diff_error < -0.1:
				diff_error = -0.1

			D_Term = kd * diff_error	

			total_error = P_Term + D_Term
			print(total_error)

			if total_error < -0.4:
				print("Inside Right Rotation")
				sim.setJointTargetVelocity(lmotor,0)
				sim.setJointTargetVelocity(rmotor,vel * abs(total_error))
			elif total_error > 0.4:
				print("Inside Left ROtation")
				sim.setJointTargetVelocity(lmotor,vel * abs(total_error))
				sim.setJointTargetVelocity(rmotor,0)
			else:
				sim.setJointTargetVelocity(lmotor,vel)
				sim.setJointTargetVelocity(rmotor,vel)

			error_before_zero = distance2		

		

	

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
