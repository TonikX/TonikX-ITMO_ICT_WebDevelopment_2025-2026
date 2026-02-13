import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8911)

# Отправляем сообщение серверу
client_socket.sendto(b'Hello, server', server_address)

# Получаем ответ от сервера (с адресом отправителя)
response, server_addr = client_socket.recvfrom(1024)
print(f'Ответ от сервера {server_addr}: {response.decode()}')

# Закрываем соединение
client_socket.close()