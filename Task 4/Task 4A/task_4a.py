'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
*  Author:				e-Yantra Team
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 3004 ]
# Author List:		[ Aryan Bawankar, Advait Dhamorikar ]
# Filename:			task_4a.py
# Functions:		[ place_packages, place_traffic_signals, place_start_end_nodes, place_horizontal_barricade, place_vertical_barricade]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

##############################################################

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    
####################### ADD YOUR CODE HERE #########################
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0 
    flag5 = 0
    for i in medicine_package_details:
        shop = i[0]
        if i[2] == "Circle":
            shape = "cylinder"
        elif i[2] == "Square":
            shape = "cube"
        elif i[2] == "Triangle":
            shape = "cone"
        # Setting Coordinate
        if shop == "Shop_1":
            if flag1 == 1:
                x = x + 0.09
            else:
                x = -0.9 + 0.044
                flag1 = 1
        elif shop == "Shop_2":
            if flag2 == 1:
                x = x + 0.09
            else:
                x = -0.54 + 0.044
                flag2 = 1
        elif shop == "Shop_3":
            if flag3 == 1:
                x = x + 0.09
            else:
                x = -0.18 + 0.044
                flag3 = 1
        elif shop == "Shop_4":
            if flag4 == 1:
                x = x + 0.09
            else:
                x = 0.18 + 0.044
                flag4 = 1
        elif shop == "Shop_5":
            if flag5 == 1:
                x = x + 0.09
            else:
                x = 0.54 + 0.044
                flag5 = 1

        package = i[1] + "_" + shape
        package_ttm = package + ".ttm"
        # print(shop, package)
        package_ttm = os.path.join(packages_models_directory, package_ttm)
        medicine = sim.loadModel(package_ttm)
        sim.setObjectParent(medicine, arena, False)
        sim.setObjectAlias(medicine, package)
        sim.setObjectPosition(medicine, arena, [x, 0.65, 0.015])
        all_models.append(medicine)

####################################################################
    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')   
####################### ADD YOUR CODE HERE #########################
    for i in traffic_signals:
        a = i[0]
        b = i[1]
        x = 0
        y = 0
        # setting up X Coordinate
        if a == 'A':
            x = -0.9
        elif a == 'B':
            x = -0.54
        elif a == 'C':
            x = -0.18
        elif a == 'D':
            x = 0.18
        elif a == 'E':
            x = 0.54
        elif a == 'F':
            x = 0.9
        
        # setting up Y Coordinate
        if b == '1':
            y = 0.9
        elif b == '2':
            y = 0.54
        elif b == '3':
            y = 0.18
        elif b == '4':
            y = -0.18
        elif b == '5':
            y = -0.54
        elif b == '6':
            y = -0.9
        name = "Signal_" + i
        position = [x, y, 0.15588]
        signal = sim.loadModel(traffic_sig_model)
        sim.setObjectParent(signal, arena, False)
        sim.setObjectAlias(signal, name)
        sim.setObjectPosition(signal, arena, position)
        all_models.append(signal)
####################################################################
    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   
####################### ADD YOUR CODE HERE #########################
    a = start_node[0]
    b = start_node[1]
    x = 0
    y = 0
       # setting up X Coordinate
    if a == 'A':
            x = -0.9
    elif a == 'B':
            x = -0.54
    elif a == 'C':
            x = -0.18
    elif a == 'D':
            x = 0.18
    elif a == 'E':
            x = 0.54
    elif a == 'F':
            x = 0.9

        # setting up Y Coordinate
    if b == '1':
            y = 0.9
    elif b == '2':
            y = 0.54
    elif b == '3':
            y = 0.18
    elif b == '4':
            y = -0.18
    elif b == '5':
            y = -0.54
    elif b == '6':
            y = -0.9
    name = "Start_Node"
    position = [x, y, 0.15588]
    start_node = sim.loadModel(start_node_model)
    sim.setObjectParent(start_node, arena, False)
    sim.setObjectAlias(start_node, name)
    sim.setObjectPosition(start_node, arena, position)
    all_models.append(start_node)

    a = end_node[0]
    b = end_node[1]
    x = 0
    y = 0
    # setting up X Coordinate
    if a == 'A':
        x = -0.9
    elif a == 'B':
        x = -0.54
    elif a == 'C':
        x = -0.18
    elif a == 'D':
        x = 0.18
    elif a == 'E':
        x = 0.54
    elif a == 'F':
        x = 0.9

        # setting up Y Coordinate
    if b == '1':
        y = 0.9
    elif b == '2':
        y = 0.54
    elif b == '3':
        y = 0.18
    elif b == '4':
        y = -0.18
    elif b == '5':
        y = -0.54
    elif b == '6':
        y = -0.9
    name = "End_Node"
    position = [x, y, 0.15588]
    end_node = sim.loadModel(end_node_model)
    sim.setObjectParent(end_node, arena, False)
    sim.setObjectAlias(end_node, name)
    sim.setObjectPosition(end_node, arena, position)
    all_models.append(end_node)
