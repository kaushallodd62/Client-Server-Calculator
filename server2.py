import sys
from socket import *
from helper import getConnectionInfo
from _thread import start_new_thread
import threading

# Thread function
def threaded(connectionSocket, addr):
    while True:
        expr = connectionSocket.recv(1024).decode()
        print_lock.acquire()

        # If expr is empty (not blank), then client socket is closed.
        if not expr:
            print_lock.release()
            break
    
        print('Received from Client ' + str(addr) + ': ' + expr)
        
        try:
            resp = str(eval(expr))
        except ZeroDivisionError:
            resp = 'Divide by zero Error! Try again!'
        except:
            resp = 'Error! Send Valid Expression!'
        
        connectionSocket.send(resp.encode())
        print('Sent to Client ' + str(addr) + ': ' + resp)
        print_lock.release()

    # Closing the TCP connection with the client. The welcoming socket continues.
    connectionSocket.close()
    print('Disconected from ' + str(addr))
    print()


# Retrieving serverIP and serverPort from the user.
serverIP, serverPort = getConnectionInfo()

# Creating a lock variable
print_lock = threading.Lock()

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
MAX_CONN = 5
serverSocket.listen(MAX_CONN)
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

    # Start a new thread and return its identifier
    start_new_thread(threaded, (connectionSocket, addr,))

# Closing TCP connection.
serverSocket.close()
print('Server process terminated.')