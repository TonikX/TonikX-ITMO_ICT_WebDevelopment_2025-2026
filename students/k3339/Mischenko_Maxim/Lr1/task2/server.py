import socket

from utils import calc_pythagoras

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print('Waiting for connection...')
while True:
    client_socket, client_address = server_socket.accept()
    print('Got connection from', client_address)

    request = client_socket.recv(1024).decode()
    print(f'Received: {request}')

    a, b = map(float, request.split())
    result = calc_pythagoras(a, b)

    client_socket.sendall(str(result).encode())

    client_socket.close()