####################################################################
    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  
####################### ADD YOUR CODE HERE #########################
    for i in horizontal_roads_under_construction:
        nodes = i

        A = nodes[0]
         # setting up X Coordinate
        if A == 'A':
            x = -0.9
        elif A == 'B':
            x = -0.54
        elif A == 'C':
            x = -0.18
        elif A == 'D':
            x = 0.18
        elif A == 'E':
            x = 0.54
        elif A == 'F':
            x = 0.9
        x = x + 0.18
        
        C = nodes[1]
         # setting up Y Coordinate
        if C == '1':
            y = 0.9
        elif C == '2':
            y = 0.54
        elif C == '3':
            y = 0.18
        elif C == '4':
            y = -0.18
        elif C == '5':
            y = -0.54
        elif C == '6':
            y = -0.9
        

        positions = [x, y, 0.027]
        name = "Horizontal_missing_road_" + A + C + "_" + nodes[3] + nodes[4]
        h_barricade = sim.loadModel(horiz_barricade_model)
        sim.setObjectParent(h_barricade, arena, False)
        sim.setObjectAlias(h_barricade, name)
        sim.setObjectPosition(h_barricade, arena, positions)
        all_models.append(h_barricade)
####################################################################
    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena') 
####################### ADD YOUR CODE HERE #########################
    for i in vertical_roads_under_construction:
        nodes = i

        A = nodes[0]
         # setting up X Coordinate
        if A == 'A':
            x = -0.9
        elif A == 'B':
            x = -0.54
        elif A == 'C':
            x = -0.18
        elif A == 'D':
            x = 0.18
        elif A == 'E':
            x = 0.54
        elif A == 'F':
            x = 0.9
        
        C = nodes[1]
         # setting up Y Coordinate
        if C == '1':
            y = 0.9
        elif C == '2':
            y = 0.54
        elif C == '3':
            y = 0.18
        elif C == '4':
            y = -0.18
        elif C == '5':
            y = -0.54
        elif C == '6':
            y = -0.9
        y = y - 0.18

        positions = [x, y, 0.027]
        name = "Vertical_missing_road_" + A + C + "_" + nodes[3] + nodes[4]
        v_barricade = sim.loadModel(vert_barricade_model)
        sim.setObjectParent(v_barricade, arena, False)
        sim.setObjectAlias(v_barricade, name)
        sim.setObjectPosition(v_barricade, arena, positions)
        all_models.append(v_barricade)
####################################################################
    return all_models


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    # arena = sim.getObject('/Arena')
    aruco_handle = sim.getObject('/aruco_3')

    arena = sim.getObject('/Arena')
    # sim.setObjectParent(aruco_handle, arena, False)
    # sim.setObjectAlias(aruco_handle, "marker")
    sim.setObjectPosition(aruco_handle, -1, [0.15, 0.15, 0.15])
    sim.setObjectOrientation(aruco_handle, -1, [0, 0, 45])
    # path directory of images in test_images folder
    img_dir = os.getcwd() + "/test_imgs/"

    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters[
        'horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters[
        'vertical_roads_under_construction']

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(
        horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(
        vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)

    choice = input(
        '\nDo you want to run your script on all test images ? => "y" or "n": ')

    if choice == 'y':
        for i in range(1, 5):

            print('\n============================================')
            print('\nFor maze_' + str(i) + '.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(
                config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters[
                'horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters[
                'vertical_roads_under_construction']

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(
                horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(
                vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            