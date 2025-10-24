import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))
#привязываем сокет к опр порту на нашем хосте

print("server running on port 8080")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f'Получено от {client_address}: {data.decode()}')

    response = "Hello, client!"
    server_socket.sendto(response.encode(), client_address)


