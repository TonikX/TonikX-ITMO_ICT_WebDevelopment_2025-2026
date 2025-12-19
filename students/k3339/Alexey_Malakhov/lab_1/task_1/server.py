import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8080))

print("UDP сервер запущен на порту 8080...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f'Подключение от {client_address}')

    request = data.decode()
    print(f'Запрос от клиента: {request}')

    response = 'Hello, client!'
    server_socket.sendto(response.encode(), client_address)
