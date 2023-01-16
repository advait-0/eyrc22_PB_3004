'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3D of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			socket_server_pt1.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def setup_client(host, port):

	"""
	Purpose:
	---
	This function creates a new socket client and then tries
    to connect to a socket server.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`client` : [ socket object ]
	           a new client socket object
	---

	
	Example call:
	---
	client = setup_client(host, port)
	""" 

	client = None

	##################	ADD YOUR CODE HERE	##################
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host,port))
	##########################################################

	return client

def receive_message_via_socket(client):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket client and returns the message when received.

	Input Arguments:
	---
	`client` :	[ socket object ]
			socket client object created by setup_client() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################
	message = client.recv(4096).decode()

	##########################################################

	return message

def send_message_via_socket(client, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket client

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################
	client.sendall(message.encode())

	##########################################################

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN SECTION #########
#########      APART FROM THE REQUIRED AREAS (host, port etc)     #########

if __name__ == "__main__":

		host = "192.168.1.5"
		port = 5050


		## Set up new socket client and connect to a socket server
		try:
			client = setup_client(host, port)

			# print(type(client))

		except socket.error as error:
			print("Error in setting up client")
			print(error)
			sys.exit()

		## Send "START" command to PB task 3D socket
		print("\nSTART command sent to PB Task 3D socket server\n")
		send_message_via_socket(client, "START")

		## Receive words from the original phrase until the command 'SHUFFLE'
		## is received after which it breaks out of the loop.
		while True:
			
			message = receive_message_via_socket(client)
			

			if message == "SHUFFLE":
				break

			else:
				print("Received message from server: " + message)

		print("\nWaiting for shuffled phrase \n")


		## Receive words from the shuffled phrase until the command 'KILL'
		## is received after which it breaks out of the loop.
		while True:
			
			message = receive_message_via_socket(client)

			send_message_via_socket(client, message)
			

			if message == "KILL":
				## Socket server connection is closed by the server
				print("\nSocket connection closed by server")
				break

			else:
				print("Received message from server: " + message)

