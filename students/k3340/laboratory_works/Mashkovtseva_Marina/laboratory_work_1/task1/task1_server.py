import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, UDP
# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))

print("Сервер запущен на порту 8080...")

while True:
    # Получаем сообщение от клиента и его адрес
    data, client_address = server_socket.recvfrom(1024)
    request = data.decode()
    print(f'Запрос от клиента {client_address}: {request}')

    # Отправляем ответ клиенту
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)