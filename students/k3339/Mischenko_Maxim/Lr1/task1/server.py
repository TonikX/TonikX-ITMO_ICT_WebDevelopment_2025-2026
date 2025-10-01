import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print('Started server on port 8080')
while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f'Received from {client_address}: {data.decode()}')

    response = b'Hello, client'
    server_socket.sendto(response, client_address)
