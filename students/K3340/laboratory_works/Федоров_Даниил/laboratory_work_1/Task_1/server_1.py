import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 1234))

print('Сервер запущен')

while True:
    data, address = server_socket.recvfrom(1024)
    print(f'{data.decode()}')
    server_socket.sendto(b'Hello, client', address)




