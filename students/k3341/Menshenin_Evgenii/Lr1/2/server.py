import socket
from mathematics import parse_math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8082))
server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()

    math = parse_math(request).do_math()

    client_connection.sendall(str(math).encode())
