import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4, UDP

# Адрес сервера
server_address = ('localhost', 8080)

# Отправляем сообщение серверу
client_socket.sendto(b'Hello, server', server_address)  # b перед строкой, чтобы сообщение было в байтах

# Получаем ответ от сервера
response, server_addr = client_socket.recvfrom(1024)  # Максимальный размер получаемых данных — 1024 байта
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()