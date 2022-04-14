import sys
from getopt import *
 
def getConnectionInfo():
    serverIP = ''
    serverPort = ''

    # Attemting to retrieve Command Line Arguments.
    try:
        opts, _ = getopt(sys.argv[1:], 'h:p:', ['hostname=', 'port='])
    except GetoptError:
        print('Usage: python3 file.py -h <hostname> -p <port>')
        sys.exit(1)
    
    # Assigning values to serverIP and serverPort.
    for opt, value in opts:
        if opt in ('-h', '-hostname'):
            serverIP = value
        elif opt in ('-p', '-port'):
            serverPort = value
            serverPort =  int(serverPort)

    # Checking if serverPort is empty.
    if serverPort == '':
        print('Usage: python3 file.py -h <hostname> -p <port>')
        sys.exit(1)
    
    # Returning serverIP and serverPort.
    return serverIP, serverPort


