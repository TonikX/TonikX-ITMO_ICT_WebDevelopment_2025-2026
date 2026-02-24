import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
client_socket.sendto(b'Hello, server!', (socket.gethostname(), 8080))

# Получаем ответ от сервера
response, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем сокет
client_socket.close()
