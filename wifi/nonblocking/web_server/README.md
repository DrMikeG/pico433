I Pico W LED web server
Learning from https://docs.python.org/3/howto/sockets.html

Watching https://youtu.be/2Oq4FQSr21I


https://github.com/voidrealms/python3/blob/main/python3-59/python3-59.py

https://stackoverflow.com/questions/5308080/python-socket-accept-nonblocking
```
import select
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 8888))
server_socket.listen(5)
print "Listening on port 8888"

read_list = [server_socket]
while True:
    readable, writable, errored = select.select(read_list, [], [])
    for s in readable:
        if s is server_socket:
            client_socket, address = server_socket.accept()
            read_list.append(client_socket)
            print "Connection from", address
        else:
            data = s.recv(1024)
            if data:
                s.send(data)
            else:
                s.close()
                read_list.remove(s)
```

It looks like the accept can be done as a reaction to data being readable?

# Accept #
https://docs.python.org/3/library/socket.html#socket.socket.accept
Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection.

