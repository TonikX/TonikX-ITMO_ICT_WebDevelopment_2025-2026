import socket
from utils import server_address

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)
print(f'Сервер запущен на {server_address[0]}:{server_address[1]}')

while True:
    # Получаем данные от клиента
    client_data, client_address = server_socket.recvfrom(1024)
    if client_data:
        print("Получены данные: ", client_data.decode("utf-8"))
        # Отправляем ответ обратно клиенту
        response = 'Hello, client'
        sent = server_socket.sendto(response.encode('utf-8'), client_address)