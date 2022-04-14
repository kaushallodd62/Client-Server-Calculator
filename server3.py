import sys
from socket import *
from select import select
from queue import Queue
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

# inputSockets is a list of sockets, i.e file descriptors that are waiting to be read. (recv data from)
inputSockets = [serverSocket]
# outputSockets is a list of sockets, i.e file descriptors that are waiting to be written on. (respond data to)
outputSockets = []
# messageQueue is a map of (socket, Queue) pair where each connection has a queue of resp messages to send to the client.
messageQueue = {}

try:
    while inputSockets:
        # readable, writable and exceptional are three lists corresponding to the first three arguments;
        # each contains the subset of the corresponding file descriptors that are ready.
        readable, writable, exceptional = select(inputSockets, outputSockets, outputSockets)
        for socket in readable:
            if socket is serverSocket:
                # After establishing a connenction with a client, the connectionSocket created is appended to the inputSockets and a (socket, Queue)
                # pair is created in messageQueue map.
                connectionSocket, addr = serverSocket.accept()
                print('Server connected with ' + str(addr))
                inputSockets.append(connectionSocket)
                messageQueue[connectionSocket] = Queue()
            else:
                expr = socket.recv(1024).decode()
                # If expr is empty (not blank), then client socket is removed from inputSockets and outputSockets.
                # The (socket, Queue) pair for the client socket will also be deleted.
                # The connectionSocket to that client to closed.
                if not expr:
                    inputSockets.remove(socket)
                    del messageQueue[socket]
                    if socket in outputSockets:
                        outputSockets.remove(socket)
                    print('Disconected from ' + str(socket.getpeername()))
                    print()
                    socket.close()

                # If expr is not empty, we evaluate the expression and add the resp to the messageQueue. We also add the socket to the outputSockets.
                else:
                    print('Received from Client ' + str(socket.getpeername()) + ': ' + expr)

                    try:
                        resp = str(eval(expr))
                    except ZeroDivisionError:
                        resp = 'Divide by zero Error! Try again!'
                    except:
                        resp = 'Error! Send Valid Expression!'
                    
                    messageQueue[socket].put(resp)
                    if socket not in outputSockets:
                        outputSockets.append(socket)
            
        for socket in writable:
            try:
                resp = messageQueue[socket].get_nowait()
                print('Sent to Client ' + str(socket.getpeername()) + ': ' + resp)
                socket.send(resp.encode())
            except:
                outputSockets.remove(socket)
            
        for socket in exceptional:
            inputSockets.remove(socket)
            if socket in outputSockets:
                outputSockets.remove(socket)
            del messageQueue[socket]
            socket.close()
except KeyboardInterrupt:
    print('\nKeyboard Interrupt. Ending Server process...')

# Closing TCP connection.
serverSocket.close()
print('Server process terminated.')
