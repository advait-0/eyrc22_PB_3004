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
# Filename:			socket_server.py
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
FORMAT = 'utf-8'
HEADER = 1024




##############################################################

def setup_server(host, port):

    """
    Purpose:
    ---
    This function creates a new socket server and then binds it 
    to a host and port specified by user.

    Input Arguments:
    ---
    `host` :	[ string ]
            host name or ip address for the server

    `port` : [ int ]
            integer value specifying port number
    Returns:

    `server` : [ socket object ]
    ---

    
    Example call:
    ---
    server = setup_server(host, port)
    """ 

    server = None

    ##################	ADD YOUR CODE HERE	##################
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (host, port)
    server.bind(addr)

    ##########################################################

    return server

def setup_connection(server):
    """
    Purpose:
    ---
    This function listens for an incoming socket client and
    accepts the connection request

    Input Arguments:
    ---
    `server` :	[ socket object ]
            socket object created by setupServer() function
    Returns:
    ---
    `connection` : [ socket object ]
            socket connection object

    `address` : [ tuple ]
            address of socket connection
    
    Example call:
    ---
    connection, address = setup_connection(server)
    """
    connection = None
    address = None

    ##################	ADD YOUR CODE HERE	##################
    server.listen()
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = server.accept()

    ##########################################################

    return connection, address

def receive_message_via_socket(connection):
    """
    Purpose:
    ---
    This function listens for a message from the specified
    socket connection and returns the message when received.

    Input Arguments:
    ---
    `connection` :	[ connection object ]
            connection object created by setupConnection() function
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
    print(f"Connected by {address}")
    msglength = connection.recv(HEADER).decode(FORMAT)
    msglength = int(msglength)

    message = connection.recv(msglength).decode(FORMAT)
    connection.sendall(message)
    print(f"[{address}] {message}")

    ##########################################################

    return message

def send_message_via_socket(connection, message):
    """
    Purpose:
    ---
    This function sends a message over the specified socket connection

    Input Arguments:
    ---
    `connection` :	[ connection object ]
            connection object created by setupConnection() function

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
    connection.send(message.encode())

    ##########################################################



######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN SECTION #########

if __name__ == "__main__":

        host = ''
        port = 5050


        ## Set up new socket server
        try:
            server = setup_server(host, port)

            # print(type(server))

        except socket.error as error:
            print("Error in setting up server")
            print(error)
            sys.exit()


        ## Set up new connection with a socket client
        try:
            connection, address = setup_connection(server)
            print(type(connection), type(address))
            print("Connected to: " + address[0] + ":" + str(address[1]))

        except KeyboardInterrupt:
            sys.exit()
            
        ## Send "START" command to PB task 3D socket client
        print("\nSTART command sent to PB Task 3D socket client\n")
        send_message_via_socket(connection, "START")


        ## Receive words from the original phrase until the command 'SHUFFLE'
        ## is received after which it breaks out of the loop.
        while True:
            
            message = receive_message_via_socket(connection)
            

            if message == "SHUFFLE":
                break

            else:
                print("Received message from client: " + message)

        print("\nWaiting for shuffled phrase \n")


        ## Receive words from the shuffled phrase until the command 'KILL'
        ## is received after which it breaks out of the loop.
        while True:
            
            message = receive_message_via_socket(connection)

            send_message_via_socket(connection, message)
            

            if message == "KILL":
                ## Socket server connection is closed when KILL command is received
                print("\nClosing socket server connection")
                connection.close()
                server.close()
                break

            else:
                print("Received message from client: " + message)




