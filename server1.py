import sys
from socket import *
from helper import getConnectionInfo

# Retrieving serverIP and serverPort from the user.
serverIP, serverPort = getConnectionInfo()

# Creating Welcoming Server Socket with IPv4 Address Family and TCP type socket.
try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
except error as err:
    print('Server Socket Creation Error: ' + str(err))
    sys.exit(1)
print('Server Socket Creation Successful.')

# Binding the socket to serverIP and serverPort.
try:
    serverSocket.bind((serverIP, serverPort))
except error as err:
    print('Server Socket Binding Error: ' + str(err))
    sys.exit(1)
print('Server Socket Bound to ' + str((serverIP, serverPort)))

# Listening for incoming connections.
serverSocket.listen(1)
print('Server is ready to recieve ...')
print()

while True:
    # Welcomes new connections until Ctrl + C is pressed.
    try:
        connectionSocket, addr = serverSocket.accept()
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt. Ending Server process...')
        break
    print('Server connected with ' + str(addr))

    # Connection with Client persists until Client terminates process.
    while True:
        expr = connectionSocket.recv(1024).decode()
        # If expr is empty (not blank), then client socket is closed.
        if not expr:
            break
        print('Received from Client: ' + expr)

        try:
            resp = str(eval(expr))
        except ZeroDivisionError:
            resp = 'Divide by zero Error! Try again!'
        except:
            resp = 'Error! Send Valid Expression!'
        
        connectionSocket.send(resp.encode())
        print('Sent to Client: ' + resp)
    # Closing the TCP connection with the client. The welcoming socket continues.
    connectionSocket.close()
    print('Disconected from ' + str(addr))
    print()

# Closing TCP connection.
serverSocket.close()
print('Server process terminated.')