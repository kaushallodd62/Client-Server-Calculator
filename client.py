import sys
from socket import *
from helper import getConnectionInfo

# Retrieving serverIP and serverPort from the user.
serverIP, serverPort = getConnectionInfo()

# Creating Client Socket with IPv4 Address Family and TCP type socket.
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except error as err:
    print('Client Socket Creation Error: ' + str(err))
    sys.exit(1)
print('Client Socket Creation Successful.')

# Establishing connection between Client and Server.
try:
    clientSocket.connect((serverIP, serverPort))
except error as err:
    print('Error connecting to server: ' + str(err))
    sys.exit(1)

# Server is ready to evaluate expressions.
print('Connected to Server: ' + str((serverIP, serverPort)))
print()

while True:
    try:
        expr = input("Enter Expression: ")
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt. Ending Client process...')
        break

    clientSocket.send(expr.encode())
    print('Sent to Server: ' + expr)

    resp = clientSocket.recv(1024).decode()
    print('Recieved from Server: ' + resp)

# Closing TCP connection.
clientSocket.close()
print('Client process terminated.')
