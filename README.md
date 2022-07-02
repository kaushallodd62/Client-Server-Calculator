# Client Server Calculator

The server program is started on a custom port provided as a command line argument (if the port isn't already occupied). Client Program is started on a custom port Next, the client program is started, again on custom port. The client sends a mathematical expression to the server. The server responds with the result.

* All Sockets use TCP and IPv4 Protocols.
* server1.py is a single process that handles one client at a time.
* server2.py is a multi-threaded server that concurrently handles multiple clients at a time.
* server3.py is a single process that handles multiple clients at a time using the "select" method.
* server4.py is a multi-threaded echo server that handles multiple clients at a time.
