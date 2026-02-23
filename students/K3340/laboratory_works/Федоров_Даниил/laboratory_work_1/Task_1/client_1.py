import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 1234)

client_socket.sendto(b'Hello, server', server_address)

data, address = client_socket.recvfrom(1024)
print(f'{data.decode()}')