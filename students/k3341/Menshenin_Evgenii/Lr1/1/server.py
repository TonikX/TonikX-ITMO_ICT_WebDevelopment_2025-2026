import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8081))


while True:
    data, address = server_socket.recvfrom(1024)
    print(data.decode())

    response = 'Hello, client!'
    server_socket.sendto(response.encode(), address)

